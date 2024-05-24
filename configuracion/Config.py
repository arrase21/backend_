import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "postgresql://sena_p_js7p_user:PEYEwh9GbRWUalmAr6PbMJa0DWRe8WeM@dpg-cp8hlkv79t8c73cijotg-a.oregon-postgres.render.com/sena_p_js7p",
        # "DATABASE_URI",
        # "postgres://arrase:Spq1Fj4lOWOEaXeOxTIIQ5Yh7DYRaC8u@dpg-cp8g6h8l6cac73c4ilu0-a.oregon-postgres.render.com/sena_p",
        # "DATABASE_URI",
        # "postgresql://postgres:211221@localhost/sena_p",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
