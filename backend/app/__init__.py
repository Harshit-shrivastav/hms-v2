from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from config import Config
from app.models.models import db, User
from werkzeug.security import generate_password_hash

flask_app = Flask(__name__)
CORS(flask_app)

flask_app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

flask_app.config["CACHE_TYPE"] = "RedisCache"
flask_app.config["CACHE_REDIS_URL"] = Config.REDIS_URL
flask_app.config["CACHE_DEFAULT_TIMEOUT"] = Config.CACHE_REDIS_TTL

cache = Cache(flask_app)

db.init_app(flask_app)

with flask_app.app_context():
    db.create_all()
    admin = User.query.filter_by(role="admin").first()
    if not admin:
        try:
            new_admin = User(
                username="admin",
                email=Config.ADMIN_EMAIL,
                role="admin",
                password=generate_password_hash(Config.ADMIN_PASSWORD),
            )
            db.session.add(new_admin)
            db.session.commit()
            print("admin created")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to create admin: {e}")

jwt = JWTManager(flask_app)
cors = CORS(flask_app, origins=Config.CORS_ORIGIN, supports_credentials=True)

flask_app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
flask_app.config["JWT_TOKEN_LOCATION"] = Config.JWT_TOKEN_LOCATION
flask_app.config["JWT_COOKIE_CSRF_PROTECT"] = False
flask_app.config["JWT_COOKIE_SAMESITE"] = "Lax"
flask_app.config["JWT_COOKIE_SECURE"] = False
flask_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 60 * 60 * 24 * 7
flask_app.config["JWT_COOKIE_MAX_AGE"] = 60 * 60 * 24 * 7
flask_app.config["WTF_CSRF_ENABLED"] = False

import app.routes.user_routes
import app.routes.admin_routes
import app.routes.doctor_routes
import app.routes.patient_routes
