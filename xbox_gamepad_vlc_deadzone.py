import socket
import pygame
import time
import subprocess

# Configuration
UDP_IP = "172.16.11.1"
UDP_PORT = 23458
RTSP_URL = "rtsp://172.16.11.1/live/ch00_1"
DEADZONE = 0.06

# Basepaket (16 Bytes)
base_packet = bytearray.fromhex("ca 47 d5 00 00 00 00 00 66 80 80 80 00 00 80 99")

def map_axis_to_byte(value):
    """Maps Joystick-Axevalue from [-1, 1] to [0, 255]."""
    return int((value + 1) / 2 * 255)

def is_significant_change(value1, value2):
    """Checks, if change is bigger then Deadzone."""
    return abs(value1 - value2) > DEADZONE

# Start RTSP-Stream using VLC
subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC', RTSP_URL])

# Pygame
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    raise RuntimeError("No Joystick found!")

joystick = pygame.joystick.Joystick(0)
joystick.init()

# UDP-Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

last_axis_x = 0.0
last_axis_y = 0.0

try:
    while True:
        pygame.event.pump()

        # read axis
        axis_x = joystick.get_axis(0)  # left-right
        axis_y = joystick.get_axis(1)  # up-down

        if (is_significant_change(axis_x, last_axis_x) or
            is_significant_change(axis_y, last_axis_y)):

            last_axis_x = axis_x
            last_axis_y = axis_y

            byte_9 = map_axis_to_byte(axis_x)
            byte_10 = map_axis_to_byte(-axis_y)  # reversed "up = FF"

            packet = base_packet[:]
            packet[9] = byte_9
            packet[10] = byte_10

            # Byte 15 = XOR from Byte 10, 11, 12 (Index 9, 10, 11)
            packet[14] = packet[9] ^ packet[10] ^ packet[11]

            # send UDP
            sock.sendto(packet, (UDP_IP, UDP_PORT))

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Closed by User.")
finally:
    pygame.quit()
