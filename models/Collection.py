from database import db


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    list_of_notes = db.relationship('Note', backref='collection', lazy='dynamic')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "list_of_notes": [note.id for note in self.list_of_notes.all()]
        }