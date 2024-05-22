from flask import Blueprint, jsonify, request
from models.Models import Pliegues, db, Cliente

pliegues_bp = Blueprint("pliegues", __name__)

MSG__NO_ENCONTRADO = "Pliegue no encontrado"


@pliegues_bp.route("/pliegues/<int:id_pliegue>", methods=["GET"])
def get_pliegue(id_pliegue):
    pliegues = Pliegues.query.get(id_pliegue)
    if pliegues:
        return jsonify({"Mensaje": pliegues.to_json()}), 200
    else:
        return jsonify({"mensaje": MSG__NO_ENCONTRADO})


@pliegues_bp.route("/pliegues/add/<int:id>", methods=["POST"])
def add_pliegues(id):
    cliente = Cliente.query.get_or_404(id, description=MSG__NO_ENCONTRADO)
    if not request.is_json:
        return jsonify({"Error": "Solicitud no valida"})

    data = request.get_json()
    required_fields = [
        "tricipital",
        "subescapular",
        "suprailiaco",
        "abdominal",
        "muslo_medial",
        "pierna",
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), 404

    nuevo_pliegue = Pliegues(
        tricipital=data["tricipital"],
        subescapular=data["subescapular"],
        suprailiaco=data["suprailiaco"],
        abdominal=data["abdominal"],
        muslo_medial=data["muslo_medial"],
        pierna=data["pierna"],
        cliente=cliente,
    )
    try:
        db.session.add(nuevo_pliegue)
        db.session.commit()
        return jsonify({"Mensaje": "Pliegue agregado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"Mensaje": str(e)})


@pliegues_bp.route("/pliegues/actualizar/<int:id_pliegue>", methods=["PATCH"])
def patch_pliegues(id_pliegue):
    pliegue = Pliegues.query.get_or_404(id_pliegue)

    if not request.is_json:
        return jsonify(), 400

    data = request.json
    pliegue.tricipital = data.get("tricipital", pliegue.tricipital)
    pliegue.subescapular = data.get("subescapular", pliegue.subescapular)
    pliegue.suprailiaco = data.get("suprailiaco", pliegue.suprailiaco)
    pliegue.abdominal = data.get("abdominal", pliegue.abdominal)
    pliegue.muslo_medial = data.get("muslo_medial", pliegue.muslo_medial)
    pliegue.pierna = data.get("pierna", pliegue.pierna)

    try:
        db.session.commit()
        return jsonify({"mensaje": "Pliegues actualizados correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": str(e)}), 400
