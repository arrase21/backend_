from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class Image(db.Model):
    __tablename__ = "image"
    id_image = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String, unique=False, nullable=False)
    id_cliente = db.Column(
        db.Integer, db.ForeignKey("clientes.id_cliente"), nullable=False
    )
    clientes = db.relationship("Cliente", back_populates="imagen")


class Rol(db.Model):
    __tablename__ = "roles"
    id_rol = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), unique=True, nullable=False)
    clientes = db.relationship("Cliente", back_populates="rol")


class Cliente(db.Model):
    __tablename__ = "clientes"
    id_cliente = db.Column(
        db.Integer,
        primary_key=True,
    )
    nombre = db.Column(db.String(100), unique=False, nullable=False)
    apellido = db.Column(db.String(100), unique=False, nullable=False)
    dni = db.Column(db.Integer, unique=True, nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.BigInteger, unique=True, nullable=False)
    contrasena = db.Column(db.String(300), unique=False, nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey("roles.id_rol"), nullable=False)
    rol = db.relationship("Rol", back_populates="clientes")
    imagen = db.relationship("Image", back_populates="clientes")
    valoraciones = db.relationship("Valoracion", back_populates="cliente")
    volumetrias = db.relationship("Volumetria", back_populates="cliente")
    pliegues = db.relationship("Pliegues", back_populates="cliente")

    def set_password(self, contrasena):
        self.contrasena = generate_password_hash(contrasena)

    def check_password_hash(self, contrasena):
        return check_password_hash(self.contrasena, contrasena)

    def to_json(self):
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "correo": self.correo,
            "telefono": self.telefono,
        }


class Valoracion(db.Model):
    __tablename__ = "valoracion"
    id_valoracion = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id_cliente"))
    # fecha = db.Column(db.Date, unique=False, nullable=False)
    talla_cm = db.Column(db.Integer, unique=False, nullable=False)
    talla_mts = db.Column(db.Float, unique=False, nullable=False)
    peso_kg = db.Column(db.Integer, unique=False, nullable=False)
    diametro_humero = db.Column(db.Integer, unique=False, nullable=False)
    diametro_femur = db.Column(db.Integer, unique=False, nullable=False)
    cliente = relationship("Cliente", back_populates="valoraciones")

    def to_json(self):
        return {
            "id_valoracion": self.id_valoracion,
            "id_cliente": self.id_cliente,
            # "fecha": self.fecha,
            "talla_cm": self.talla_cm,
            "talla_mts": self.talla_mts,
            "peso_kg": self.peso_kg,
            "diametro_femur": self.diametro_femur,
            "diametro_humero": self.diametro_humero,
        }


class Volumetria(db.Model):
    __tablename__ = "volumetria"
    id_volumetria = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id_cliente"))

    v_cuello = db.Column(db.Integer, unique=False, nullable=False)
    v_hombro = db.Column(db.Integer, unique=False, nullable=False)  #
    v_torax = db.Column(db.Integer, unique=False, nullable=False)
    v_abdomen = db.Column(db.Integer, unique=False, nullable=False)
    v_bitrocanterico = db.Column(db.Integer, unique=False, nullable=False)
    v_muslo_medial = db.Column(db.Integer, unique=False, nullable=False)
    v_pierna = db.Column(db.Integer, unique=False, nullable=False)
    v_brazo_contraido = db.Column(db.Integer, unique=False, nullable=False)
    cliente = relationship("Cliente", back_populates="volumetrias")

    def to_json(self):
        return {
            "id_volumetria": self.id_volumetria,
            "id_cliente": self.id_cliente,
            "v_cuello": self.v_cuello,
            "v_hombro": self.v_hombro,
            "v_torax": self.v_torax,
            "v_abdomen": self.v_abdomen,
            "v_bitrocanterico": self.v_bitrocanterico,
            "v_muslo_medial": self.v_muslo_medial,
            "v_pierna": self.v_pierna,
            "v_brazo_contraido": self.v_brazo_contraido,
        }


class Pliegues(db.Model):
    __tablename__ = "pliegues"
    id_pliegue = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id_cliente"))
    tricipital = db.Column(db.Integer, unique=False, nullable=False)
    subescapular = db.Column(db.Integer, unique=False, nullable=False)
    suprailiaco = db.Column(db.Integer, unique=False, nullable=False)
    abdominal = db.Column(db.Integer, unique=False, nullable=False)
    muslo_medial = db.Column(db.Integer, unique=False, nullable=False)
    pierna = db.Column(db.Integer, unique=False, nullable=False)
    cliente = relationship("Cliente", back_populates="pliegues")

    def to_json(self):
        return {
            "id_pliegue": self.id_pliegue,
            "id_cliente": self.id_cliente,
            "tricipital": self.tricipital,
            "subescapular": self.subescapular,
            "suprailiaco": self.suprailiaco,
            "abdominal": self.abdominal,
            "muslo_medial": self.muslo_medial,
            "pierna": self.pierna,
        }


Cliente.valoraciones = relationship(
    "Valoracion", order_by=Valoracion.id_valoracion, back_populates="cliente"
)
Cliente.volumetrias = relationship(
    "Volumetria", order_by=Volumetria.id_volumetria, back_populates="cliente"
)
Cliente.pliegues = relationship(
    "Pliegues", order_by=Pliegues.id_pliegue, back_populates="cliente"
)


def initialize_roles():
    roles = [
        {"id_rol": 1, "descripcion": "Administrador"},
        {"id_rol": 2, "descripcion": "Usuario"},
    ]

    for role_data in roles:
        role = Rol.query.get(role_data["id_rol"])
        if not role:
            new_role = Rol(
                id_rol=role_data["id_rol"], descripcion=role_data["descripcion"]
            )
            db.session.add(new_role)

    db.session.commit()
