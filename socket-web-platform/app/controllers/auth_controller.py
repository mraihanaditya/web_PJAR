from flask import Blueprint, request, redirect, session, flash, url_for
from flask_mail import Message
from itsdangerous import SignatureExpired, BadSignature

from app import mail, serializer, db 
from app.models.user import User
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    
    # CARA BENAR: Cek apakah email sudah ada di database melalui Model User
    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
        flash("Email sudah terdaftar!")
        return redirect('/')
    
    # CARA BENAR: Simpan user baru ke database
    new_user = User(email=email, password=password, verified=False)
    db.session.add(new_user)
    db.session.commit()
    
    token = serializer.dumps(email, salt='email-confirm')
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    
    try:
        msg = Message('Verifikasi Akun Dashboard Socket', sender=Config.MAIL_USERNAME, recipients=[email])
        msg.body = f"""
            Halo,

            Terima kasih telah mendaftar pada Socket Web Platform.

            Untuk menyelesaikan proses registrasi dan mengaktifkan akun Anda, silakan lakukan verifikasi email melalui tautan berikut:

            {confirm_url}

            Link tersebut akan mengonfirmasi bahwa alamat email ini benar-benar milik Anda.
            """
        mail.send(msg)
        flash("Registrasi berhasil! Cek email Anda dan klik link verifikasi sebelum login.")
        
    except Exception as e:
        # Jika gagal kirim email, batalkan pendaftaran dari database
        db.session.delete(new_user)
        db.session.commit()
        flash(f"Gagal mengirim email: {e}")
        
    return redirect('/')

@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        flash("Link verifikasi sudah kadaluarsa! Silakan daftar ulang.")
        return redirect('/')
    except BadSignature:
        flash("Link verifikasi tidak valid atau rusak!")
        return redirect('/')
        
    # CARA BENAR: Update status verifikasi
    user = User.query.filter_by(email=email).first()
    if user:
        user.verified = True
        db.session.commit()
        flash("Akun berhasil diverifikasi! Silakan Sign In sekarang.")
    else:
        flash("Akun tidak ditemukan.")
        
    return redirect('/')

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    # CARA BENAR: Mencari data akun saat login
    user = User.query.filter_by(email=email).first()
    
    # Jika user ditemukan DAN passwordnya cocok (mengikuti password yang sudah diregister)
    if user and user.password == password:
        
        # Opsional: Pastikan akun sudah melewati verifikasi registrasi
        if not user.verified:
            flash("Akun belum diverifikasi dari proses registrasi! Silakan cek email Anda terlebih dahulu.")
            return redirect('/')
            
        # Membuat token khusus untuk sesi login ini dengan salt yang berbeda
        token = serializer.dumps(email, salt='login-verify')
        login_url = url_for('auth.verify_login', token=token, _external=True)
        
        try:
            msg = Message('Verifikasi Login Dashboard Socket', sender=Config.MAIL_USERNAME, recipients=[email])
            msg.body = f"""
                Halo,

                Seseorang baru saja memasukkan email dan password yang benar untuk akun Anda.
                Untuk menyelesaikan proses Sign In dan masuk ke Dashboard, silakan klik tautan verifikasi berikut:

                {login_url}

                Tautan ini berlaku selama 10 menit. Jika Anda tidak merasa melakukan login, abaikan email ini dan segera ubah password Anda.
                """
            mail.send(msg)
            
            # Berikan notifikasi ke UI agar user mengecek email (Sesi belum diaktifkan di sini)
            flash("Kredensial benar! Link untuk melanjutkan login telah dikirim ke email Anda.")
            
        except Exception as e:
            flash(f"Gagal mengirim email verifikasi login: {e}")
            
    else:
        flash("Email atau password salah!")
        
    return redirect('/')

# --- RUTE BARU: VERIFIKASI LINK LOGIN ---
@auth_bp.route('/verify-login/<token>')
def verify_login(token):
    try:
        # Maksimal waktu klik link adalah 10 menit (600 detik)
        email = serializer.loads(token, salt='login-verify', max_age=600)
    except SignatureExpired:
        flash("Link verifikasi login sudah kadaluarsa! Silakan Sign In ulang dari awal.")
        return redirect('/')
    except BadSignature:
        flash("Link verifikasi login tidak valid atau rusak!")
        return redirect('/')
        
    # Jika token valid, pastikan user masih ada di database
    user = User.query.filter_by(email=email).first()
    if user:
        # Di sinilah proses otorisasi login sebenarnya terjadi
        session['logged_in'] = True
        session['email'] = email
        flash("Login berhasil diotorisasi! Selamat datang.")
    else:
        flash("Akun tidak ditemukan.")
        
    return redirect('/')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')