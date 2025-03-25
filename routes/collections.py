from flask import Blueprint,request,jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.orm.attributes import flag_modified

from database import db

from models.note import Note
from models.collection import Collection

collections_bp = Blueprint('collections', __name__)

@collections_bp.route('/collections', methods=['POST'])
@jwt_required()
def create_collection():
    user_id = get_jwt_identity()
    data = request.get_json()

    new_collection = Collection(title=data['title'], user_id=user_id, list_of_notes=[])

    note_ids = data.get('notes', [])
    print(note_ids)
    if note_ids:
        notes = Note.query.filter(Note.id.in_(set(note_ids)),Note.user_id==user_id).all()
        print(notes, "=============-=-=-=-=-=-=-=-")
        for note in notes:
            new_collection.list_of_notes.append(note.id)
    db.session.add(new_collection)
    db.session.commit()

    return jsonify({
        "message": "Collection created!",
        "collection": new_collection.to_dict()
    }), 201

@collections_bp.route('/collections', methods=['GET'])
@jwt_required()
def get_all_collections():
    user_id = get_jwt_identity()
    collections = Collection.query.filter_by(user_id=user_id).all()
    return jsonify([returningCollection.to_dict() for returningCollection in collections])

@collections_bp.route('/collections/<string:id>', methods=['GET'])
@jwt_required()
def get_collections(id):
    collections = Collection.query.filter_by(id=id, user_id=get_jwt_identity()).first()
    if not collections:
        return jsonify({"error": "collection not found"}), 404
    return jsonify(collections.to_dict())

@collections_bp.route('/collections/<string:id>', methods=['PUT'])
@jwt_required()
def update_collection(id):
    collections = Collection.query.filter_by(id=id, user_id=get_jwt_identity()).first()
    if not collections:
        return jsonify({"error": "collection not found"}), 404
    data = request.get_json()
    collections.title = data['title']
    db.session.commit()
    return jsonify({"message": "Collection updated!", "collection": collections.to_dict()})


@collections_bp.route('/collections/<string:id>/add_notes', methods=['POST'])
@jwt_required()
def add_notes_to_collection(id):
    user_id = get_jwt_identity()
    collections = Collection.query.filter_by(id=id, user_id=user_id).first()
    if not collections:
        return jsonify({"message": "Collection not found!",
                        "status_code": 404})
    data = request.get_json()

    note_ids = data.get('notes', [])

    if not isinstance(note_ids, list):
        return jsonify({"error": "note_ids must be a list"}), 400

    valid_notes = Note.query.filter(Note.id.in_(set(note_ids)), Note.user_id==user_id).all()

    if not valid_notes:
        return jsonify({"error": "No valid notes found"}), 400

    for note in valid_notes:
        print(note.id)
        if note.id not in collections.list_of_notes:
            collections.list_of_notes.append(note.id)
    print(collections.list_of_notes)

    flag_modified(collections, "list_of_notes")
    db.session.commit()

    return jsonify({
        "message": "Notes added to collection!",
        "collection": collections.to_dict()
    }), 200

@collections_bp.route('/collections/<string:id>/remove_notes', methods=['DELETE'])
@jwt_required()
def remove_notes_from_collection(id):
    user_id = get_jwt_identity()
    collection = Collection.query.filter_by(id=id, user_id=user_id).first()
    list_of_notes = collection.list_of_notes
    if not collection:
        return jsonify({"message": "Collection not found!"}), 404
    print(collection)

    data = request.get_json()
    note_ids = data.get('notes', [])

    if not isinstance(note_ids, list):
        return jsonify({"error": "notes must be a list"}), 400

    valid_notes = Note.query.filter(Note.id.in_(note_ids), Note.user_id == user_id).all()
    removed_notes = []
    for note_id in valid_notes:
        print((str(note_id)))
        print(list_of_notes)
        if note_id.id not in list_of_notes:
            return jsonify({"error": f"Note ID {note_id} is not in this collection"}), 400
        list_of_notes.remove(note_id.id)  # Removes association instead of deleting the note
        removed_notes.append(note_id.id)

    flag_modified(collection, "list_of_notes")
    db.session.commit()

    return jsonify({
        "message": "Notes removed from collection!",
        "removed_notes": removed_notes,
        "collection": collection.to_dict()
    }), 200

@collections_bp.route('/collections/<string:id>/', methods=['DELETE'])
@jwt_required()
def delete_collection(id):
    user_id = get_jwt_identity()
    collection = Collection.query.filter_by(id=id,user_id=user_id).first()
    if not collection:
        return jsonify({"message": "Collection not found!"}), 404
    db.session.delete(collection)
    db.session.commit()
    return jsonify({"message": "Collection deleted!"})