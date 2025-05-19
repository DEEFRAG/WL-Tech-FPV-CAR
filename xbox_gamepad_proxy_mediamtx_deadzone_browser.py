import asyncio
import websockets
import socket
import json
import subprocess
import webbrowser
import os

UDP_IP = "172.16.11.1"
UDP_PORT = 23458
SEND_INTERVAL = 0.1  # 100 ms
DEADZONE_BYTE_THRESHOLD = 10  # Mindestabweichung von 0x80 (128)

BASE_PACKET = bytearray.fromhex("ca 47 d5 00 00 00 00 00 66 80 80 80 00 00 80 99")

latest_input = {"x": 0.0, "y": 0.0}
input_lock = asyncio.Lock()

def map_axis_to_byte(value):
    return int((value + 1) / 2 * 255)

def exceeds_deadzone(byte_val):
    return abs(byte_val - 128) >= DEADZONE_BYTE_THRESHOLD

async def handle_connection(websocket):
    global latest_input
    async for message in websocket:
        data = json.loads(message)
        async with input_lock:
            latest_input["x"] = data["x"]
            latest_input["y"] = data["y"]

async def udp_loop():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        async with input_lock:
            x = latest_input["x"]
            y = latest_input["y"]

        byte_9 = map_axis_to_byte(x)
        byte_10 = map_axis_to_byte(-y)

        # Wenn außerhalb der Deadzone → sende gemappte Werte, sonst neutral (0x80)
        if not exceeds_deadzone(byte_9):
            byte_9 = 0x80
        if not exceeds_deadzone(byte_10):
            byte_10 = 0x80

        packet = BASE_PACKET[:]
        packet[9] = byte_9
        packet[10] = byte_10
        packet[14] = packet[9] ^ packet[10] ^ packet[11]

        sock.sendto(packet, (UDP_IP, UDP_PORT))
        await asyncio.sleep(SEND_INTERVAL)

def start_mediamtx():
    print("Starte mediamtx (RTSP → WebRTC)...")
    return subprocess.Popen(["./mediamtx"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def open_html():
    file_path = os.path.abspath("index.html")
    url = f"file://{file_path}"
    print(f"Öffne HTML-Datei im Browser: {url}")
    webbrowser.open(url)

async def main():
    mediamtx_proc = start_mediamtx()
    await asyncio.sleep(1)

    open_html()

    print("Starte WebSocket-zu-UDP-Proxy auf Port 8765...")
    try:
        async with websockets.serve(handle_connection, "0.0.0.0", 8765):
            await udp_loop()
    finally:
        if mediamtx_proc:
            mediamtx_proc.terminate()
        print("Beendet.")

if __name__ == "__main__":
    asyncio.run(main())
