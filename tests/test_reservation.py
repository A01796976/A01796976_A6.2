import unittest
import os
from hotel import Hotel
from customer import Customer
from reservation import Reservation

class TestReservation(unittest.TestCase):
    def setUp(self):
        """Configuración previa a cada test."""
        self.hotel = Hotel()
        self.customer = Customer()
        self.reservation = Reservation()

        # Usar archivos de prueba para no corromper datos reales
        self.hotel.filename = "test_hotels.json"
        self.customer.filename = "test_customers.json"
        self.reservation.filename = "test_reservations.json"

    def tearDown(self):
        """Limpieza después de cada test."""
        for file in ["test_hotels.json", "test_customers.json", 
                     "test_reservations.json"]:
            if os.path.exists(file):
                os.remove(file)
                
  # --- PRUEBAS DE RESERVACIÓN ---
    def test_reservation_creation(self):
        """Prueba crear reservación exitosa."""
        # Pre-requisitos: Hotel y Cliente deben existir
        self.hotel.create_hotel(1, "H1", "L1", 5)
        self.customer.create_customer(100, "C1", "E1")
        
        self.assertTrue(self.reservation.create_reservation("R1", 100, 1))
        
        # Verificar duplicado
        self.assertFalse(self.reservation.create_reservation("R1", 100, 1))

    def test_reservation_invalid_entities(self):
        """Prueba fallos por falta de hotel o cliente."""
        self.hotel.create_hotel(1, "H1", "L1", 5)
        # Cliente no existe
        self.assertFalse(self.reservation.create_reservation("R2", 999, 1))

    def test_cancel_reservation(self):
        """Prueba cancelar reservación."""
        self.hotel.create_hotel(1, "H1", "L1", 5)
        self.customer.create_customer(100, "C1", "E1")
        self.reservation.create_reservation("R1", 100, 1)
        
        self.assertTrue(self.reservation.cancel_reservation("R1"))
        self.assertFalse(self.reservation.cancel_reservation("R99"))

    def test_file_errors(self):
        """Prueba manejo de archivos corruptos (Req 5)."""
        with open("test_hotels.json", "w") as f:
            f.write("{bad json")
        # No debe crashear, retorna lista vacía o None
        self.assertIsNone(self.hotel.display_hotel_info(1))

if __name__ == "__main__":
    unittest.main()