from database import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content
        }

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    list_of_notes = db.relationship('Note', backref='collection', lazy='dynamic')  # ✅ Corrected

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "list_of_notes": [note.id for note in self.list_of_notes.all()]  # Convert to list of IDs
        }
