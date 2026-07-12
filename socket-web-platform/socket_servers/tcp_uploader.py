import socket
import os

HOST = '0.0.0.0'
PORT = 5001
SAVE_DIR = 'uploaded_files'

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def start_tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print("=" * 60)
    print("            TCP FILE UPLOAD SERVER")
    print("=" * 60)
    print(f"[INFO] Server berjalan")
    print(f"[INFO] Host        : {HOST}")
    print(f"[INFO] Port        : {PORT}")
    print(f"[INFO] Save Folder : {os.path.abspath(SAVE_DIR)}")
    print("[STATUS] Menunggu koneksi client...")
    print("=" * 60)

    while True:
        conn, addr = server.accept()

        print(f"\n[CONNECT] Client terhubung")
        print(f"          IP Address : {addr[0]}")
        print(f"          Port       : {addr[1]}")

        # Baca 100 byte pertama sebagai nama file
        header = conn.recv(100)
        if not header:
            print("[WARNING] Header file kosong. Koneksi ditutup.")
            conn.close()
            continue

        filename = header.decode().strip()
        filepath = os.path.join(SAVE_DIR, filename)

        print(f"[FILE] Nama File   : {filename}")
        print("[INFO] Mulai menerima file...")

        total_bytes = 0

        with open(filepath, "wb") as f:
            while True:
                data = conn.recv(4096)
                if not data:
                    break

                f.write(data)
                total_bytes += len(data)

        print(f"[SUCCESS] Upload selesai")
        print(f"[INFO] Lokasi File : {filepath}")
        print(f"[INFO] Ukuran File : {total_bytes} bytes")
        print(f"[DISCONNECT] Client {addr[0]} telah terputus.")
        print("-" * 60)

        conn.close()

if __name__ == "__main__":
    start_tcp_server()