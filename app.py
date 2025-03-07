from flask import Flask
from flask_migrate import Migrate
from config import Config
from database import db
from extensions import jwt, bcrypt
from routes.notes import notes_bp
from routes.collections import collections_bp
from routes.auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(notes_bp)
app.register_blueprint(collections_bp)

app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)