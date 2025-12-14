from app import db
from datetime import datetime
import enum

class ConferenceStatus(enum.Enum):
    IDEES = "Idées"
    CONTACTE = "Contacté"
    PLANIFIE = "Planifié"
    BLOQUE = "Bloqué"
    FEEDBACK = "Feedback"
    TERMINE = "Terminé"

class ConferenceLevel(enum.Enum):
    EASY = "easy"
    MID = "mid"
    EXPERT = "expert"

class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(ConferenceStatus), default=ConferenceStatus.IDEES, nullable=False)
    assignee = db.Column(db.String(100), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    link_doc = db.Column(db.String(500), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    level = db.Column(db.Enum(ConferenceLevel), default=ConferenceLevel.EASY, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status.value,
            'assignee': self.assignee,
            'date': self.date.isoformat() if self.date else None,
            'link_doc': self.link_doc,
            'address': self.address,
            'level': self.level.value if self.level else None
        }
