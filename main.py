import math, paramiko, datetime, locale, yaml, os, sys, requests, pytz
from time import strftime
from dateutil import tz
from datetime import datetime, timedelta, timezone, time
import datetime
from ics import *
import urllib.request
import time as t

yaml.warnings({'YAMLLoadWarning': False})

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')

# Laddar credentials
conf = yaml.load(open("credentials.yml"))

statusCal = "Schemat är tomt"
statusDay = "Schemat är tomt"

### HTML och CSS - Variabler för skapande av index.html och style.css ###

indexHTML1 = '<html>\n<head>\n<meta charset="utf-8">\n<title>Makerspace - Ledigt eller Upptaget?</title>\n<meta name="description" content="Makerspace - Ledigt eller Upptaget?">\n<meta name="author" content="Micke Kring">\n<meta http-equiv="cache-control" content="no-cache, must-revalidate, post-check=0, pre-check=0" />\n<meta http-equiv="cache-control" content="max-age=0" />\n<meta http-equiv="expires" content="0" />\n<meta http-equiv="expires" content="Tue, 01 Jan 1980 1:00:00 GMT" />\n<meta http-equiv="pragma" content="no-cache" />\n<meta http-equiv="refresh" content="15" />'
indexHTML2 = '\n<link rel="stylesheet" type="text/css" href="style.css">\n<link rel="stylesheet" type="text/css" href="style_bg.css">\n<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.3.1/css/all.css" integrity="sha384-mzrmE5qonljUremFsqc01SB46JvROS7bZs3IO2EmfFsd15uHvIt+Y8vEf7N7fWAU" crossorigin="anonymous">\n</head>\n'
indexHTML3 = '<body>\n<div class="list-row">\n<div class="list-left">'
indexHTML4 = '\n<div class="info"><h4><i class="far fa-envelope"></i> Boka rummet | micke.kring@stockholm.se</h4><h4><i class="far fa-envelope"></i> Felanmälan helpdesk | helpdesk@arstaskolan.se</h4></div>\n</div>\n<div class="list-right">'
indexHTML5 = '</div>\n</div>\n</body>\n</html>'

roomStatus = 'nada'
roomTemp = 'nada'

### Klocka och tid - på skärm + 90 sekunder ###

def klockan():
	global klNu
	tid0 = t.time()
	tid1 = tid0 + 90
	klNu = (t.strftime("%H:%M",t.localtime(tid1)))

### Kollar om tid är mellan två klockslag

def is_time_between(begin_clock, end_clock, check_time=None):
	check_time = check_time or datetime.now().time()
	if begin_clock < end_clock:
		return check_time >= begin_clock and check_time <= end_clock
	else:
		return check_time >= begin_clock or check_time <= end_clock

### HTML och CSS vid upptaget, välkommen och ingen inne ###

def upptaget():
	global roomStatus
	global available
	available = "u"
	with open("error_log.csv", "a") as error_log:
		error_log.write("\n{0},Log,Status - Lektion pågår".format(strftime("%Y-%m-%d %H:%M:%S")))
	roomStatus = ('<h1>B213 | MAKERSPACE</h1><br /><p><i class="far fa-calendar-alt" aria-hidden="true"></i> Schema</p><br /><h5><table style="width:100%">' + statusDay + '</table></h5></p>')
	css = ('body{background-color: #d63535;}')
	curStatus = '<h1><i class="far fa-clock" aria-hidden="true"></i> ' + klNu + '</h1><br /><p class="bold">LEKTION PÅGÅR</p><h6>Salen är nu upptagen och aktivitet pågår.</h6><br /><br /><p>' + str(statusCal) + '</p>'

	with open("style_bg.css", "w") as f1, open("index2.html", "w") as f2:
		f1.write(css)
		f2.write(indexHTML1 + indexHTML2 + indexHTML3 + roomStatus + indexHTML4 + curStatus + indexHTML5)
	fileupload()

def valkommen():
	global roomStatus
	global available
	available = "v"

	with open("error_log.csv", "a") as error_log:
		error_log.write("\n{0},Log,Status - Ledigt".format(strftime("%Y-%m-%d %H:%M:%S")))
	roomStatus = ('<h1>B213 | MAKERSPACE</h1><br /><p><i class="far fa-calendar-alt" aria-hidden="true"></i> Schema</p><br /><h5><table style="width:100%">' + statusDay + '</table></h5></p>')
	css = ('body{background-color: #52a530;}')
	curStatus = '<h1><i class="far fa-clock" aria-hidden="true"></i> ' + klNu + '</h1><br /><p class="bold">LEDIG</p><h6>Salen är just nu obokad och ledig att användas.</h6><br /><br /><p>' + str(statusCal) + '</p>'

	with open("style_bg.css", "w") as f1, open("index2.html", "w") as f2:
		f1.write(css)
		f2.write(indexHTML1 + indexHTML2 + indexHTML3 + roomStatus + indexHTML4 + curStatus + indexHTML5)
	fileupload()

def fileupload(): # Här laddar vi upp filerna som har med välkommen, upptaget och ingen inne att göra
	try:
		host = conf['user']['host']
		port = conf['user']['port']
		transport = paramiko.Transport((host, port))

		password = conf['user']['password']
		username = conf['user']['username']
		transport.connect(username = username, password = password)

		sftp = paramiko.SFTPClient.from_transport(transport)

		sftp.chdir("/var/www/bloggmu/public/rum/b213/")
		filepath = "index2.html"
		localpath = "/home/pi/kod/makerspace/index2.html"
		filepath2 = "style.css"
		localpath2 = "/home/pi/kod/makerspace/style.css"
		filepath3 = "style_bg.css"
		localpath3 = "/home/pi/kod/makerspace/style_bg.css"

		sftp.put(localpath, filepath)
		sftp.put(localpath2, filepath2)
		sftp.put(localpath3, filepath3)

		sftp.close()
		transport.close()
		with open("error_log.csv", "a") as error_log:
			error_log.write("\n{0},Log,Filer - status - uppladdade".format(strftime("%Y-%m-%d %H:%M:%S")))
		print("Filerna har laddats upp.")
	except:
		print("Error. Filerna kunde inte laddas upp.")
		with open("error_log.csv", "a") as error_log:
			error_log.write("\n{0},Error,Filer - status - kunde inte ladda upp".format(strftime("%Y-%m-%d %H:%M:%S")))
		pass

def indexupload(): # Här laddar vi upp alla initiala filer som behövs som inte uppdateras under körning.
	try:
		host = conf['user']['host']
		port = conf['user']['port']
		transport = paramiko.Transport((host, port))

		password = conf['user']['password']
		username = conf['user']['username']
		transport.connect(username = username, password = password)

		sftp = paramiko.SFTPClient.from_transport(transport)

		sftp.chdir("/var/www/bloggmu/public/rum/b213/")
		filepath5 = "index2.html"
		localpath5 = "/home/pi/kod/makerspace/index2.html"
		filepath6 = "style.css"
		localpath6 = "/home/pi/kod/makerspace/style.css"
		filepath7 = "user_pic.jpg"
		localpath7 = "/home/pi/kod/makerspace/user_pic.jpg"
		filepath8 = "style_bg.css"
		localpath8 = "/home/pi/kod/makerspace/style_bg.css"
		filepath9 = "index.html"
		localpath9 = "/home/pi/kod/makerspace/index.html"

		sftp.put(localpath5, filepath5)
		sftp.put(localpath6, filepath6)
		sftp.put(localpath7, filepath7)
		sftp.put(localpath8, filepath8)
		sftp.put(localpath9, filepath9)

		sftp.close()
		transport.close()
		with open("error_log.csv", "a") as error_log:
			error_log.write("\n{0},Log,Filer - initiala - uppladdade".format(strftime("%Y-%m-%d %H:%M:%S")))
	except:
		print("Error. Filerna kunde inte laddas upp.")
		with open("error_log.csv", "a") as error_log:
			error_log.write("\n{0},Error,Filer - initiala - kunde inte laddas upp".format(strftime("%Y-%m-%d %H:%M:%S")))
		pass

def Calendar():
	global statusCal
	global statusDay
	#global override
	global available
	global activity_now
	klockan()

	url = conf['urlcalendar']['link_url']

	try:
		with urllib.request.urlopen(url) as response:
			ics_string = response.read()
		
		### RIGHT NOW ###

		window_start = datetime.now(timezone.utc)
		window_end = window_start + timedelta(minutes=1)
		events = get_events_from_ics(ics_string, window_start, window_end)

		for e in events:
			activity_now = ('{}'.format(e['summary']))
			start = (e['startdt'])
			start_date = (start.strftime("%Y-%m-%d"))
			start_time_h = (start.strftime("%H"))
			start_time_hour = (int(start_time_h) + 2)
			start_time_min = (start.strftime("%M"))
			end = (e['enddt'])
			end_date = (end.strftime("%Y-%m-%d"))
			end_time_h = (end.strftime("%H"))
			end_time_hour = (int(end_time_h) + 2)
			end_time_min = (end.strftime("%M"))

			start_time_tot = (str(start_time_hour) + ":" + str(start_time_min))
			end_time_tot = (str(end_time_hour) + ":" + str(end_time_min))

		try:
			statusCal = ((start_time_tot) + " - " + (end_time_tot) + " | " + (activity_now))
			print(statusCal)
			
			if "   " not in activity_now.lower():
				print("UPPTAGET")
				upptaget()

			else:
				print("LEDIGT")
				statusCal = ("")
				valkommen()

		except:
			statusCal = ("")
			valkommen()
			print(statusCal)

		### LIST DAY ###

		window_start = datetime.now(timezone.utc)
		window_end = window_start + timedelta(hours=10)
		events = get_events_from_ics(ics_string, window_start, window_end)

		listDay = []

		for e in events:
			activity_day = ('{}'.format(e['summary']))
			start = (e['startdt'])
			start_date_day = (start.strftime("%a"))
			start_time_day = (start.strftime("%H:%M"))
			start_time_h = (start.strftime("%H"))
			start_time_hour = (int(start_time_h) + 2)
			start_time_min = (start.strftime("%M"))

			end = (e['enddt'])
			end_date = (end.strftime("%Y-%m-%d"))
			end_time_h = (end.strftime("%H"))
			end_time_hour = (int(end_time_h) + 2)
			end_time_min = (end.strftime("%M"))

			start_time_tot = (str(start_time_hour) + ":" + str(start_time_min))
			end_time_tot = (str(end_time_hour) + ":" + str(end_time_min))

			listDay.append('<tr><th class="first">' + (start_date_day.capitalize()) + '</th><th class="second">' + (start_time_tot) + " - " + (end_time_tot) + '</th><th class="third">' + (activity_day) + '</th></tr>')
		
		statusDay = ("".join(listDay))

		print(statusDay)

	except:
		print("Kunde inte hämta kalender")
		with open("error_log.csv", "a") as error_log:
			error_log.write("\n{0},Error,Kunde inte hämta kalender".format(strftime("%Y-%m-%d %H:%M:%S")))
		pass

def Main():

	try:
		button_delay = 0.2
		
		print("\n Startar och laddar upp initiala filer...")
		
		indexupload() # Laddar upp alla filer som initialt behövs, i fall lokala ändringar gjorts
		
		print("\nReady player one")

		while True:
			Calendar()
			t.sleep(30)
			fileupload()
	
	finally: # Om programmet avslutas rensas GPIO
		print("End game...")

### MAIN PROGRAM ###

if __name__ == "__main__":
	Main()