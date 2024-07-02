from app import create_app
from app.base import init_db

"""
    Este archivo limpia la base de datos y la inicializa con valores por defecto.
    Usar con precaucion, ya que se perderan todos los datos existentes en la base de datos.
    en su lugar usar el comando 'flask run' en la terminal para iniciar la aplicacion.
"""
app = create_app()

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run()
    