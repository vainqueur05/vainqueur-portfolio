from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    client = db.Column(db.String(100))
    source_link = db.Column(db.String(200))
    demo_link = db.Column(db.String(200))
    date = db.Column(db.String(20))
    category = db.Column(db.String(50))

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    price = db.Column(db.String(50))
    delivery_days = db.Column(db.Integer)

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50))  # frontend, backend, tools, ai
    percentage = db.Column(db.Integer)   # pour affichage en barre de progression

class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50))
    value = db.Column(db.String(50))
    icon = db.Column(db.String(50))

class Benefit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))


class VisitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(200))
    ip = db.Column(db.String(45))          # ← doit s'appeler 'ip'
    user_agent = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Bio(db.Model):
    id = db.Column(db.Integer, primary_key=True, default=1)
    name = db.Column(db.String(100))
    title = db.Column(db.String(200))
    bio_text = db.Column(db.Text, default='Je suis développeur passionné...')
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    availability = db.Column(db.Boolean, default=True)
    avatar = db.Column(db.String(200), default='default-avatar.jpg')

    @classmethod
    def get_singleton(cls):
        bio = cls.query.get(1)
        if not bio:
            bio = cls(id=1)
            db.session.add(bio)
            db.session.commit()
        return bio

# ... (garde tes autres modèles User, Project, etc. inchangés) ...

class GlobalConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Boolean, default=False)

    @classmethod
    def is_maintenance(cls):
        """Vérifie si le mode maintenance est actif sans faire planter l'app"""
        try:
            # On cherche la clé spécifique dans la table de config
            config = cls.query.filter_by(key='maintenance_mode').first()
            if config:
                return config.value
            return False
        except Exception:
            # En cas d'erreur (table manquante, etc.), on considère que c'est ouvert
            return False
        

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    message = db.Column(db.Text)
    read = db.Column(db.Boolean, default=False) # <--- Nouveau : Statut de lecture
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

class WhatsAppClick(db.Model): # <--- Nouveau : Tracker les prospects WhatsApp
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)