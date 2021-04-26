import win32api


def get_idle_duration():
    millis = win32api.GetTickCount() - win32api.GetLastInputInfo()
    return millis / 1000.0
