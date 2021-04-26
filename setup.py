import sys
import os
from platform_d import get_platform

try:
    import pip
except ImportError:
    print("No pip found!")
    try:
        import urllib.request as req
        req.urlretrieve("https://bootstrap.pypa.io/get-pip.py", "get-pip.py")
        os.system("python get-pip.py")
    except ImportError:
        print("URL Lib not found. Please download pip file from the url: "
              "https://bootstrap.pypa.io/get-pip.py")
        sys.exit(0)
    except Exception:
        print("ERROR. Try running this file as administrator")
        sys.exit(0)

p_wx = "wxPython"
p_win32gui = "pywin32"
try:
    __import__("wx")
except ImportError:
    os.system("pip install %s" % p_wx)
    try:
        __import__("wx")
    except ImportError:
        print("Please Install wxPython package. Try running the command: pip install wxPython")
        sys.exit(0)

try:
    __import__("win32gui")
except ImportError:
    os.system("pip install %s" % p_win32gui)
    try:
        __import__("win32gui")
    except ImportError:
        print("Please Install pywin32 package. Try running the command: pip install pywin32")
        sys.exit(0)

try:
    if get_platform() == 'Windows':
        def set_batch():
            import getpass
            user_name = getpass.getuser()
            file_path = os.path.dirname(os.path.realpath(__file__)) + "\\logger.py"
            bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\
            Startup' % user_name
            with open(bat_path + '\\' + "logger.cmd", "w+") as bat_file:
                bat_file.write(r'python "%s" ' % file_path)

        def set_registry():
            import winreg as reg
            os_path = os.path.dirname(os.path.realpath(__file__))
            f_name = os.path.join(os_path, "logger.py")
            open_key = reg.OpenKey(reg.HKEY_CURRENT_USER,
                                   "Software\\Microsoft\\Windows\\CurrentVersion"
                                   "\\Run",
                                   0, reg.KEY_ALL_ACCESS)
            reg.SetValueEx(open_key, "python_logger", 0, reg.REG_SZ, f_name)
            reg.CloseKey(open_key)

        set_batch()

except Exception as excp:
    print("Couldnt set the registry keys. Kindly see how to run how to set registry "
          "keys to run scripts")
    print(str(excp))
    sys.exit(0)

