from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import os

from models.Models import Image, db, Cliente

image_bp = Blueprint('upload', __name__)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@image_bp.route('/upload/img/<int:id>/', methods=["POST"])
def upload_img(id):
    cliente = Cliente.query.get_or_404(id)
    if cliente is None:
        return jsonify({"Mensaje": "Cliente encontrado"}), 400

    if not request.is_json:
        return jsonify({"Error": "Solicitud no válida"})

    if 'image' not in request.files:
        return jsonify({"Mensaje": 'Se requiere la imagen'})

    image = request.files['image']

    # verificar la imagen
    if not image or image.filename == '':
        return jsonify({"Mensaje": "Nombre de archivo vacío"})

    if not image or not allowed_file(image.filename):
        return jsonify({"Mensaje": "Tipo de archivo no permitido"})

    # Crear la carpeta del usuario si no existe
    user_folder = os.path.join('static/images/', str(id))
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    if image.filename is None or image.filename == "":
        return jsonify({"Mensaje": "Error, nombre vacio"})

    filename = secure_filename(image.filename)
    image_path = os.path.join(user_folder, filename)

    image.save(image_path)

    # Guardar la ruta de la imagen en la base de datos
    new_image = Image(image_path=image_path, cliente_id=id)
    try:
        db.session.add(new_image)
        db.session.commit()
        return jsonify({"Mensaje": "Imagen subida correctamente"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"Mensaje": "Error al subir la imagen"})

# from models.Models import Image, db, Cliente
# import os
#
# from flask import Blueprint, jsonify, request
#
# image_bp = Blueprint('upload', __name__)
#
#
# @image_bp.route('/upload/img/<int:id>/', methods=["POST"])
# def upload_img(id):
#     cliente = Cliente.query.get_or_404(id)
#     if not request.is_json:
#         return jsonify({"Error": "Solicitud no valida"})
#
#     if 'imgage' not in request.files or request.form:
#         return jsonify({"Mensake": 'Se requiere la imgen'})
#
#     image = request.files['image']
#     user_folder = os.path.join('/imagen', id)
#
#     if not os.path.exists(user_folder):
#         os.makedirs(user_folder)
#
#     image_path = os.path.join(user_folder, image.filename)
#     image.save(image_path)
#
#     new_image = Image(image_path=image_path)
#     try:
#         db.session.add(new_image)
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"Mensaje": "Error al subir la img"})
