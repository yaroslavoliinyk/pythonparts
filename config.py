import winreg
import os
import warnings


OLDEST_ALLPLAN_VERSION = 2021
NEWEST_ALLPLAN_VERSION = 2023


warnings.filterwarnings("ignore", category=RuntimeWarning)


def open_key(version):
    registry_path   = rf"SOFTWARE\NEMETSCHEK\Allplan\{version}.0\InstallRoot"
    return winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path)


def get_registry_key():    # This is the location of NemAll Allplan scripts like NemAll_Python_Geometry, etc. 
    version = NEWEST_ALLPLAN_VERSION
    v = os.environ.get("ALLPLAN_PYTHOPARTS_API")    # If user did not create specific env var, then use default 2022 version
    if v is not None and v.isdigit():
        version = v
    version     = int(version)

    while version >= OLDEST_ALLPLAN_VERSION:
        try:
            registry_key = open_key(version)
            return registry_key
        except FileNotFoundError:
            version -= 1

    raise FileNotFoundError(f"No Allplan found on PC from version {OLDEST_ALLPLAN_VERSION} to version {NEWEST_ALLPLAN_VERSION}. Please install Allplan.")


def path_allplan_pp_api():               
    registry_key    = get_registry_key() 
    drive, _        = winreg.QueryValueEx(registry_key, "ProgramDrive")
    lib_path, _     = winreg.QueryValueEx(registry_key, "ProgramPath")
    return drive + lib_path


def path_pp_framework():
    registry_key        = get_registry_key()
    drive, _            = winreg.QueryValueEx(registry_key, "ProgramDataDrive")
    etc_path, _         = winreg.QueryValueEx(registry_key, "ProgramDataPath")
    return drive + etc_path + r"\Etc\PythonPartsFramework"


def path_pp_framework_general_sctips():
    return path_pp_framework() + r"\GeneralScripts"
