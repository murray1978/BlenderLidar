#__init__.py

bl_info = {
    "name": "3D Scanner Importer",
    "author": "Murray Smith",
    "version": (0, 0, 1),
    "blender": (2, 81, 6),
    "location": "File > Import-Export",
    "description": "Import point data from serial lidar unit",
    "warning": "expects 0xFA, Angle(((low,high) + 0xA0) / 4), RPM(low,high), distance(low,high)",
    "doc_url": "{BLENDER_MANUAL_URL}/addons/lidar/lidar.html",
    "support": '',
    "category": "",
}

import bpy

from bpy_extras.io_utils import (
        orientation_helper,
        axis_conversion,
        )
from bpy.props import (
        BoolProperty,
        FloatProperty,
        StringProperty,
        EnumProperty,
        )

#if "bpy" in locals():
#    import importlib
#    if "import_obj" in locals():
#        importlib.reload(import_obj)
#    if "export_obj" in locals():
#        importlib.reload(export_obj)

@orientation_helper(axis_forward='-Z', axis_up='Y') #change to suit lidar