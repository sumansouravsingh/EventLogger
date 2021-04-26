import csv
import os
import sys
import time
import datetime
import threading

LogFile = os.path.realpath(__file__)+'logs\\log_' + time.strftime("%Y-%b-%d", time.localtime())
LogFile = LogFile.replace("\\get-contents.py", "\\")
Data = {}
file_count = 0
time_current = datetime.datetime.now()
old_cnt = 0
file_list = set()
dir_list = set()


def init_app():
    global file_count
    global time_current
    global old_cnt
    cnt = 0
    path = "C:\\PyCharmProject\\EventLogger"
    check_all_dir(path)
    if not os.path.exists(LogFile + ".csv"):
        Data["Column1"] = "TOTAL FILES"
        Data["Time Taken"] = "TIME TAKEN"
        write(Data, LogFile)
    Data.clear()
    while True:
        get_files(path)
        print(file_count)
        while old_cnt == file_count:
            time.sleep(5)
            get_files(path)
            cnt += 1
            if cnt > 5:
                sys.exit(0)
        cnt = 0
        old_cnt = file_count
        seconds = (datetime.datetime.now() - time_current)
        Data["File"] = file_count
        Data["time"] = seconds.microseconds
        time.sleep(5)
        write(Data, LogFile)
        Data.clear()


def get_files(path):
    check_all_dir(path)
    for directory in dir_list:
        t = threading.Thread(target=parse_dir, args=(directory,))
        t.start()
        t.join()


def check_all_dir(path):
    dir_list.add(path)
    for item in os.listdir(path):
        it = path+"\\"+item
        if (not os.path.isfile(it)) and it not in dir_list:
            dir_list.add(it)
            check_all_dir(it)


def parse_dir(path):
    global file_list
    global file_count

    for item in os.listdir(path):
        it = path+"\\"+item
        if os.path.isfile(it):
            if it not in file_list:
                file_count += 1
                file_list.add(it)
        else:
            parse_dir(it)


def write(data, logfile):
    logfile = logfile + '.csv'
    if "Idle" in data:
        del data["Idle"]
    try:
        f_output = open(logfile, 'a')
        output = csv.writer(f_output)
        output.writerow(data.values())
        f_output.close()
    except IOError as io:
        print(io)
    except Exception as excp:
        print(excp)


if __name__ == "__main__":
    init_app()
    print(os.path.isfile("C:\\PyCharmProject\\EventLogger\\.idea\\EventLogger.iml"))