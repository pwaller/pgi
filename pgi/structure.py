# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import cast

from pgi.codegen.fieldgen import generate_field_getter, generate_field_setter
from pgi.gir import GIUnionInfoPtr, GIFieldInfoFlags, GIStructInfoPtr
from pgi.glib import g_try_malloc0, free
from pgi.gtype import PGType
from pgi.obj import MethodAttribute


class _DummyInfo(object):
    def get_methods(self):
        return []


class BaseUnion(object):
    """A base class for all unions (for type checking..)"""


class _Union(BaseUnion):
    __info__ = _DummyInfo()
    __gtype__ = None
    _obj = 0
    _size = 0
    _needs_free = False

    def __init__(self):
        obj = g_try_malloc0(self._size)
        if not obj and self._size:
            raise MemoryError(
                "Could not allocate structure %r" % self.__class__.__name__)
        self._obj = obj
        self._needs_free = True

    def __repr__(self):
        form = "<%s union at 0x%x (%s at 0x%x)>"
        name = type(self).__name__
        return form % (name, id(self), self.__gtype__.name, self._obj)

    __str__ = __repr__

    def __del__(self):
        if self._needs_free:
            free(self._obj)


class BaseStructure(object):
    """A base class for all structs (for type checking..)"""


class _Structure(BaseStructure):
    """Class template for structures."""

    _obj = None  # the address of the struct
    _size = 0 # size fo the struct in bytes
    __gtype__ = None  # the gtype
    _needs_free = False

    def __init__(self):
        obj = g_try_malloc0(self._size)
        if not obj and self._size:
            raise MemoryError(
                "Could not allocate structure %r" % self.__class__.__name__)
        self._obj = obj

    def __repr__(self):
        form = "<%s structure at 0x%x (%s at 0x%x)>"
        name = type(self).__name__
        return form % (name, id(self), self.__gtype__.name, self._obj)

    __str__ = __repr__

    def __del__(self):
        if self._needs_free:
            free(self._obj)


class FieldAttribute(object):
    _getter = None
    _setter = None

    def __init__(self, info):
        self._info = info
        self._readable = info.flags.value & GIFieldInfoFlags.IS_READABLE
        self._writeable = info.flags.value & GIFieldInfoFlags.IS_WRITABLE

    def __get__(self, instance, owner):
        if not self._readable:
            raise AttributeError

        if not self._getter:
            self._getter = generate_field_getter(self._info)

        if instance:
            return self._getter(instance)
        return self

    def __set__(self, instance, value):
        if not self._writeable:
            raise AttributeError

        if not self._setter:
            self._setter = generate_field_setter(self._info)

        if instance:
            return self._setter(instance, value)
        return self


def UnionAttribute(info):
    union_info = cast(info, GIUnionInfoPtr)

    cls = type(info.name, _Union.__bases__, dict(_Union.__dict__))
    cls.__module__ = info.name
    cls.__gtype__ = PGType(union_info.g_type)
    cls._size = union_info.size

    # Add methods
    for method_info in union_info.get_methods():
        method_name = method_info.name
        attr = MethodAttribute(method_info)
        setattr(cls, method_name, attr)

    # Add fields
    for field_info in union_info.get_fields():
        field_name = field_info.name
        attr = FieldAttribute(field_info)
        setattr(cls, field_name, attr)

    return cls


def StructureAttribute(info):
    """Creates a new struct class."""

    struct_info = cast(info, GIStructInfoPtr)

    # Copy the template and add the gtype
    cls_dict = dict(_Structure.__dict__)
    cls = type(info.name, _Structure.__bases__, cls_dict)
    cls.__module__ = info.namespace
    cls.__gtype__ = PGType(struct_info.g_type)
    cls._size = struct_info.size

    # Add methods
    for method_info in struct_info.get_methods():
        method_name = method_info.name
        attr = MethodAttribute(method_info)
        setattr(cls, method_name, attr)

    # Add fields
    for field_info in struct_info.get_fields():
        field_name = field_info.name
        attr = FieldAttribute(field_info)
        setattr(cls, field_name, attr)

    return cls
