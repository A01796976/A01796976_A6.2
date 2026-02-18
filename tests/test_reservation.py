"""
Módulo de pruebas para el sistema de reservaciones.
"""
import unittest
import os
from reservation import Reservation


class TestReservation(unittest.TestCase):
    """
    Suite de pruebas para validar la lógica de creación y
    cancelación de reservaciones.
    """
    def setUp(self):
        """Configuración previa a cada test."""
        self.reservation = Reservation()

        # Usar archivos de prueba para no corromper datos reales
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
        self.assertTrue(self.reservation.create_reservation("R1", 1, 1))

        # Verificar duplicado
        self.assertFalse(self.reservation.create_reservation("R1", 1, 1))

    def test_reservation_invalid_entities(self):
        """Prueba fallos por falta de hotel o cliente."""
        # Cliente no existe
        self.assertFalse(self.reservation.create_reservation("R2", 999, 1))

    def test_cancel_reservation(self):
        """Prueba cancelar reservación."""
        self.reservation.create_reservation("R1", 1, 1)

        self.assertTrue(self.reservation.cancel_reservation("R1"))
        self.assertFalse(self.reservation.cancel_reservation("R99"))


if __name__ == "__main__":
    unittest.main()
