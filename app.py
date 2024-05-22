from configuracion.Config import Config
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from models.Models import db

from controllers.Login import logging_bp, login_manager
from controllers.Cliente import clientes_bp
from controllers.Valoracion import valoraciones_bp
from controllers.Pliegues import pliegues_bp
from controllers.Volumetria import volumetria_bp

# Crear la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
app.secret_key = "tu_clave_secreta"
db.init_app(app)

login_manager.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(clientes_bp)
app.register_blueprint(logging_bp)
app.register_blueprint(valoraciones_bp)
app.register_blueprint(pliegues_bp)
app.register_blueprint(volumetria_bp)

with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
