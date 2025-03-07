from database import db
import uuid


class Collection(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    list_of_notes = db.relationship('Note', backref='collection', lazy='dynamic')
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "list_of_notes": [note.id for note in self.list_of_notes.all()]
        }