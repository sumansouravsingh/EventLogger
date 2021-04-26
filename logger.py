import os
from win32gui import GetWindowText, GetForegroundWindow
from time import strftime, localtime
import idledetect
import threadname
import csvlogwrite as logwrite

Data = {}
LogFile = os.path.realpath(__file__)+'logs\\' + strftime("%Y-%b-%d", localtime())
LogFile = LogFile.replace("\\logger.py", "\\")


def init_app():
	global Data
	Data = {}
	if not os.path.exists(LogFile+".csv"):
		Data["Column1"] = "PROCESS NAME"
		Data["Column2"] = "PROCESS ID"
		Data["Column3"] = "PROCESS CREATION TIME"
		Data["Column4"] = "ACTIVE WINDOW NAME"
		Data["Column5"] = "TOTAL IDLE TIME(seconds)"
		Data["Column6"] = "PROCESS LOG START TIME"
		Data["Column7"] = "PROCESS LOG END TIME"
		logwrite.Write(Data, LogFile)
	refresh()
	while True:
		log_data()
	

def log_data():
	global Data
	idle = idledetect.get_idle_duration()
	if idle > 300:
		old = Data['Idle']
		Data['Idle'] = idle
		Data['TotalIdle'] = Data['TotalIdle'] + Data['Idle'] - old
	else:
		Data['Idle'] = 0

	if GetWindowText(GetForegroundWindow()) and "ActiveWindowText" in Data and (
			Data['ActiveWindowText'] != str(GetWindowText(GetForegroundWindow()))):
		Data['log_end_time'] = strftime("%d %b %Y - %H:%M:%S")
		logwrite.Write(Data, LogFile)
		refresh()


def refresh():
	global Data
	fg_obj = GetForegroundWindow()
	p = threadname.get_threadname(fg_obj)
	if p:
		Data.clear()
		Data['ProcessName'] = str(p.name).split('name=\'')[1].split('.')[0]
		Data['ProcessID'] = p.pid
		Data['ProcessCreationTime'] = strftime("%d %b %Y %H:%M:%S", localtime(p.create_time()))
		Data['ActiveWindowText'] = str(GetWindowText(fg_obj))
		Data['Idle'] = 0
		Data['TotalIdle'] = 0
		Data['log_start_time'] = strftime("%d %b %Y - %H:%M:%S")


if __name__ == "__main__":
	init_app()
