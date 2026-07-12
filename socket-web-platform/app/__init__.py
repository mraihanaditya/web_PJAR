from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import Config
from itsdangerous import URLSafeTimedSerializer

# Inisialisasi Ekstensi
mail = Mail()
db = SQLAlchemy()
serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)
    db.init_app(app)

    # 1. IMPORT MODEL LEBIH DULU (Sangat Penting!)
    from app.models.user import User
    from app.models.video import Video

    # 2. BARU IMPORT CONTROLLER
    from app.controllers.auth_controller import auth_bp
    from app.controllers.dashboard_controller import dashboard_bp
    from app.controllers.stream_controller import stream_bp

    # 3. REGISTER BLUEPRINT
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(stream_bp)

    # 4. BUAT TABEL
    with app.app_context():
        db.create_all()

    return app