from flask import Blueprint, request, jsonify
from database import db
from models.Note import Note

notes_bp = Blueprint('notes', __name__)


# Create a note
@notes_bp.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    new_note = Note(title=data['title'], content=data['content'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify({"message": "Note created!", "note": new_note.to_dict()}), 201

# Get all notes
@notes_bp.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    return jsonify([note.to_dict() for note in notes])

# Get a single note by ID
@notes_bp.route('/notes/<int:id>', methods=['GET'])
def get_note(id):
    note = Note.query.get(id)
    if not note:
        return (jsonify
        ({"message": "Note not found!", "status_code": 404}))
    return jsonify(note.to_dict())

# Update a note
@notes_bp.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    note = Note.query.get(id)
    if not note:
        return (jsonify
    ({"message": "Note not found!", "status_code": 404}))
    data = request.get_json()
    if 'title' in data:
        note.title = data['title']
        print(f"Updated title: {note.title}")
    if 'content' in data:
        note.content = data['content']
    db.session.commit()
    return jsonify({"message": "Note updated!", "note": note.to_dict()})

# Delete a note
@notes_bp.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted!"})




