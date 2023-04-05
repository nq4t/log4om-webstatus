# LOG4OM Web Statuts
# Version: 5-APR-2023 - Jay Moore/NQ4T
# https://git.pickmy.org/nq4t/log4om-webstatus
# https://nq4t.com/software/log4omudp/
# FreeBSD 3-Clause License (see LICENSE)

import time
import xml.etree.ElementTree as ET
import socket
import select

UDP_IP = "0.0.0.0"
UDP_PORT = 2242 # Default Log4OM UDP Out Port
UDP_C_IP = "192.168.1.70" # Set to IP running Log4OM
UDP_C_PORT = 2241

tot = 1

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

check = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def checkrig():
    check = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    check.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    check.bind((UDP_IP, UDP_C_PORT))
    msg = """<?xml version="1.0" encoding="utf-8"?>
    <RemoteControlRequest>
    <MessageId>C0FC027F-D09E-49F5-9CA6-33A11E05A053</MessageId>
    <RemoteControlMessage>Alive</RemoteControlMessage>
    </RemoteControlRequest>"""
    check.sendto(msg.encode(), (UDP_C_IP, UDP_C_PORT))
    status = select.select([check], [], [], 2)
    if status[0]:
        writehtml(f"Radio Off", False)
    else:
        writehtml(f"Log4OM Down", False)
    check.close()

def writehtml(rs, t = "true"):
    header = """<html>\n<head>\n<title>FT-1000MP Status</title>
        <meta http-equiv=\"refresh\" content=\"5\">\n</head>\n"""
	# if you use CSS then modify for your stylesheet URI
    css = """<link rel=\"stylesheet\" href=\"poole.css\">
        <link rel=\"stylesheet\" href=\"hyde.css\">
        <link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css?family=PT+Sans:400,400italic,700|Abril+Fatface\">"""
    div = "<body><body class=\"theme-base-0d\"><div class=\"sidebar\"><div class=\"sidebar-about\">"
    footer = "\n</div></div></body>\n</html>"
    isonair = "ON THE AIR<br>\n"
    with open("/var/www/log/radio.html", "w") as html: # Modifiy file location as needed.
        if t == True: # Checks for on-air
             html.write(header + css + div + isonair + rs + footer) # If not using CSS, remove it.
        else:
             html.write(header + css + div + rs + footer)

while True:
    ready = select.select([sock], [], [], 6) # Just give it an extra second
    if ready[0]:
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
        time.sleep(.1)
    else:
        sleepy = time.time() - tot
        if sleepy > 60: # How often to check in Off/Down state
             checkrig()
             tot = time.time()
