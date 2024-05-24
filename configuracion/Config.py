import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "postgresql://postgres:211221@localhost/sena_p",
        # "DATABASE_URI",
        # "postgres://arrase:Spq1Fj4lOWOEaXeOxTIIQ5Yh7DYRaC8u@dpg-cp8g6h8l6cac73c4ilu0-a.oregon-postgres.render.com/sena_p",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
