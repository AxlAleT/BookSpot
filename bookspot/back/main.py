from app import create_app
from app.core.base import init_db, populate_books

app = create_app()

with app.app_context():
    init_db()
    populate_books()

if __name__ == '__main__':
    app.run(debug=True)
