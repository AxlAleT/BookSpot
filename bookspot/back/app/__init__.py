from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from app.core.config import Config
from flask_session import Session

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config.get_instance())
    app.config['DEBUG'] = True  # Habilitar modo debug

    CORS(app, supports_credentials=True)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)  

    Session(app)

    from app.api.auth.router import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.api.ventas.router import ventas_bp
    app.register_blueprint(ventas_bp, url_prefix='/ventas')
    from app.api.inventario.router import inventario_bp
    app.register_blueprint(inventario_bp, url_prefix='/inventario')
    from app.api.apartados.router import apartados_bp
    app.register_blueprint(apartados_bp, url_prefix='/apartado')
    return app