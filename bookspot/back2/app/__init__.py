from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from flask_session import Session
from config import AppConfig  # Asegúrate de que esta importación sea correcta

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app_config = AppConfig.get_instance()  # Obtiene la instancia de configuración
    app.config.from_object(app_config)  # Usa la instancia para configurar la app

    # Configuración específica de la sesión
    app.config['SESSION_SQLALCHEMY'] = db

    CORS(app, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    Session(app)  # Inicializa la sesión después de configurar db

    from app.blueprints.login.bp_login import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.blueprints.ventas.bp_ventas import ventas_bp
    app.register_blueprint(ventas_bp, url_prefix='/ventas')
    from app.blueprints.inventario.bp_inventario import inventario_bp
    app.register_blueprint(inventario_bp, url_prefix='/inventario')

    return app