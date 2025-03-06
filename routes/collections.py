from flask import Blueprint,request,jsonify
from sqlalchemy.orm.collections import collection

from database import db

from models.Note import Note
from models.Collection import Collection

collections_bp = Blueprint('collections', __name__)

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

@collections_bp.route('/collections', methods=['GET'])
def get_all_collections():
    collections = Collection.query.all()
    return jsonify([returningCollection.to_dict() for returningCollection in collections])

@collections_bp.route('/collections/<int:id>', methods=['GET'])
def get_collections(id):
    collections = Collection.query.get_or_404(id)
    return jsonify(collections.to_dict())

@collections_bp.route('/collections/<int:id>', methods=['PUT'])
def update_collection(id):
    collections = Collection.query.get_or_404(id)
    data = request.get_json()
    collections.title = data['title']
    db.session.commit()
    return jsonify({"message": "Collection updated!", "collection": collections.to_dict()})


@collections_bp.route('/collections/<int:id>/add_notes', methods=['POST'])
def add_notes_to_collection(id):
    collections = Collection.query.get(id)
    if not collections:
        return jsonify({"message": "Collection not found!",
                        "status_code": 404})
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
    collection = Collection.query.get(id)
    if not collection:
        return jsonify({"message": "Collection not found!", "status_code": 404}), 404
    print(collection)

    data = request.get_json()
    note_ids = data.get('notes', [])

    if not isinstance(note_ids, list):
        return jsonify({"error": "notes must be a list"}), 400

    # Ensure only notes that are in the collection are removed
    removed_notes = []
    for note_id in note_ids:
        note = Note.query.get(note_id)
        if not note or note not in collection.list_of_notes:
            return jsonify({"error": f"Note ID {note_id} is not in this collection"}), 400

        collection.list_of_notes.remove(note)  # Removes association instead of deleting the note
        removed_notes.append(note_id)

    db.session.commit()

    return jsonify({
        "message": "Notes removed from collection!",
        "removed_notes": removed_notes,
        "collection": collection.to_dict()
    }), 200

@collections_bp.route('/collections/<int:id>/', methods=['DELETE'])
def delete_collection(id):
    collection = Collection.query.get_or_404(id)
    db.session.delete(collection)
    db.session.commit()
    return jsonify({"message": "Collection deleted!"})