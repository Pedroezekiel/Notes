from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import db
from models.Note import Note

notes_bp = Blueprint('notes', __name__)


# Create a note
@notes_bp.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    data = request.get_json()
    new_note = Note(title=data['title'], content=data['content'])
    new_note.user_id = get_jwt_identity()
    db.session.add(new_note)
    db.session.commit()
    return jsonify({"message": "Note created!", "note": new_note.to_dict()}), 201

# Get all notes
@notes_bp.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    notes = Note.query.filter_by(user_id=user_id).all()
    return jsonify([note.to_dict() for note in notes])

# Get a single note by ID
@notes_bp.route('/notes/<string:id>', methods=['GET'])
@jwt_required()
def get_note(id):
    note = Note.query.filter_by(id=id, user_id=get_jwt_identity()).first()
    if not note:
        return (jsonify
        ({"message": "Note not found!", "status_code": 404}))
    return jsonify(note.to_dict())

# Update a note
@notes_bp.route('/notes/<string:id>', methods=['PUT'])
@jwt_required()
def update_note(id):
    note = Note.query.filter_by(id=id, user_id=get_jwt_identity()).first()
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
@notes_bp.route('/notes/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_note(id):
    user_id = get_jwt_identity()
    note = Note.query.filter_by(id=id, user_id=user_id).first()
    if not note:
        return jsonify({"message": "Note not found!", "status_code": 404})
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted!"})




