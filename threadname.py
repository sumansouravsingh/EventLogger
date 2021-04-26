import psutil #http://code.google.com/p/psutil/wiki/Documentation#Classes
from win32process import GetWindowThreadProcessId


def get_threadname(HWND):

    try:
        pprocess = GetWindowThreadProcessId(HWND)
        p = psutil.Process(pprocess[1])
    except Exception as ecp:
        return None
    return p
