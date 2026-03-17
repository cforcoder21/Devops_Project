from datetime import datetime
from src.main.app import db


class Incident(db.Model):
    __tablename__ = 'incidents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # P0, P1, P2, P3
    status = db.Column(db.String(30), default='open')     # open, resolved, closed
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    detected_by = db.Column(db.String(100))
    reported_by = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    postmortem = db.relationship('PostMortem', backref='incident', uselist=False, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'severity': self.severity,
            'status': self.status,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'detected_by': self.detected_by,
            'reported_by': self.reported_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


class PostMortem(db.Model):
    __tablename__ = 'postmortems'

    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    impact = db.Column(db.Text)
    root_cause = db.Column(db.Text)
    timeline = db.Column(db.JSON)           # List of {"time": ..., "event": ...}
    contributing_factors = db.Column(db.JSON)
    action_items = db.Column(db.JSON)       # List of {"task": ..., "owner": ..., "due_date": ...}
    lessons_learned = db.Column(db.Text)
    detection_method = db.Column(db.String(100))
    resolution_steps = db.Column(db.Text)
    created_by = db.Column(db.String(100))
    reviewed_by = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'incident_id': self.incident_id,
            'summary': self.summary,
            'impact': self.impact,
            'root_cause': self.root_cause,
            'timeline': self.timeline,
            'contributing_factors': self.contributing_factors,
            'action_items': self.action_items,
            'lessons_learned': self.lessons_learned,
            'detection_method': self.detection_method,
            'resolution_steps': self.resolution_steps,
            'created_by': self.created_by,
            'reviewed_by': self.reviewed_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
