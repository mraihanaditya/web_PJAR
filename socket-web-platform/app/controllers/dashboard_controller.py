from flask import Blueprint, render_template, request, flash, redirect, session
import socket
from config import Config
from app import db
from app.models.video import Video
from app.models.user import User

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    videos = []
    
    # Pastikan user sudah login
    if session.get('logged_in'):
        # 1. Cari data User di database berdasarkan email yang ada di session
        current_user = User.query.filter_by(email=session['email']).first()
        
        if current_user:
            # 2. Ambil video HANYA yang memiliki user_id milik user yang sedang login
            videos = Video.query.filter_by(user_id=current_user.id)\
                                .order_by(Video.uploaded_at.desc())\
                                .all()
                                
    return render_template('index.html', videos=videos)

@dashboard_bp.route('/upload', methods=['POST'])
def upload_file():
    if not session.get('logged_in'):
        flash("Silakan login terlebih dahulu.")
        return redirect('/')

    if 'file' not in request.files:
        flash('Tidak ada file')
        return redirect('/')
        
    file = request.files['file']
    
    if file.filename == '':
        flash('Tidak ada file yang dipilih')
        return redirect('/')

    try:
        # 1. Baca ukuran dan data file
        file_data = file.read()
        file_size = len(file_data)
        
        # 2. Proses Kirim File via TCP Socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((Config.TCP_SERVER_IP, Config.TCP_SERVER_PORT))
        header = f"{file.filename:<100}".encode('utf-8')
        client_socket.sendall(header + file_data)
        client_socket.close()
        
        # 3. Cari ID user yang sedang login
        user = User.query.filter_by(email=session['email']).first()
        
        # 4. Simpan Metadata ke Database MENGGUNAKAN 'user_id'
        new_video = Video(
            title=file.filename,
            filename=file.filename,
            size=file_size,
            user_id=user.id
        )
        db.session.add(new_video)
        db.session.commit()
        
        flash("Video berhasil diupload dan tersimpan di sistem!")
    except Exception as e:
        # Jika gagal, tampilkan error aslinya agar mudah dilacak
        flash(f"Gagal upload via TCP: {str(e)}")
        
    return redirect('/')