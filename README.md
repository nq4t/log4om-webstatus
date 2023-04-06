# Log4OM Web Status

This python program will take UDP messages blasted at it from Log4OM and will write it to a HTML file. It will
continually update this file as messages come in. It requires you to let Log4OM automatically send status packets.

## Usage

Place the script on a system that can hear UDP from Log4OM and has a way of putting the resulting HTML file on a webserver
as fast as possible. Edit the script as required (IP, port, output location, HTML formatting).

## Basic Operation

Log4OM has a feature that has it send out UDP messages automatically as long as specific conditions are met. This python
script/program will take in the messages sent at it's IP and parse a few things out of the XML. It writes this to an
HTML file every time a message comes in; so the HTML generated is set to auto-reload every 5 seconds. It currently displays
the following in a very basic way:

- Your current VFO frequency and opearating mode.
- Your TX offset/split if it exists
- If your radio is off or Log4OM is not loaded

This now will determine if the radio is off or if Log4OM is not loaded by trying to request the Alive command over remote
control. It will assue Log4OM is active if a response is received. In an effort to make the thing a bit less chatty, it 
backs down to 60 second checks when not receiving data automatically. 

Code could likely use more optimization. ChatGPT has been used to some degree but currently has issues giving complete 
output. 

## Examples

This has been implemented on the sidebar/menu of [nq4t.com](https://nq4t.com). The actual webpage that's updated is served
from my [QTH's webserver](https://log.nq4t.com/radio.html).

## History

```
02-FEB-2023: Initial Version. Shows status and basic offline message.
04-APR-2023: Second Version. Now shows more percise offline message. Removes threads.
```

## License

```
BSD 3-Clause License

Copyright (c) 2023, Jay Moore

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
