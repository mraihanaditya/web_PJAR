# Socket Web Platform (TCP Upload & UDP Stream)

Aplikasi Flask untuk manajemen video: **TCP** untuk *upload* yang stabil, dan **UDP** untuk *streaming* berlatensi rendah.

## 🛠️ Prasyarat
- Python 3.x
- Git
- XAMPP (MySQL)

---

## 🚀 Cara Instalasi

**1. Clone & Install Library**
Buka terminal dan jalankan perintah berikut secara berurutan:
```bash
git clone [https://github.com/username_anda/socket-web-platform.git](https://github.com/username_anda/socket-web-platform.git)
cd socket-web-platform

# Buat dan aktifkan virtual environment
python -m venv venv
venv\Scripts\activate      # Untuk pengguna Windows
# source venv/bin/activate # Untuk pengguna Mac/Linux

# Instal dependencies
pip install -r requirements.txt
```

**2. Setup Database**

- Nyalakan Apache dan MySQL di XAMPP.
- Buka http://localhost/phpmyadmin di browser.
- Buat database baru bernama web_socket (tabel akan dibuat otomatis oleh sistem).

**3. Konfigurasi (.env)**
Buat file baru bernama .env di folder utama aplikasi, lalu isi dengan:
```
SECRET_KEY=rahasia_bebas
DATABASE_URL=mysql+pymysql://root:@localhost/web_socket
MAIL_USERNAME=email_anda@gmail.com
MAIL_PASSWORD=password_app_gmail_anda
TCP_SERVER_IP=127.0.0.1
TCP_SERVER_PORT=5001
UDP_SERVER_IP=127.0.0.1
UDP_SERVER_PORT=5002
```
