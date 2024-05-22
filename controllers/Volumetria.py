from flask import Blueprint, jsonify, request
from models.Models import Volumetria, Cliente, db

volumetria_bp = Blueprint("vlumetria", __name__)

MSG__NO_ENCONTRADO = "Volumetria no encontrado"


@volumetria_bp.route("/volumetria/<int:id_volumetria>", methods=["GET"])
def get_volumetria(id_volumetria):
    volumetria = Volumetria.query.get_or_404(id_volumetria)
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
        "cuello",
        "hombro",
        "torax",
        "abdomen",
        "bitrocanterico",
        "muslo_medial",
        "pierna",
        "brazo_contraido",
    ]
    if not all(field in data for field in required_fields):
        return jsonify({"Mensaje": "Faltan Campos Obligatorios"}), 404

    nueva_volumetria = Volumetria(
        cuello=data["cuello"],
        hombro=data["hombro"],
        torax=data["torax"],
        abdomen=data["abdomen"],
        bitrocanterico=data["bitrocanterico"],
        muslo_medial=data["muslo_medial"],
        pierna=data["pierna"],
        brazo_contraido=data["brazo_contraido"],
        cliente=cliente,
    )

    try:
        db.session.add(nueva_volumetria)
        db.session.commit()
        return jsonify({"Mensaje": "Volumetria agregada exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"Mensaje": str(e)})
