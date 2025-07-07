# Flask Notes API

A RESTful API for managing notes and collections, built with Flask. The API supports user authentication (JWT), note management, and organizing notes into collections.

## Features
- User registration and login with JWT authentication
- Secure password hashing with Flask-Bcrypt
- CRUD operations for notes
- CRUD operations for collections
- Add/remove notes to/from collections
- Each user has isolated notes and collections

## Project Structure
```
flask-notes-api/
├── app.py                # Application entry point
├── config.py             # Configuration settings
├── database.py           # SQLAlchemy database instance
├── extensions.py         # JWT, Bcrypt, and token blacklist
├── models/
│   ├── user.py           # User model
│   ├── note.py           # Note model
│   └── collection.py     # Collection model
├── routes/
│   ├── auth.py           # Auth routes (register, login, logout)
│   ├── notes.py          # Note CRUD routes
│   └── collections.py    # Collection CRUD routes
├── migrations/           # Database migrations (if used)
├── .env                  # Environment variables
└── README.md             # Project documentation
```

## Setup Instructions
1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables**
   - Create a `.env` file with your configuration (e.g., `SECRET_KEY`, `DATABASE_URI`)
4. **Run database migrations** (if using Flask-Migrate)
   ```bash
   flask db upgrade
   ```
5. **Start the application**
   ```bash
   python app.py
   ```

## API Endpoints

### Auth
- `POST /auth/register` — Register a new user
- `POST /auth/login` — Login and receive JWT token
- `POST /auth/logout` — Logout (JWT token blacklist)

### Notes
- `POST /notes` — Create a note (JWT required)
- `GET /notes` — List all notes for the user (JWT required)
- `GET /notes/<id>` — Get a specific note (JWT required)
- `PUT /notes/<id>` — Update a note (JWT required)
- `DELETE /notes/<id>` — Delete a note (JWT required)

### Collections
- `POST /collections` — Create a collection (optionally with notes)
- `GET /collections` — List all collections for the user
- `GET /collections/<id>` — Get a specific collection
- `PUT /collections/<id>` — Update a collection's title
- `DELETE /collections/<id>` — Delete a collection
- `POST /collections/<id>/add_notes` — Add notes to a collection
- `DELETE /collections/<id>/remove_notes` — Remove notes from a collection

## Notes
- All endpoints (except register/login) require a valid JWT token in the `Authorization: Bearer <token>` header.
- Collections store a list of note IDs in a JSON field. For a more robust solution, consider using a many-to-many association table.
- Token blacklisting is in-memory and will reset on server restart. For production, use a persistent store (e.g., Redis).

## License
MIT
