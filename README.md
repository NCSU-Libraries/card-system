# Card System
Regulates access to DH Hill Library Makerspace, restricted to NC State University students, faculty and staff with campus ID cards. 

This repository includes Python code running on the system as well as electrical and mechanical design files.

## System Overview
![System block diagram]
(/system-block-diagram.png)

The system comprises a Raspberry Pi with touchscreen, magnetic stripe card readers, a laser-cut enclosure produced in-house, a circuit board produced in-house, and associated electronics. It interacts with a web API (also produced in the Library) to authenticate users. The Pi runs a modified version of Raspbian Linux provided by Adafruit for use with their PiTFT touchscreens.

Users sign into the space by swiping their campus ID card on the entry card reader. The system accesses a database of users with the SpaceAuth API to check for the user's access privileges. If the user has access, they are greeted with a green light and an "access granted" from the speaker; otherwise, a red light and "access denied". The system also has a motion sensor (PIR) which, when triggered, triggers the system to deny access.

## Bill of Materials
| Item  | Quantity  | Link  |
| ----- | --------- | ----- |
Raspberry Pi 2 Model B | 1 | https://www.raspberrypi.org/products/raspberry-pi-2-model-b/
PiTFT Plus 3.5" 480x320 | 1 | https://www.adafruit.com/products/2441
Assorted Terminal Blocks | - | https://www.adafruit.com/products/2234
ID TECH MiniMag Duo IDMB-354133B | 2 | http://idtechproducts.com/products/swipe-reader-writers/minimag-ii-compact-intelligent-magstripe-reader
Panel Monunt USB Port | 3 | https://www.adafruit.com/product/908
Panel Mount Ethernet Port | 1 | https://www.adafruit.com/products/909
Panel Mount 2.1mm Barrel Jack | 1 | https://www.adafruit.com/products/610
PIR Sensor | 1 | https://www.adafruit.com/products/189
330R Resistors | 2 | https://www.sparkfun.com/products/11507
10mm Green LED | 1 | https://www.sparkfun.com/products/10633
10mm Red LED | 1 | https://www.sparkfun.com/products/10632
3" 8 Ohm Speaker | 1 | https://www.adafruit.com/products/1313
3.5mm Stereo Plug | 1 | https://www.adafruit.com/products/1700
Mono Amplifier | 1 | https://www.sparkfun.com/products/11044
10K Logarithmic Potentiometer | 1 | https://www.sparkfun.com/products/9940
Male Machine Pin Headers | 1 | https://www.sparkfun.com/products/117
Female Machine Pin Headers | 1 | https://www.sparkfun.com/products/743
2x13 shrouded header | 1 | https://www.sparkfun.com/products/retired/11490
6-wire Ribbon Cable | 1 | https://www.sparkfun.com/products/10651
2x6 Crimp connector | 2 | https://www.sparkfun.com/products/10651
2x6 Shrouded Header | 1 | https://www.sparkfun.com/products/10877


## Author
Aaron Arthur, adarthur@ncsu.edu

## Project Collaborators
Bret Davidson  (author of Space Auth API)
Adam Rogers (project requirements + management)
Jack Twiddy (PCB and enclosure fabrication)
Augustus Vieweg (code contribution)

## LICENSE
MIT License
