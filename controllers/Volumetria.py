from flask import Blueprint, jsonify, request
from models.Models import Volumetria, Cliente, db

volumetria_bp = Blueprint("vlumetria", __name__)

MSG__NO_ENCONTRADO = "Volumetria no encontrado"


@volumetria_bp.route("/volumetria/cliente/<int:cliente_id>", methods=["GET"])
def get_volumetrias_by_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    volumetrias = Volumetria.query.filter_by(cliente_id=cliente.id).all()
    return jsonify(
        {"volumetrias": [volumetria.to_json() for volumetria in volumetrias]}
    ), 200


@volumetria_bp.route("/volumetria/<int:id_volumetria>", methods=["GET"])
def get_volumetria(id_volumetria):
    volumetria = Volumetria.query.get_or_404(id_volumetria)
    if volumetria:
        return jsonify({"Mensaje": volumetria.to_json()}), 200
    else:
        return jsonify({"Mensaje": "Error No encontrado"}), 400


@volumetria_bp.route("/volumetria/cliente/<int:id>", methods=["GET"])
def get_volumetria_cliente(id):
    volumetria = Cliente.query.get_or_404(id)
    if volumetria:
        return jsonify({"Mensaje": volumetria.to_json()}), 200
    else:
        return jsonify({"Mensaje": "Error No encontrado"}), 400


@volumetria_bp.route("/volumetria/add/<int:id>", methods=["POST"])
def add_volumetria(id):
    cliente = Cliente.query.get_or_404(id, description=MSG__NO_ENCONTRADO)

    if not request.is_json:
        return jsonify({"Error": "Solicitud no valida"})

    data = request.get_json()
    required_fields = [
        "v_cuello",
        "v_hombro",
        "v_torax",
        "v_abdomen",
        "v_bitrocanterico",
        "v_muslo_medial",
        "v_pierna",
        "v_brazo_contraido",
    ]
    if not all(field in data for field in required_fields):
        return jsonify({"Mensaje": "Faltan Campos Obligatorios"}), 404

    nueva_volumetria = Volumetria(
        v_cuello=data["v_cuello"],
        v_hombro=data["v_hombro"],
        v_torax=data["v_torax"],
        v_abdomen=data["v_abdomen"],
        v_bitrocanterico=data["v_bitrocanterico"],
        v_muslo_medial=data["v_muslo_medial"],
        v_pierna=data["v_pierna"],
        v_brazo_contraido=data["v_brazo_contraido"],
        cliente=cliente,
    )

    try:
        db.session.add(nueva_volumetria)
        db.session.commit()
        return jsonify({"Mensaje": "Volumetria agregada exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"Mensaje": str(e)})
