from app import create_app
from app.core.base import init_db, populate_books, init_tipos_movimiento, init_metodos_pago

app = create_app()

with app.app_context():
    init_db()
    #populate_books()
    init_tipos_movimiento()
    init_metodos_pago()

if __name__ == '__main__':
    app.run(debug=True)
