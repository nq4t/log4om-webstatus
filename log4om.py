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
                if tc < 15: # 15 seconds
                        time.sleep(6)
                else:
                        writehtml(f"Radio off")
                        time.sleep(30)

def log4om():
        global tot
        global rstatus
        while True:
                data, addr = sock.recvfrom(1024)
                root = ET.fromstring(data.decode("utf-8"))
                freq = int(root.find("Freq").text)
                tx_freq = int(root.find("TXFreq").text)
                mode = root.find("Mode").text
                f = freq / 100
                tf = tx_freq / 100
                sv = tf - f # Determines split value
                if sv > 0:
                    writehtml(f"Frequency: {f}kHz {mode}<br>Up: {sv:.2f} kHz")
                elif sv < 0:
                    sv = sv * -1 # Invert negative numbers
                    writehtml(f"Frequency: {f}kHz {mode}<br>Down: {sv:.2f} kHz")
                else:
                    writehtml(f"Frequency: {f}kHz {mode}")
                tot = time.time() #timestamp
                time.sleep(.1)

def writehtml(rs):
    header = "<html>\n<head>\n<title>FT-1000MP Status</title>\n<meta http-equiv=\"refresh\" content=\"5\">\n</head>\n<body>\n"
    with open("/var/www/log/radio.html", "w") as html: # Modify file location as needed.
        html.write(header + rs + "\n</body>\n</html>")

T = Thread(target=monitor,daemon=True)
L = Thread(target=log4om)

L.start() # Start the UDP thread
time.sleep(5) # Wait 5 seconds in case Log4OM is already running.
T.start() # Start monitor
