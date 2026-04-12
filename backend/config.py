import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dbvuevbhciehiub"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "bnejbcjbcivjeebvu"
    CORS_ORIGIN = os.environ.get("CORS_ORIGIN") or "http://localhost:5173"
    JWT_TOKEN_LOCATION = os.environ.get("JWT_TOKEN_LOCATION") or "cookies"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///hms.db"
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL") or "admin@hms.com"
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") or "admin@hms.com"
    REDIS_URL = os.environ.get("REDIS_URL") or "rediss://default:gQAAAAAAATqZAAIncDE1N2I4YzgxODIyMzE0Y2RjOWNjNGEwMGU4MTE1OTA0ZXAxODA1Mzc@gentle-ferret-80537.upstash.io:6379/0"
    CACHE_REDIS_TTL = 300
    SMTP_SERVER = "smtp.gmx.com"
    SMTP_PORT = 587
    SMTP_EMAIL = os.environ.get("SMTP_EMAIL") or "harshit@gmx.ie"
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD") or "ZBL7L3HQUMTR335SMKV3"
