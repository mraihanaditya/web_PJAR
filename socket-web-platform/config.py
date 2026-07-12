import os
from dotenv import load_dotenv

# Membaca isi dari file .env
load_dotenv()

class Config:
    # Mengambil nilai dari file .env
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    
    # --- KONFIGURASI DATABASE ---
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Konfigurasi Email
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Konfigurasi Socket
    TCP_SERVER_IP = os.environ.get('TCP_SERVER_IP')
    # Pastikan port diubah menjadi integer (int)
    TCP_SERVER_PORT = int(os.environ.get('TCP_SERVER_PORT')) 
    UDP_SERVER_IP = os.environ.get('UDP_SERVER_IP')
    UDP_SERVER_PORT = int(os.environ.get('UDP_SERVER_PORT')) 