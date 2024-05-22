import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI", "postgresql://postgres:211221@localhost/sena_p"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
