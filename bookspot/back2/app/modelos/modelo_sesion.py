from datetime import datetime, timezone
from app import db

class Sesion(db.Model):
    __tablename__ = 'sesion'

    id = db.Column(db.Integer, primary_key=True)
    session_data = db.Column(db.LargeBinary(length=128))
    expiry = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)