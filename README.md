# Log4OM Web Status

This python program will take UDP messages blasted at it from Log4OM and will write it to a HTML file. It will
continually update this file as messages come in. It requires you to let Log4OM automatically send status packets.

### Usage

Place the script on a system that can hear UDP from Log4OM and has a way of putting the resulting HTML file on a webserver
as fast as possible. Edit the script as required (IP, port, output location, HTML formatting).

### Basic Operation

Log4OM has a feature that has it send out UDP messages automatically as long as specific conditions are met. This python
script/program will take in the messages sent at it's IP and parse a few things out of the XML. It writes this to an
HTML file every time a message comes in; so the HTML generated is set to auto-reload every 5 seconds. It currently displays
the following in a very basic way:

- Your current VFO frequency and opearating mode.
- Your TX offset/split if it exists

If no data is received from Log4OM, because you turned your rig off or shutdown Log4OM; it will indicate your radio is
off and wait for data to come back. Support is planned to show if rig is in transmit. 

The "Radio Off" message happens after 15 seconds of no data. This is done by checking the elapsed time since the timestamo
was last updated; which happens every time a message comes in.

The script contains examples of how to add additional portions of HTML. This was done for nq4t.com. They are commented out by
default. You will need to modify this as you require.
