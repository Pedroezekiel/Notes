from flask import Blueprint, request, jsonify
from extensions import blacklisted_tokens
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from models.user import User
from database import db

auth_bp = Blueprint("auth", __name__)

# Register route
@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Login route
@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200

@auth_bp.route("/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklisted_tokens.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200


# @auth_bp.route("/protected", methods=["GET"])
# def protected():
#     current_user_id = get_jwt_identity()
#     print(current_user_id)
#     user = User.query.get(current_user_id)
#     print(user)
#     if not user:
#         return jsonify({"error": "User not found"}), 40
#     return jsonify({"message": f"Welcome, {user.username}!"}), 200
