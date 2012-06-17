# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import POINTER

from glib import *
from gibaseinfo import *
from gipropertyinfo import *
from gicallableinfo import *
from giconstantinfo import *
from gistructinfo import *
from _util import load, wrap_class

_gir = load("girepository-1.0")


def gi_is_interface_info(base_info):
    return base_info.get_type().value == GIInfoType.INTERFACE


class GIInterfaceInfo(GIBaseInfo):
    pass


class GIInterfaceInfoPtr(POINTER(GIInterfaceInfo)):
    _type_ = GIInterfaceInfo

    def __repr__(self):
        values = {}
        values["n_constants"] = self.get_n_constants()
        values["n_signals"] = self.get_n_signals()
        values["n_methods"] = self.get_n_methods()
        values["n_properties"] = self.get_n_properties()
        values["n_prerequisites"] = self.get_n_prerequisites()

        l = ", ".join(("%s=%r" % (k, v) for (k, v) in sorted(values.items())))
        return "<%s %s>" % (self._type_.__name__, l)

_methods = [
    ("get_n_prerequisites", gint, [GIInterfaceInfoPtr]),
    ("get_prerequisite", GIBaseInfoPtr, [GIInterfaceInfoPtr, gint]),
    ("get_n_properties", gint, [GIInterfaceInfoPtr]),
    ("get_property", GIPropertyInfoPtr, [GIInterfaceInfoPtr, gint]),
    ("get_n_methods", gint, [GIInterfaceInfoPtr]),
    ("get_method", GIFunctionInfoPtr, [GIInterfaceInfoPtr, gint]),
    ("find_method", GIFunctionInfoPtr, [GIInterfaceInfoPtr, gchar_p]),
    ("get_n_signals", gint, [GIInterfaceInfoPtr]),
    ("get_signal", GISignalInfoPtr, [GIInterfaceInfoPtr, gint]),
    ("get_n_vfuncs", gint, [GIInterfaceInfoPtr]),
    ("get_vfunc", GIVFuncInfoPtr, [GIInterfaceInfoPtr, gint]),
    ("get_n_constants", gint, [GIInterfaceInfoPtr]),
    ("get_constant", GIConstantInfoPtr, [GIInterfaceInfoPtr, gint]),
    ("get_iface_struct", GIStructInfoPtr, [GIInterfaceInfoPtr]),
    ("find_vfunc", GIVFuncInfoPtr, [GIInterfaceInfoPtr, gchar_p]),
]

wrap_class(_gir, GIInterfaceInfo, GIInterfaceInfoPtr,
           "g_interface_info_", _methods)

__all__ = ["GIInterfaceInfo", "GIInterfaceInfoPtr", "gi_is_interface_info"]