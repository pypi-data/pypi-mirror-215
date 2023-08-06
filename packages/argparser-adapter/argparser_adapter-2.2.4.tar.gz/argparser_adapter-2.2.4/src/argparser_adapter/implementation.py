#!/usr/bin/env python3
import argparse
import collections
import functools
import inspect
import itertools
from dataclasses import dataclass
from typing import Any, Dict, Tuple, List

from . import adapter_logger

METHOD_METADATA: Dict[str, 'CommandLine'] = {}
CHOICE_METADATA: Dict[str, 'ChoiceCommand'] = {}


class CommandLine(object):
    def __init__(self, required: bool = False, default=None):
        self.required = required
        self.default = default

    def __call__(self, original_func):
        @functools.wraps(original_func)
        def wrappee(*args, **kwargs):
            original_func(*args, **kwargs)

        self.client = original_func
        METHOD_METADATA[original_func.__qualname__] = self
        return wrappee

    def __str__(self):
        return f"{self.client.__qualname__} required {self.required} default {self.default}"


@dataclass
class Choice:
    """name: metavar or option name
    is_position: Argument is positional if True, -- style option if not
    default: Default value for choice, if any
    help: Header for help. Choice values are added automatically
    """
    name: str
    is_position: bool
    default: object = None
    help: str = None


class ChoiceCommand(object):
    def __init__(self, choice: Choice):
        self.choice = choice

    def __call__(self, original_func):
        @functools.wraps(original_func)
        def wrappee(*args, **kwargs):
            original_func(*args, **kwargs)

        self.client = original_func
        CHOICE_METADATA[original_func.__qualname__] = self
        return wrappee

    def __str__(self):
        return f"{self.client.__qualname__} choice {self.choice}"


class ArgparserAdapter:
    BOOL_YES = ('true', 'on', 'yes')
    BOOL_NO = ('false', 'off', 'no')

    _INSTANCE: 'ArgparserAdapter' = None

    def __init__(self, client, *, group: bool = False, required: bool = False):
        """client: object to analyze for methods
        group: put arguments in an arparse group
        required: if using a group, make it required"""
        if not ArgparserAdapter._INSTANCE is None:
            raise ValueError(f"Only one {self.__class__.__name__} currently supported")
        ArgparserAdapter._INSTANCE = self
        self.client = client
        self.argadapt_required = required
        self.argadapt_group = group
        self._argadapt_dict = {}
        self._choice_dict = collections.defaultdict(dict)

    def param_conversion_exception(self, e: Exception, method_name: str, parameter_name: str, parameter_type: type,
                                   value: str) -> Any:
        """
        :param e: Exception thrown
        :param method_name: called method
        :param parameter_name: parameter name
        :param parameter_type:
        :param value: value passed on command line
        :return: valid value for parameter_type, or raise exception
        """
        raise ValueError(f"conversion error of method {method_name} parameter {parameter_name} value {value} {e}")

    def register(self, argparser: argparse.ArgumentParser) -> None:
        """Add arguments to argparser based on self.argadapt_settings"""
        needarg = False
        if self.argadapt_group:
            ap = argparser.add_mutually_exclusive_group(required=self.argadapt_required)
            arequired = False
            needarg = True
        else:
            ap = argparser
            arequired = self.argadapt_required
        choice_args: List[Tuple[Choice, List]] = []
        for d in inspect.getmembers(self.client, self.__only_methods):
            name, mobj = d
            kwargs = {}
            if (meta := METHOD_METADATA.get(mobj.__func__.__qualname__, None)) is not None:
                if meta.required and meta.default is not None:
                    adapter_logger.warning(f"Default with required {meta}")
                else:
                    adapter_logger.info(meta)
                kwargs = {'required': meta.required}
                if meta.default is not None:
                    kwargs['default'] = meta.default
            if (choice_meta := CHOICE_METADATA.get(mobj.__func__.__qualname__, None)) is not None:
                if meta is not None:
                    raise ValueError(f"{name} can only be decorated once")
                for choice, values in choice_args:
                    if choice == choice_meta.choice:
                        values.append(name)
                        break
                else:
                    choice_args.append((choice_meta.choice, [name]))
                doc = inspect.getdoc(mobj)
                self._choice_dict[choice_meta.choice.name][name] = (getattr(self.client, name),doc)

            doc = inspect.getdoc(mobj)
            if meta is not None:
                needarg = False
                arg = name
                sig = inspect.signature(mobj, follow_wrapped=True)
                ptypes = [p for _, p in sig.parameters.items()]
                self._argadapt_dict[arg] = (getattr(self.client, name), ptypes)
                nargs = len(ptypes)
                if nargs > 0:
                    desc = tuple(sig.parameters.keys())
                    if meta is not None:
                        ap.add_argument(f'--{arg}', nargs=nargs, metavar=desc, help=doc, **kwargs)
                    else:
                        ap.add_argument(f'--{arg}', nargs=nargs, metavar=desc, required=arequired, help=doc)
                else:
                    if meta is not None:
                        ap.add_argument(f'--{arg}', action='store_true', help=doc, **kwargs)
                    else:
                        ap.add_argument(f'--{arg}', action='store_true', help=doc)
        if needarg:
            raise ValueError(
                f"No methods marked @CommandLine found and group is required")
        for choice, values in choice_args:
            helpdocs = []
            if choice.help:
                helpdocs.append(choice.help)
            for optioname, v in self._choice_dict[choice.name].items():
                if v[1] != None:
                    helpdocs.append(f"{optioname} ({v[1]})")
            help = '\n'.join(helpdocs)
            if choice.is_position:
                ap.add_argument(choice.name,choices=values,default=choice.default,help=help)
            else:
                ap.add_argument(f"--{choice.name}",choices=values,default=choice.default,help=help)

    @staticmethod
    def _interpret(typ, value):
        if typ.annotation != bool:
            return typ.annotation(value)
        lvalue = value.lower()
        if lvalue in ArgparserAdapter.BOOL_YES:
            return True
        if lvalue in ArgparserAdapter.BOOL_NO:
            return False
        try:
            return bool(int(value))
        except:
            pass
        vals = itertools.chain(ArgparserAdapter.BOOL_YES, ArgparserAdapter.BOOL_NO)
        raise ValueError(f"Unable to interpret {value} as bool. Pass one of {','.join(vals)} or integer value")

    def call_specified_methods(self, args: argparse.Namespace) -> None:
        """Call method from parsed args previously registered"""
        for name, mspec in self._argadapt_dict.items():
            params = getattr(args, name, None)
            if params:
                method, iparams = mspec
                if params is True:  # noaction store_true argument
                    method()
                    continue
                if not isinstance(params, list):
                    params = [params]
                #                assert (len(params) == len(iparams))
                callparams = []
                for value, ptype in zip(params, iparams):
                    if ptype.annotation != ptype.empty:
                        try:
                            value = self._interpret(ptype, value)
                        except Exception as e:
                            value = self.param_conversion_exception(e, name, ptype.name, ptype.annotation, value)
                    callparams.append(value)
                method(*callparams)
        for name, ctuple in self._choice_dict.items():
            value = getattr(args, name, None)
            if value:
                method = ctuple[value][0]
                method()


    @staticmethod
    def __only_methods(x):
        return inspect.ismethod(x)
