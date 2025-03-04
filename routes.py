from flask import Blueprint, request, jsonify
from sqlalchemy.orm.collections import collection

from database import db
from models import Note, Collection

notes_bp = Blueprint('notes', __name__)

collections_bp = Blueprint('collections', __name__)

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
    note = Note.query.get_or_404(id)
    return jsonify(note.to_dict())

# Update a note
@notes_bp.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    note = Note.query.get_or_404(id)
    data = request.get_json()
    note.title = data['title']
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

@collections_bp.route('/collections', methods=['POST'])
def create_collection():
    data = request.get_json()

    new_collection = Collection(title=data['title'])
    db.session.add(new_collection)
    db.session.commit()

    note_ids = data.get('notes', [])
    if note_ids:
        notes = Note.query.filter(Note.id.in_(note_ids)).all()
        for note in notes:
            note.collection_id = new_collection.id

    db.session.commit()

    return jsonify({
        "message": "Collection created!",
        "collection": new_collection.to_dict()
    }), 201

@collections_bp.route('/collections/<int:id>', methods=['GET'])
def get_collections(id):
    collections = Collection.query.get_or_404(id)
    return jsonify(collections.to_dict())

@collections_bp.route('/collections/<int:id>', methods=['PUT'])
def update_collection(id):
    collections = Collection.query.get_or_404(id)
    data = request.get_json()
    collections.title = data['title']
    collections.list_of_notes = data.get('notes', [])
    db.session.commit()
    return jsonify({"message": "Collection updated!", "collection": collections.to_dict()})


@collections_bp.route('/collections/<int:id>/add_notes', methods=['POST'])
def add_notes_to_collection(id):
    collections = Collection.query.get_or_404(id)
    data = request.get_json()

    note_ids = data.get('notes', [])

    if not isinstance(note_ids, list):
        return jsonify({"error": "note_ids must be a list"}), 400

    valid_notes = Note.query.filter(Note.id.in_(note_ids)).all()

    if not valid_notes:
        return jsonify({"error": "No valid notes found"}), 400

    for note in valid_notes:
        note.collection_id = collections.id

    db.session.commit()

    return jsonify({
        "message": "Notes added to collection!",
        "collection": collections.to_dict()
    }), 200

@collections_bp.route('/collections/<int:id>/remove_notes', methods=['DELETE'])
def remove_notes_from_collection(id):
    collections = Collection.query.get_or_404(id)
    data = request.get_json()
    note_ids = data.get('notes', [])
    if not isinstance(note_ids, list):
        return jsonify({"error": "note_ids must be a list"}), 400
    for note_id in note_ids:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
    return jsonify({"message": "Notes removed from collection!",
                    "collection": collections.to_dict()}), 200

@collections_bp.route('/collections/<int:id>/remove_collection', methods=['DELETE'])
def delete_collection(id):
    collection = Collection.query.get_or_404(id)
    db.session.delete(collection)
    db.session.commit()
    return jsonify({"message": "Collection deleted!"})




