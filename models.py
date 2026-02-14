from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    api_key = db.Column(db.Text, nullable=False)  # Encrypted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)

class PromoJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(100))
    tokens_used = db.Column(db.Integer, default=0)
    estimated_cost = db.Column(db.Float, default=0.0)
    zip_path = db.Column(db.String(500))
    status = db.Column(db.String(20), default='pending') # pending, processing, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
