from flask import jsonify

class BookNotFoundException(Exception):
    def __init__(self, book_id: int):
        self.response = jsonify({
            "error": "BookNotFound",
            "message": f"Libro no encontrado con ID: {book_id}"
        })
        self.response.status_code = 404

class NotEnoughStockException(Exception):
    def __init__(self, book_id: int, requested_quantity: int, available_quantity: int):
        self.response = jsonify({
            "error": "NotEnoughStock",
            "message": (f"No hay suficiente stock para el libro con ID: {book_id}. "
                        f"Solicitaste {requested_quantity}, pero solo hay {available_quantity} disponibles.")
        })
        self.response.status_code = 400

from flask import jsonify

class InvalidRequestException(Exception):
    def __init__(self, message="InvalidRequest"):
        super().__init__(message)  # Esto establece el mensaje de la excepción base.
        self.response = jsonify({
            "error": message,  # Usa el mensaje personalizado o el predeterminado.
        })
        self.response.status_code = 400