import socket
import os

HOST = '0.0.0.0'
PORT = 5002
BASE_DIR = 'uploaded_files'

def start_udp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))

    print("=" * 60)
    print("          UDP VIDEO STREAMING SERVER")
    print("=" * 60)
    print(f"[INFO] Server berjalan pada {HOST}:{PORT}")
    print(f"[INFO] Folder video : {os.path.abspath(BASE_DIR)}")
    print("[INFO] Menunggu permintaan client...")
    print("=" * 60)

    while True:
        try:
            data, addr = server.recvfrom(1024)

            print(f"\n[REQUEST] Permintaan diterima dari {addr}")

            request_data = data.decode('utf-8').split('|')

            # Format:
            # FETCH | filename.mp4 | start_byte | length
            if request_data[0] == "FETCH" and len(request_data) == 4:

                filename = request_data[1]
                start_byte = int(request_data[2])
                length = int(request_data[3])

                print(f"[VIDEO] File        : {filename}")
                print(f"[VIDEO] Start Byte  : {start_byte}")
                print(f"[VIDEO] Chunk Size  : {length} Byte")

                filepath = os.path.join(BASE_DIR, filename)

                if os.path.exists(filepath):

                    with open(filepath, 'rb') as f:
                        f.seek(start_byte)
                        chunk = f.read(length)

                    server.sendto(chunk, addr)

                    print(f"[SUCCESS] Mengirim {len(chunk)} Byte ke {addr}")

                else:
                    print(f"[ERROR] File '{filename}' tidak ditemukan.")

                    server.sendto(b"ERROR_NOT_FOUND", addr)

            else:
                print(f"[WARNING] Format request tidak valid dari {addr}")

        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == '__main__':
    start_udp_server()