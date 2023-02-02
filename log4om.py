from threading import *
import time
import xml.etree.ElementTree as ET
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 2242 # Default Log4OM UDP Out Port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
tot = time.time()


def monitor():
        global tot
        while True:
                tc = time.time() - tot # time since last timestamp
                if tc < 15: #15 seconds
                        time.sleep(6)
                else:
                        writehtml(f"Radio Off or Log4OM Not Running", False) #writehtml() requires two arguements and you can't be on air if radio is off
                        time.sleep(30) # Slow checks when radio off/no UDP

def log4om():
        global tot
        while True:
                data, addr = sock.recvfrom(1024)
                root = ET.fromstring(data.decode("utf-8"))
                freq = int(root.find("Freq").text)
                tx_freq = int(root.find("TXFreq").text)
                mode = root.find("Mode").text
                onair = (root.find("IsTransmitting").text == "true")
                f = freq / 100
                tf = tx_freq / 100
                sv = tf - f # Determines split value
                if sv > 0:
                    writehtml(f"Frequency: {f}kHz {mode}<br>Tx Split &middot; Up: {sv:.2f} kHz", onair)
                elif sv < 0:
                    sv = sv * -1 # Invert negative numbers
                    writehtml(f"Frequency: {f}kHz {mode}<br>Tx Split &middot; Down: {sv:.2f} kHz", onair)
                else:
                    writehtml(f"Frequency: {f}kHz {mode}", onair)
                tot = time.time() #timestamp
                time.sleep(.1)

def writehtml(rs, t = "true"):
    header = "<html>\n<head>\n<title>FT-1000MP Status</title>\n<meta http-equiv=\"refresh\" content=\"5\">\n</head>\n" # Basic Header
    #css = "<link rel=\"stylesheet\" href=\"poole.css\">\n<link rel=\"stylesheet\" href=\"hyde.css\">\n<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css?family=PT+Sans:400,400italic,700|Abril+Fatface\">" # This adds my CSS files.
    #div = "<body><body class=\"theme-base-0d\"><div class=\"sidebar\"><div class=\"sidebar-about\">" # This is additional formatting
    footer = "\n</div></div></body>\n</html>" # footer
    isonair = "ON THE AIR<br>\n" # on-air html
    with open("/var/www/log/radio.html", "w") as html: # Modifiy file location as needed.
        if t == True: # Checks for on-air
             #html.write(header + css + div + isonair + rs + footer) # This will add additional variables (for css, etc.) to the HTML file.
             html.write (header + isonair + rs + footer) # No formatting version
        if t == False: # Checks for on-air
             #html.write(header + css + div + rs + footer) # Same as above without isonair, use if additional html is used
             html.write(header + rs + footer) # No formatting version

T = Thread(target=monitor,daemon=True) # Daemon the monitor thread
L = Thread(target=log4om)

L.start() # Start the UDP thread
time.sleep(5) # Wait 5 seconds in case Log4OM is already running and outputting messages
T.start() # Start monitor thread
