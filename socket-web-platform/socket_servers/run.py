import subprocess
import signal
import sys
import time

print("=" * 60)
print("        SOCKET SERVER PLATFORM")
print("=" * 60)

try:
    # Menjalankan TCP Server
    print("[INFO] Menjalankan TCP File Upload Server...")
    tcp_process = subprocess.Popen(
        ["python3", "TCP/tcp_uploader.py"]
    )

    time.sleep(1)

    # Menjalankan UDP Server
    print("[INFO] Menjalankan UDP Video Streaming Server...")
    udp_process = subprocess.Popen(
        ["python3", "UDP/udp_streamer.py"]
    )

    print("\n" + "=" * 60)
    print("[SUCCESS] Semua server berhasil dijalankan")
    print(" TCP Server : Port 5001")
    print(" UDP Server : Port 5002")
    print("=" * 60)
    print("Tekan CTRL + C untuk menghentikan semua server.\n")

    # Menunggu kedua proses tetap berjalan
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n")
    print("=" * 60)
    print("[INFO] Menghentikan semua server...")

    tcp_process.terminate()
    udp_process.terminate()

    tcp_process.wait()
    udp_process.wait()

    print("[SUCCESS] TCP Server berhenti.")
    print("[SUCCESS] UDP Server berhenti.")
    print("[INFO] Socket Server Platform ditutup.")
    print("=" * 60)

    sys.exit(0)

except Exception as e:
    print(f"[ERROR] {e}")