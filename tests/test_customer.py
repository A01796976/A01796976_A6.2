import unittest
import os
from customer import Customer

class TestCustomer(unittest.TestCase):
    def setUp(self):
        """Configuración previa a cada test."""
        self.customer = Customer()
    

        # Usar archivos de prueba para no corromper datos reales
        self.customer.filename = "test_customers.json"

    def tearDown(self):
        """Limpieza después de cada test."""
        for file in ["test_hotels.json", "test_customers.json", 
                     "test_reservations.json"]:
            if os.path.exists(file):
                os.remove(file)
                
    # --- PRUEBAS DE CLIENTES ---
    def test_customer_management(self):
        """Prueba creación, lectura y borrado de cliente."""
        self.assertTrue(self.customer.create_customer(10, "Juan", "j@m.c"))
        
        info = self.customer.display_customer_info(10)
        self.assertEqual(info['email'], "j@m.c")
        
        self.assertTrue(self.customer.modify_customer_info(10, email="x@m.c"))
        self.assertEqual(self.customer.display_customer_info(10)['email'], 
                         "x@m.c")
        
        self.assertTrue(self.customer.delete_customer(10))

    def test_customer_failures(self):
        """Pruebas de fallo en clientes."""
        self.assertIsNone(self.customer.display_customer_info(99))
        self.assertFalse(self.customer.delete_customer(99))
        
if __name__ == "__main__":
    unittest.main()