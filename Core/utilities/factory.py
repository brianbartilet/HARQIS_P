from importlib import import_module
from typing import TypeVar, Generic, Type
import sys
from Core.utilities.custom_logger import custom_logger

T = TypeVar('T')


log = custom_logger('EPA Page Factory')


class EpaFactory(Generic[T]):

    def __new__(cls, kls: Type[T], override_base=True, **kwargs) -> T:
        bgroup = kwargs.get('bgroup')
        if override_base:
            module_path = "Application.ePA.pages.bgroups.{0}".format(bgroup)
            kls_name = kls.__name__.lstrip('I')
        else:
            module_path = "Application.ePA.pages.base"
            kls_name = kls.__name__
        try:
            module = import_module(module_path)
            _kls = getattr(module, kls_name)
            instance =_kls(**kwargs)
            if instance is None:
                sys.exit("Cannot create class instance. Please check parameters.")
            return instance
        except ModuleNotFoundError:
            log.error("BGROUP '{0}' Invalid, no modules found.  Please check target page instantiation".format(bgroup))
        except AttributeError:
            log.error("Page '{0}' does not exist for BGROUP '{1}'".format(kls_name, bgroup))
