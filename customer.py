"""
Módulo para la gestión de clientes.
"""
import json
import os


class Customer:
    """Clase para administrar clientes y su persistencia."""

    def __init__(self):
        self.filename = "data/customers.json"

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

    def create_customer(self, customer_id, name, email):
        """Crea un nuevo cliente."""
        customers = self._load_data()
        if any(c['id'] == customer_id for c in customers):
            return False

        new_cust = {"id": customer_id, "name": name, "email": email}
        customers.append(new_cust)
        self._save_data(customers)
        return True

    def delete_customer(self, customer_id):
        """Elimina un cliente por ID."""
        customers = self._load_data()
        new_list = [c for c in customers if c['id'] != customer_id]
        if len(new_list) == len(customers):
            return False
        self._save_data(new_list)
        return True

    def display_customer_info(self, customer_id):
        """Retorna información de un cliente."""
        customers = self._load_data()
        for cust in customers:
            if cust['id'] == customer_id:
                return cust
        return None

    def modify_customer_info(self, customer_id, name=None, email=None):
        """Modifica datos del cliente."""
        customers = self._load_data()
        updated = False
        for cust in customers:
            if cust['id'] == customer_id:
                if name:
                    cust['name'] = name
                if email:
                    cust['email'] = email
                updated = True
                break
        if updated:
            self._save_data(customers)
            return True
        return False
