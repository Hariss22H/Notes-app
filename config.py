import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    # Prefer DATABASE_URL if provided (for production). Otherwise use a local sqlite file for
    # ease of development and container usage.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        os.environ.get("SQLITE_URL", "sqlite:///notes.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
