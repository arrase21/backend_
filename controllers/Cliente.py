import re

from flask import Blueprint, jsonify, request
from models.Models import Cliente, Rol, db

clientes_bp = Blueprint("clientes", __name__)


@clientes_bp.route("/clientes/", methods=["GET"])
def get_clientes():
    clientes = Cliente.query.all()
    json_clientes = list(map(lambda x: x.to_json(), clientes))
    return jsonify({"Clientes": json_clientes}), 200


@clientes_bp.route("/cliente/<int:id>/", methods=["GET"])
def get_cliente(id):
    cliente = Cliente.query.get(id)
    if cliente:
        return (
            jsonify(
                {
                    "Cliente": cliente.to_json(),
                }
            ),
            200,
        )
    else:
        return jsonify({"message": "Cliente not found"}), 404


@clientes_bp.route("/agregar/cliente/", methods=["POST"])
def post_cliente():
    if request.json is None:
        return jsonify({"Error": "Solicitud JSON no valida"}), 400
    data = request.json
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    dni = data.get("dni")
    correo = data.get("correo")
    telefono = data.get("telefono")
    contrasena = data.get("contrasena")
    id_rol = data.get("id_rol")

    if None in (nombre, apellido, dni, correo, telefono, contrasena, id_rol):
        return jsonify({"Mensaje": "Faltan campos obligatorios"}), 400
    # Validaciones adicionales
    if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
        return jsonify({"Mensaje": "Correo no válido"}), 400

    nuevo_cliente = Cliente(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        correo=correo,
        telefono=telefono,
        contrasena=contrasena,
        id_rol=id_rol,
    )
    nuevo_cliente.set_password(contrasena)

    try:
        db.session.add(nuevo_cliente)
        db.session.commit()
        return jsonify({"Mensaje": "Cliente creado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"mensaje": "Error desconocido al agregar cliente: " + str(e)}),
            400,
        )


@clientes_bp.route("/actualizar/cliente/<int:id>/", methods=["PATCH"])
def patch_cliente(id):
    if request.json is None:
        return jsonify({"Error": "Solicitud no valida"}), 400
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"Error": "Usuario no encontrado"})
    data = request.json
    cliente.nombre = data.get("nombre", cliente.nombre)
    cliente.apellido = data.get("apellido", cliente.apellido)
    cliente.correo = data.get("correo", cliente.correo)
    cliente.telefono = data.get("telefono", cliente.telefono)
    cliente.contrasena = data.get("contrasena", cliente.contrasena)
    db.session.commit()
    return jsonify({"Mensaje": "Usuario Actualizado"}), 200


@clientes_bp.route("/cliente/promover_admin/<int:id>/", methods=["PATCH"])
def promover_admin(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"Mensaje": "Cliente no encontrado"}), 404
    rol_administrador = Rol.query.filter_by(descripcion="Administrador").first()
    if not rol_administrador:
        return jsonify({"Mensaje": "Rol de administrador no encontrado"}), 404
    if cliente.rol == rol_administrador:
        return jsonify({"Mensaje": "El cliente ya es administrador"}), 200
    cliente.rol = rol_administrador
    db.session.commit()
    return jsonify({"Mensaje": "Cliente promovido como administrador"}), 200


@clientes_bp.route("/cliente/promover_user/<int:id>/", methods=["PATCH"])
def promover_user(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"Mensaje": "Cliente no encontrado"}), 404
    rol_user = Rol.query.filter_by(descripcion="Usuario").first()
    if not rol_user:
        return jsonify({"Mensaje": "Rol de administrador no encontrado"}), 404
    if cliente.rol == rol_user:
        return jsonify({"Mensaje": "El cliente admin, degradando a usuario "}), 200
    cliente.rol = rol_user
    db.session.commit()
    return jsonify({"Mensaje": "Cliente degradado a usuario"}), 200


@clientes_bp.route("/eliminar/cliente/<int:id>/", methods=["DELETE"])
def delete_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"Mensaje": "Usuario No encontrado!!!"}), 404
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"Mensaje": "Cliente eliminado"}), 200
