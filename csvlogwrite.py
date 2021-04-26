import csv


def Write(data, logfile):
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

