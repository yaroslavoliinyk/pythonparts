import os
import sys
import winreg


def access_allplan_pp_api(version=2022):    # This is the location of NemAll Allplan scripts like NemAll_Python_Geometry, etc.    
    v = os.environ.get("ALLPLAN_PYTHOPARTS_API")
    if v is not None:
        version     = str(int(v))
    else:
        version     = str(int(version))
    registry_path   = rf"SOFTWARE\NEMETSCHEK\Allplan\{version}.0\InstallRoot"
    registry_key    = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path)
    drive, _        = winreg.QueryValueEx(registry_key, "ProgramDrive")
    lib_path, _     = winreg.QueryValueEx(registry_key, "ProgramPath")
    return drive + lib_path


sys.path.append(access_allplan_pp_api())
import NemAll_Python_Geometry as AllplanGeo    # type: ignore
from .src import create_scene, create_cuboid



