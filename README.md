# Backend

- Proyecto para entrenadores personales que quieran tener un mejor manejo de las valoraciones y entrenamientos de los clientes
- Casi monolitico ya que no uso microservicios su deployment sera sencillo y en un solo servidor que acepte PostgreSQL

# Requisitos

- Python 3.10 >
- PostgreSQL
- Entorno virtual de Python .venv
- Crear una bd PostgreSQL que se llame sena_p con contrasena 211221

## Servidor

- Entrar al entorno virtual
  - pip install -r requirements.txt
- Ejecutar `gunicorn --bind 0.0.0.0:5000 app:app`
- Al ejecutar `gunicorn --bind 0.0.0.0:5000 app:app` este creara las tablas de la base de datos y levantara un servidor de prueba
- En el archivo **http.http** puedes ver las rutas de todos los endpoints y consultarlas o consumirlas
