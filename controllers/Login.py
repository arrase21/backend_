import logging

from flask import Blueprint, Flask, jsonify, request, session
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from models.Models import Cliente

app = Flask(__name__)
logging_bp = Blueprint("login", __name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return Cliente.query.get(int(user_id))


def verificar_rol(rol_requerido):
    if not current_user.is_authenticated:
        return False
    return rol_requerido == current_user.rol.descripcion


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@logging_bp.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"Error": "Solicitud no valida"}), 400

    data = request.get_json()
    correo = data.get("correo")
    contrasena = data.get("contrasena")

    if not correo or not contrasena:
        return jsonify({"Error": "Correo y contraseña son requeridos"}), 400

    cliente = Cliente.query.filter_by(correo=correo).first()

    if cliente is None:
        logger.info(
            f"Intento de inicio de sesión fallido: correo no encontrado ({
                correo})"
        )
        return jsonify({"Error": "Correo o contraseña incorrectos"}), 401
    if not cliente.check_password_hash(contrasena):
        logger.info(
            f"Intento de inicio de sesión fallido: contraseña incorrecta ({
                correo})"
        )
        return jsonify({"Error": "Correo o contraseña incorrectos"}), 401

    user = User(cliente.id_cliente)
    login_user(user)

    es_administrador = cliente.rol.descripcion == "Administrador"
    session["es_administrador"] = es_administrador

    return (
        jsonify(
            {
                "Mensaje": "Inicio de sesión exitoso",
                "es_administrador": es_administrador,
            }
        ),
        200,
    )


@logging_bp.route("/logout", methods=["POST"])
def logout():
    user_id = session.get("user_id")
    session.clear()
    logout_user()
    logger.info(f"Usuario {user_id} cerró sesión.")
    return jsonify({"Mensaje": "Sesión cerrada"}), 200
