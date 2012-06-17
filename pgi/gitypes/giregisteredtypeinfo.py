# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import POINTER

from glib import *
from gobject import *
from gibaseinfo import *
from _util import load, wrap_class

_gir = load("girepository-1.0")


def gi_is_registered_type_info(base_info):
    type_ = base_info.get_type().value
    it = GIInfoType
    return type_ in (it.BOXED, it.ENUM, it.FLAGS, it.INTERFACE, it.OBJECT,
                     it.STRUCT, it.UNION)


class GIRegisteredTypeInfo(GIBaseInfo):
    pass


class GIRegisteredTypeInfoPtr(POINTER(GIRegisteredTypeInfo)):
    _type_ = GIRegisteredTypeInfo

    def __repr__(self):
        values = {}
        values["type_name"] = self.get_type_name()
        values["type_init"] = self.get_type_init()
        values["g_type"] = self.get_g_type()

        l = ", ".join(("%s=%r" % (k, v) for (k, v) in sorted(values.items())))
        return "<%s %s>" % (self._type_.__name__, l)

_methods = [
    ("get_type_name", gchar_p, [GIRegisteredTypeInfoPtr]),
    ("get_type_init", gchar_p, [GIRegisteredTypeInfoPtr]),
    ("get_g_type", GType, [GIRegisteredTypeInfoPtr]),
]

wrap_class(_gir, GIRegisteredTypeInfo, GIRegisteredTypeInfoPtr,
           "g_registered_type_info_", _methods)

__all__ = ["GIRegisteredTypeInfo", "GIRegisteredTypeInfoPtr",
           "gi_is_registered_type_info"]