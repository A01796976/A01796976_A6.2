"""
Módulo para la gestión de hoteles.
"""
import json
import os


class Hotel:
    """Clase para administrar hoteles y su persistencia."""

    def __init__(self):
        self.filename = "data/hotels.json"

    def _load_data(self):
        """Carga datos del archivo JSON."""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_data(self, data):
        """Guarda datos en el archivo JSON."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
        except IOError:
            print(f"Error al guardar en {self.filename}")

    def create_hotel(self, hotel_id, name, location, rooms):
        """Crea un nuevo hotel si no existe."""
        hotels = self._load_data()
        if any(h['id'] == hotel_id for h in hotels):
            print(f"Hotel {hotel_id} ya existe.")
            return False

        new_hotel = {
            "id": hotel_id,
            "name": name,
            "location": location,
            "rooms": rooms
        }
        hotels.append(new_hotel)
        self._save_data(hotels)
        return True

    def delete_hotel(self, hotel_id):
        """Elimina un hotel por ID."""
        hotels = self._load_data()
        original_count = len(hotels)
        hotels = [h for h in hotels if h['id'] != hotel_id]

        if len(hotels) == original_count:
            return False

        self._save_data(hotels)
        return True

    def display_hotel_info(self, hotel_id):
        """Retorna información de un hotel."""
        hotels = self._load_data()
        for hotel in hotels:
            if hotel['id'] == hotel_id:
                return hotel
        return None

    def modify_hotel_info(self, hotel_id, name=None, location=None):
        """Modifica atributos de un hotel."""
        hotels = self._load_data()
        updated = False
        for hotel in hotels:
            if hotel['id'] == hotel_id:
                if name:
                    hotel['name'] = name
                if location:
                    hotel['location'] = location
                updated = True
                break

        if updated:
            self._save_data(hotels)
            return True
        return False
