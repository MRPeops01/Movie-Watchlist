import os
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from movie_library.routes import pages

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["MONGODB_URI"] = os.environ.get("MONGODB_URI")
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw"
    )
    app.db = MongoClient(app.config["MONGODB_URI"]).get_default_database()

    # Add test user ONLY if not already in DB
    if not app.db.users.find_one({"email": "testuser@example.com"}):
        app.db.users.insert_one({
            "username": "testuser",
            "email": "testuser@example.com",
            "password": generate_password_hash("password123")
        })
        print("Test user added to Atlas!")

    app.register_blueprint(pages)
    return app
