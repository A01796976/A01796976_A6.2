"""
Módulo para la gestión de reservaciones.
"""
import json
import os
from hotel import Hotel
from customer import Customer


class Reservation:
    """Clase para administrar reservaciones."""

    def __init__(self):
        self.filename = "reservations.json"
        self.hotel_manager = Hotel()
        self.customer_manager = Customer()

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

    def create_reservation(self, res_id, customer_id, hotel_id):
        """Crea una reservación validando existencia de cliente y hotel."""
        if not self.customer_manager.display_customer_info(customer_id):
            print(f"Cliente {customer_id} no encontrado.")
            return False
        if not self.hotel_manager.display_hotel_info(hotel_id):
            print(f"Hotel {hotel_id} no encontrado.")
            return False

        reservations = self._load_data()
        if any(r['id'] == res_id for r in reservations):
            return False

        reservations.append({
            "id": res_id,
            "customer_id": customer_id,
            "hotel_id": hotel_id
        })
        self._save_data(reservations)
        return True

    def cancel_reservation(self, res_id):
        """Cancela una reservación por ID."""
        reservations = self._load_data()
        new_res = [r for r in reservations if r['id'] != res_id]
        if len(new_res) == len(reservations):
            return False
        self._save_data(new_res)
        return True
