import qrcode
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

ip = get_local_ip()
url = f"http://{ip}:8501"
print(f"Your local URL: {url}")

img = qrcode.make(url)
img.save("anniversary_qr.png")
print("QR Code saved as anniversary_qr.png — share it with her!")
