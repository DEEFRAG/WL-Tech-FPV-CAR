import socket
import pygame
import time
import subprocess

# Konfiguration
UDP_IP = "172.16.11.1"
UDP_PORT = 23458
RTSP_URL = "rtsp://172.16.11.1/live/ch00_1"
DEADZONE = 0.06

# Grundpaket (16 Bytes)
base_packet = bytearray.fromhex("ca 47 d5 00 00 00 00 00 66 80 80 80 00 00 80 99")

def map_axis_to_byte(value):
    """Mappt Joystick-Achsenwert von [-1, 1] auf [0, 255]."""
    return int((value + 1) / 2 * 255)

def is_significant_change(value1, value2):
    """Prüft, ob Änderung größer als Deadzone ist."""
    return abs(value1 - value2) > DEADZONE

# RTSP-Stream per externem VLC starten
subprocess.Popen(['/Applications/VLC.app/Contents/MacOS/VLC', RTSP_URL])

# Pygame initialisieren
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    raise RuntimeError("Kein Joystick gefunden!")

joystick = pygame.joystick.Joystick(0)
joystick.init()

# UDP-Socket vorbereiten
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialwerte speichern
last_axis_x = 0.0
last_axis_y = 0.0

try:
    while True:
        pygame.event.pump()

        # Achsen lesen
        axis_x = joystick.get_axis(0)  # Links–rechts
        axis_y = joystick.get_axis(1)  # Hoch–runter

        if (is_significant_change(axis_x, last_axis_x) or
            is_significant_change(axis_y, last_axis_y)):

            last_axis_x = axis_x
            last_axis_y = axis_y

            byte_9 = map_axis_to_byte(axis_x)
            byte_10 = map_axis_to_byte(-axis_y)  # Umgekehrt für "oben = FF"

            packet = base_packet[:]
            packet[9] = byte_9
            packet[10] = byte_10

            # Byte 15 = XOR von Byte 10, 11, 12 (Index 9, 10, 11)
            packet[14] = packet[9] ^ packet[10] ^ packet[11]

            # UDP senden
            sock.sendto(packet, (UDP_IP, UDP_PORT))

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Beendet durch Benutzer.")
finally:
    pygame.quit()
