# pylint: disable=missing-module-docstring, missing-class-docstring
"""
Módulo de pruebas para el sistema de reservaciones.
"""
import unittest
import os

from hotel import Hotel
from customer import Customer
from reservation import Reservation


class TestAllSystem(unittest.TestCase):
    """
    Suite de pruebas para validar la totalidad de la
    logica
    """

    def setUp(self):
        """Configura el entorno antes de CADA prueba."""
        # Nombres de archivos de prueba
        self.hotel_file = "test_hotels.json"
        self.cust_file = "test_customers.json"
        self.res_file = "test_reservations.json"

        # Inicializar las instancias
        self.hotel = Hotel()
        self.customer = Customer()
        self.reservation = Reservation()

        # --- TRUCO IMPORTANTE ---
        # Forzamos a que TODOS usen los archivos de prueba.
        # Incluso los gestores internos dentro de la clase Reservation.
        self.hotel.filename = self.hotel_file
        self.customer.filename = self.cust_file
        self.reservation.filename = self.res_file
        self.reservation.hotel_manager.filename = self.hotel_file
        self.reservation.customer_manager.filename = self.cust_file

    def tearDown(self):
        """Borra los archivos basura después de cada prueba."""
        for f in [self.hotel_file, self.cust_file, self.res_file]:
            if os.path.exists(f):
                os.remove(f)

    # ==========================================
    # PRUEBAS DE HOTEL (Para cubrir hotel.py)
    # ==========================================
    def test_hotel_full_lifecycle(self):
        """1. Crear"""
        self.assertTrue(self.hotel.create_hotel(1, "Hotel Test", "MX", 10))
        self.assertFalse(
            self.hotel.create_hotel(1, "Duplicado", "MX", 10)
        )  # Fallo intencional

        # 2. Mostrar
        info = self.hotel.display_hotel_info(1)
        self.assertEqual(info["name"], "Hotel Test")
        self.assertIsNone(self.hotel.display_hotel_info(999))

        # 3. Modificar
        self.assertTrue(
            self.hotel.modify_hotel_info(1, name="Hotel Mod", location="US")
        )
        self.assertEqual(self.hotel.display_hotel_info(1)["location"], "US")
        self.assertFalse(
            self.hotel.modify_hotel_info(999, name="Fantasma")
        )  # No existe

        # 4. Eliminar
        self.assertTrue(self.hotel.delete_hotel(1))
        self.assertFalse(self.hotel.delete_hotel(1))  # Ya no existe

    def test_hotel_file_errors(self):
        """Crear archivo corrupto para probar manejo de errores"""
        with open(self.hotel_file, "w", encoding="utf-8") as f:
            f.write("{ json invalido")
        self.assertIsNone(self.hotel.display_hotel_info(1))

    # ==========================================
    # PRUEBAS DE CLIENTE (Para cubrir customer.py)
    # ==========================================
    def test_customer_full_lifecycle(self):
        """1. Crear"""
        self.assertTrue(self.customer.create_customer(10, "Ana", "a@a.com"))
        self.assertFalse(self.customer.create_customer(10, "Ana", "a@a.com"))
        customer_info = self.customer.display_customer_info(10)
        # 2. Mostrar
        self.assertEqual(customer_info["name"], "Ana")
        self.assertIsNone(self.customer.display_customer_info(999))

        # 3. Modificar
        result = self.customer.modify_customer_info(10, email="b@b.com")
        self.assertTrue(result)
        self.assertEqual(customer_info["email"], "b@b.com")
        result = self.customer.modify_customer_info(999, name="Nadie")
        self.assertFalse(result)

        # 4. Eliminar
        self.assertTrue(self.customer.delete_customer(10))
        self.assertFalse(self.customer.delete_customer(10))

    def test_customer_file_errors(self):
        """validacion de archivo"""
        with open(self.cust_file, "w", encoding="utf-8") as f:
            f.write("basura")
        self.assertIsNone(self.customer.display_customer_info(1))

    # ==========================================
    # PRUEBAS DE RESERVACIÓN (Para cubrir reservation.py)
    # ==========================================
    def test_reservation_lifecycle(self):
        """Pre-requisitos: Crear Hotel y Cliente en los archivos de prueba"""
        self.hotel.create_hotel(1, "H1", "L1", 5)
        self.customer.create_customer(100, "C1", "E1")
        # 1. Crear Reservación Exita
        self.assertTrue(self.reservation.create_reservation("RES1", 100, 1))
        # 2. Crear Reservación Fallida (Duplicada)
        self.assertFalse(self.reservation.create_reservation("RES1", 100, 1))
        # 3. Crear Reservación Fallida (Datos no existen)
        self.assertFalse(
            self.reservation.create_reservation("RES2", 999, 1)
        )  # Cliente no existe
        self.assertFalse(
            self.reservation.create_reservation("RES3", 100, 999)
        )  # Hotel no existe
        # 4. Cancelar
        self.assertTrue(self.reservation.cancel_reservation("RES1"))
        self.assertFalse(self.reservation.cancel_reservation("RES1"))

    def test_reservation_file_errors(self):
        """Archivo corrupto"""
        with open(self.res_file, "w", encoding="utf-8") as f:
            f.write("corrupto")
        self.assertFalse(self.reservation.cancel_reservation("RES1"))


if __name__ == "__main__":
    unittest.main()
