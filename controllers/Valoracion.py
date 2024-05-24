import logging

from flask import Blueprint, jsonify, request

from models.Models import Cliente, Valoracion, db

valoraciones_bp = Blueprint("valoraciones", __name__)
valoraciones_bp = Blueprint("valoraciones", __name__)
logging.basicConfig(level=logging.INFO)

MSG_CLIENTE_NO_ENCONTRADO = "Cliente no encontrado"
MSG_SOLICITUD_JSON_NO_VALIDA = "Solicitud JSON no válida"
MSG_FALTAN_CAMPOS_OBLIGATORIOS = "Faltan campos obligatorios"
MSG_VALORACION_CREADA = "Valoración creada exitosamente"


@valoraciones_bp.route("/valoraciones/cliente/<int:cliente_id>", methods=["GET"])
def get_valoraciones_by_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    valoraciones = Valoracion.query.filter_by(cliente_id=cliente.id).all()
    return (
        jsonify(
            {"valoraciones": [valoracion.to_json() for valoracion in valoraciones]}
        ),
        200,
    )


@valoraciones_bp.route("/valoraciones/", methods=["GET"])
def get_valoraciones():
    valoraciones = Valoracion.query.all()
    valoraciones_json = [valoracion.to_json() for valoracion in valoraciones]
    return jsonify({"valoraciones": valoraciones_json}), 200


@valoraciones_bp.route("/valoracion/<int:id_valoracion>", methods=["GET"])
def get_valoracion(id_valoracion):
    valoracion = Valoracion.query.get(id_valoracion)
    if valoracion:
        return jsonify({"Valoracion": valoracion.to_json()}), 200
    else:
        return jsonify({"Mensaje": MSG_CLIENTE_NO_ENCONTRADO}), 404


@valoraciones_bp.route("/valoracion/add/<int:id>", methods=["POST"])
def add_valoracion(id):
    cliente = Cliente.query.get_or_404(id, description=MSG_CLIENTE_NO_ENCONTRADO)

    if not request.is_json:
        return jsonify({"error": MSG_SOLICITUD_JSON_NO_VALIDA}), 400

    data = request.get_json()
    required_fields = [
        "talla_cm",
        "talla_mts",
        "peso_kg",
        "diametro_humero",
        "diametro_femur",
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": MSG_FALTAN_CAMPOS_OBLIGATORIOS}), 400

    nueva_valoracion = Valoracion(
        # fecha=data["fecha"],
        talla_cm=data["talla_cm"],
        talla_mts=data["talla_mts"],
        peso_kg=data["peso_kg"],
        diametro_humero=data["diametro_humero"],
        diametro_femur=data["diametro_femur"],
        cliente=cliente,
    )

    try:
        db.session.add(nueva_valoracion)
        db.session.commit()
        return jsonify({"mensaje": MSG_VALORACION_CREADA}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@valoraciones_bp.route("/valoracion/patch/<int:id_valoracion>", methods=["PATCH"])
def patch_valoracion(id_valoracion):
    if request.json is None:
        return jsonify({"Error": "Solicitud no valida"}), 400
    valoracion = Valoracion.query.get(id_valoracion)
    if not valoracion:
        return jsonify({"Error": "Usuario no encontrado"})

    data = request.json
    valoracion.fecha = data.get("fecha", valoracion.fecha)
    valoracion.talla_cm = data.get("talla_cm", valoracion.talla_cm)
    valoracion.talla_mts = data.get("talla_mts", valoracion.talla_mts)
    valoracion.peso_kg = data.get("peso_kg", valoracion.peso_kg)
    valoracion.diametro_humero = data.get("diametro_humero", valoracion.diametro_humero)
    valoracion.diametro_femur = data.get("diametro_femur", valoracion.diametro_femur)

    db.session.commit()
    return jsonify({"Mensaje": "Valoraion actualizada"})
