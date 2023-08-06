"""
uniquorn - a metaclass to create class instances with the same parameters only once
"""
from inspect import signature
from typing import TypeVar, Any, Type


C = TypeVar("C")
T = TypeVar("T")
PROTECT = list | tuple | set | bool


class Uniquorn(type):
    """
    A metaclass to create class instances with the same parameters only once

    By default, lists and dicts parameters are sorted.
    To suppress sorting, in the class define
    - _uniquorn_list_order_matters = True
    - _uniquorn_dict_order_matters = True

    Caveats:
    - Uniquorns are only created uniquely
        It will not be noted if you later change the instance parameters.
        So if you really want you can still create duplicate instances.
    - Uniqueness is limited
        Structured parameters will easily bypass the uniqueness mechanism.
    """
    def __new__(cls, name, bases, attrs):
        """
        Prepare each class to register its unique instances
        """
        cls = super().__new__(cls, name, bases, attrs)
        cls._uniquorn_instances = {}
        return cls

    def _uniquorn_parameter_order_not_protected(
            cls,
            name: str,
            order_protection: PROTECT,
    ) -> bool:
        if isinstance(order_protection, (list, tuple, set)):
            return name not in order_protection
        return order_protection is not True

    def _uniquorn_parameter_order_not_protected_through_attribute(
            cls,
            name: str,
            order_protection_attribute_name: str,
    ) -> bool:
        if hasattr(cls, order_protection_attribute_name):
            return cls._uniquorn_parameter_order_not_protected(name, getattr(cls, order_protection_attribute_name))
        return True

    def _uniquorn_canonical_parameter_value(
            cls,
            name: str,
            value: T,
    ) -> T:
        match value:
            case list() if cls._uniquorn_parameter_order_not_protected_through_attribute(name, "uniquorn_list_order_matters"):
                return list(sorted(value))
            case dict() if cls._uniquorn_parameter_order_not_protected_through_attribute(name, "uniquorn_dict_order_matters"):
                return {
                    k: v
                    for k, v in sorted(value.items())
                }
            case _:
                return value

    def _uniquorn_instance_key(cls, *args: Any, **kwargs: Any) -> str:
        """
        Compute a unique key for a set of instantiation parameters
        """
        arguments = signature(cls.__init__).bind("self", *args, **kwargs).arguments
        return f"""{", ".join(
            f"{name}={cls._uniquorn_canonical_parameter_value(name, value)}"
            for name, value in arguments.items()
            if name != "self"
        )}"""

    def __call__(cls: C, *args: Any, **kwargs: Any) -> C:
        """
        Avoid creating a class instance with the same parameters twice.
        :return: unique instance
        """
        key = cls._uniquorn_instance_key(*args, **kwargs)
        if key not in cls._uniquorn_instances:
            cls._uniquorn_instances[key] = super(Uniquorn, cls).__call__(*args, **kwargs)
        return cls._uniquorn_instances[key]
