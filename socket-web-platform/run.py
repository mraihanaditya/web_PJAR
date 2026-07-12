from app import create_app

# Inisialisasi Aplikasi Flask
app = create_app()

if __name__ == '__main__':
    # Mengambil nilai IP yang sudah dimuat oleh Flask dari config.py
    tcp_ip = app.config.get('TCP_SERVER_IP')
    udp_ip = app.config.get('UDP_SERVER_IP')
    
    print(f"[*] Menghubungi TCP Server di IP: {tcp_ip}")
    print(f"[*] Menghubungi UDP Server di IP: {udp_ip}")
    
    app.run(host='0.0.0.0', debug=True, port=5000)