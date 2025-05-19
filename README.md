# WL-Tech-FPV-CAR
Replacement for the WL Tech FPV CAR App for the WLtoys 6401 Mini RC Cars 1:64

# xbox_gamepad_vlc_deadzone.py:

Python file for using the left Analogstick of a Xbox Controller (One/Series) as an input to drive a WLtoys 6401 Mini RC Car that is connected via WiFi.

It uses a 6% Deadzone of the Stick to avoid constant Motor noise when the Stick is not exactly centered.

It starts the Videostream of the Camera in VLC for FPV Driving. Only works if VLC is installed on macOS.


To start type this into the terminal:

python xbox_gamepad_vlc_deadzone.py

if this fails try this instead:

python3 xbox_gamepad_vlc_deadzone.py


you may need to install the pygame Library first. To do this type this into the termanial:

pip install pygame

if this fails try this instead:

pip3 install pygame


# xbox_gamepad_proxy_mediamtx_deadzone_browser.py:

If you do not want to use VLC and/or pygame but instead prefer to use a Webbrowser you can start this script.

It depends on mediamtx for converting the rtsp Videostream to WebRTC which you can get here: https://github.com/bluenviron/mediamtx/releases

Just download the mediamtx file and put it in the same directory as the python script.


To start type this into the terminal:

python xbox_gamepad_proxy_mediamtx_deadzone_browser.py

if this fails try this instead:

python3 xbox_gamepad_proxy_mediamtx_deadzone_browser.py

It will start mediamtx automaticly and opens the index.html file in your WebBrowser.


you may need to install the websockets Library first. To do this type this into the termanial:

pip install websockets

if this fails try this instead:

pip3 install websockets


## Some more Informations:

I got the WLtoys 6401 Mini RC Car from Aliexpress: https://www.aliexpress.com/item/1005008669909371.html

I downloaded the WL Tech FPV CAR Android APK File from http://app.eastgallop.com/custom/wl/wl_tech_fpv_car/

Decompiled it to find the URL of the 1280x720 30 fps HEVC h.265 Video-Stream in the source files, which is rtsp://172.16.11.1/live/ch00_1

I used an Android App called Packet Capture to see what Data is transmitted to the RC Car. It was mostly the same Hex-String to the IP 172.16.11.1 Port 23458 via UDP.

Playing with the controlls inside the WL Tech FPV CAR App resulted in figuring out how the Data is structured.

There is a checksum, that is send to the RC Car all the time. I tried to figured out how it is calculated using https://www.scadacore.com/tools/programming-calculators/online-checksum-calculator/ it was not not that hard to understand how it works.

I used ChatGPT to generate the Python Code.
