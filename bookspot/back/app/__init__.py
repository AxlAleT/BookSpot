from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('app.core.config.Config')

    db.init_app(app)
    ma.init_app(app)

    from app.api.ventas.router import ventas_bp
    app.register_blueprint(ventas_bp, url_prefix='/ventas')

    # Registrar otros blueprints de la misma manera
    # from app.api.inventario.router import inventario_bp
    # app.register_blueprint(inventario_bp, url_prefix='/inventario')

    return app
