import unittest
import os
from hotel import Hotel

class TestHotel(unittest.TestCase):
    def setUp(self):
        """Configuración previa a cada test."""
        self.hotel = Hotel()
    

        # Usar archivos de prueba para no corromper datos reales
        self.hotel.filename = "test_hotels.json"

    def tearDown(self):
        """Limpieza después de cada test."""
        for file in ["test_hotels.json", "test_customers.json", 
                     "test_reservations.json"]:
            if os.path.exists(file):
                os.remove(file)
                
    # --- PRUEBAS DE HOTEL ---
    def test_hotel_management(self):
        """Prueba creación, lectura y borrado de hotel."""
        self.assertTrue(self.hotel.create_hotel(1, "Hotel A", "Mex", 10))
        # Intentar duplicado
        self.assertFalse(self.hotel.create_hotel(1, "Hotel A", "Mex", 10))
        
        info = self.hotel.display_hotel_info(1)
        self.assertEqual(info['name'], "Hotel A")
        
        self.assertTrue(self.hotel.modify_hotel_info(1, name="Hotel B"))
        self.assertEqual(self.hotel.display_hotel_info(1)['name'], "Hotel B")
        
        self.assertTrue(self.hotel.delete_hotel(1))
        self.assertFalse(self.hotel.delete_hotel(99))

    def test_hotel_not_found(self):
        """Prueba buscar hotel inexistente."""
        self.assertIsNone(self.hotel.display_hotel_info(99))

if __name__ == "__main__":
    unittest.main()