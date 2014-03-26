# Copyright 2012-2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi.clib.gir import GITypeTag
from pgi.clib.glib import GErrorPtr
from pgi.clib.gobject import GType
from pgi.gerror import PGError
from pgi.gtype import PGType

from .utils import BaseType, register_type


@register_type(GITypeTag.GTYPE)
class GType_(BaseType):

    def check(self, name):
        gtype_map = {
            str: "gchararray",
            int: "gint",
            float: "gdouble",
            bool: "gboolean",
        }

        items = gtype_map.items()
        gtype_map = dict((k, PGType.from_name(v)) for (k, v) in items)

        var = self.parse("""
if not $_.isinstance($obj, $PGType):
    if hasattr($obj, "__gtype__"):
        $obj = $obj.__gtype__
    elif $obj in $gtype_map:
        $obj = $gtype_map[$obj]

if not $_.isinstance($obj, $PGType):
    raise TypeError("%r not a GType" % $obj)
""", gtype_map=gtype_map, obj=name, PGType=PGType)

        return var["obj"]

    def pack(self, name):
        var = self.parse("""
$gtype = $GType($obj._type.value)
""", obj=name, GType=GType)

        return var["gtype"]

    pack_in = pack

    def pre_unpack(self, name):
        return name

    def unpack(self, name):
        var = self.parse("""
$pgtype = $PGType($gtype)
""", gtype=name, PGType=PGType)

        return var["pgtype"]

    def new(self):
        var = self.parse("""
$gtype = $GType()
""", GType=GType)

        return var["gtype"]


@register_type(GITypeTag.ERROR)
class Error(BaseType):

    def unpack(self, name):
        var = self.parse("""
if $gerror_ptr:
    $out = $PGError($gerror_ptr.contents)
else:
    $out = $none
""", gerror_ptr=name, PGError=PGError, none=None)

        return var["out"]

    def check_raise(self, name):
        self.parse("""
if $error:
    raise $error
""", error=name)

    def new(self):
        return self.parse("""
$ptr = $gerror_ptr()
""", gerror_ptr=GErrorPtr)["ptr"]

    def free(self, name):
        self.parse("""
if $ptr:
    $ptr.free()
""", ptr=name)