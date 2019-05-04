# Rumskalender

Första uppladdning - fungerar, men behöver snyggas till. :) 

Python 3.X 
Se även __main.py__ och installera de moduler som importeras om du inte har dessa i ditt system

# Vad behöver du ändra
I __credentials.yml__ får du lägga till adressen till din publika googlekalender samt uppgifterna till din SFTP-server.

I __main.py__ får du ändra variablerna __indexHTML1-5__ som skapar webbsidan och dessutom vaiablerna roomStatus i funktionerna __upptaget()__ och __valkommen()__

I __main.py__ i funktionerna __fileUpload()__ och __indexUpload()__ får du ändra sökvägarna till din lokala katalog samt på din server;<br /><br />
		sftp.chdir("/var/www/bloggmu/public/rum/b213/")<br />
		filepath = "index2.html"<br />
		localpath = "/home/pi/kod/makerspace/index2.html"<br />
		filepath2 = "style.css"<br />
		localpath2 = "/home/pi/kod/makerspace/style.css"<br />
		filepath3 = "style_bg.css"<br />
		localpath3 = "/home/pi/kod/makerspace/style_bg.css"<br /><br />

# Credits
Kalenderimportfunktionaliteten är en omarbetning och vidareutveckling av jeinarsson https://gist.github.com/jeinarsson/989329deb6906cae49f6e9f979c46ae7
    

