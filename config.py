
import os
import warnings


OLDEST_ALLPLAN_VERSION = 2021
NEWEST_ALLPLAN_VERSION = 2023


try:
    import winreg
    warnings.filterwarnings("ignore", category=RuntimeWarning)


    def open_key(version):
        """
        The function `open_key` opens a specific registry key based on the given version number.
        
        :param version: The `version` parameter is a string that represents the version number of the
        software. It is used to construct the registry path to the installation root of the software
        :return: a key object that represents a specific registry key in the Windows registry.
        """
        registry_path   = rf"SOFTWARE\NEMETSCHEK\Allplan\{version}.0\InstallRoot"
        return winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path)


    def get_registry_key():    # This is the location of NemAll Allplan scripts like NemAll_Python_Geometry, etc. 
        """
        The function `get_registry_key()` retrieves the registry key for the installed version of Allplan on
        a PC, starting from the newest version and going back to the oldest version.
        :return: the registry key for the specified version of Allplan.
        """
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
        """
        The function `path_allplan_pp_api` returns the path to the Allplan PP API library.
        :return: the path to the Allplan PP API library.
        """
        registry_key    = get_registry_key() 
        drive, _        = winreg.QueryValueEx(registry_key, "ProgramDrive")
        lib_path, _     = winreg.QueryValueEx(registry_key, "ProgramPath")
        return drive + lib_path


    def path_pp_framework():
        """
        The function `path_pp_framework()` returns the path to the Python Parts Framework folder.
        :return: the path to the Python Parts Framework directory.
        """
        registry_key        = get_registry_key()
        drive, _            = winreg.QueryValueEx(registry_key, "ProgramDataDrive")
        etc_path, _         = winreg.QueryValueEx(registry_key, "ProgramDataPath")
        return drive + etc_path + r"\Etc\PythonPartsFramework"


    def path_pp_framework_general_sctips():
        """
        The function returns the path to the "GeneralScripts" folder within the "pp_framework" folder.
        :return: The function `path_pp_framework_general_sctips()` is returning the path to the
        "GeneralScripts" folder within the "pp_framework" directory.
        """
        return path_pp_framework() + r"\GeneralScripts"
except Exception:
    print('unix-base system')