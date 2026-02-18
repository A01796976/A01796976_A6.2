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
        
    def test_create_duplicate_customer(self):
        """Cubre la línea 36: Intentar crear un cliente duplicado."""
        self.customer.create_customer(1, "Ana", "ana@mail.com")
        # Intentamos crear el mismo ID de nuevo
        result = self.customer.create_customer(1, "Ana Duplicada", "ana2@mail.com")
        self.assertFalse(result)

    def test_modify_email_only(self):
        """Cubre la línea 67: Modificar solo el email."""
        self.customer.create_customer(2, "Beto", "beto@mail.com")
        # Enviamos name=None para que solo entre al if del email
        self.customer.modify_customer_info(2, email="beto_nuevo@mail.com")
        
        info = self.customer.display_customer_info(2)
        self.assertEqual(info['email'], "beto_nuevo@mail.com")
        self.assertEqual(info['name'], "Beto") # El nombre no debió cambiar

    def test_modify_non_existent_customer(self):
        """Cubre la línea 75: Intentar modificar un cliente que no existe."""
        result = self.customer.modify_customer_info(999, name="Fantasma")
        self.assertFalse(result)

    def test_invalid_json_file(self):
        """Cubre líneas 21-22: Archivo corrupto."""
        # Creamos un archivo basura
        with open("test_customers.json", "w") as f:
            f.write("Esto no es un JSON")
        
        # Debe manejar el error y retornar None o lista vacía sin tronar
        result = self.customer.display_customer_info(1)
        self.assertIsNone(result)
        
if __name__ == "__main__":
    unittest.main()