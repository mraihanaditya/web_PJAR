from app import db
from datetime import datetime
import uuid

class Video(db.Model):
    __tablename__ = 'videos'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    
    # PASTIKAN BARIS INI ADA DAN MENGGUNAKAN 'users.id'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)