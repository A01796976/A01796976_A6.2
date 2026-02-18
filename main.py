"""
Programa principal (Main) para ejecutar el Sistema de Reservaciones.
Permite la interacción con el usuario a través de la consola.
"""
import sys
from hotel import Hotel
from customer import Customer
from reservation import Reservation


def print_menu():
    """Imprime las opciones del menú."""
    print("\n--- SISTEMA DE RESERVACIONES ---")
    print("1. Crear Hotel")
    print("2. Mostrar Hotel")
    print("3. Modificar Hotel")
    print("4. Borrar Hotel")
    print("----------------")
    print("5. Crear Cliente")
    print("6. Mostrar Cliente")
    print("7. Modificar Cliente")
    print("8. Borrar Cliente")
    print("----------------")
    print("9. Crear Reservación")
    print("10. Cancelar Reservación")
    print("----------------")
    print("0. Salir")


def main():
    """Función principal de ejecución."""
    hotel_sys = Hotel()
    customer_sys = Customer()
    reservation_sys = Reservation()

    while True:
        print_menu()
        option = input("Selecciona una opción: ")

        # --- GESTIÓN DE HOTELES ---
        if option == '1':
            try:
                hid = int(input("ID del Hotel (número): "))
                name = input("Nombre del Hotel: ")
                loc = input("Ubicación: ")
                rooms = int(input("Número de habitaciones: "))
                if hotel_sys.create_hotel(hid, name, loc, rooms):
                    print(">> Hotel creado exitosamente.")
                else:
                    print(">> Error: El ID ya existe.")
            except ValueError:
                print(">> Error: ID y Habitaciones deben ser números.")

        elif option == '2':
            try:
                hid = int(input("ID del Hotel a buscar: "))
                info = hotel_sys.display_hotel_info(hid)
                if info:
                    print(f">> Info: {info}")
                else:
                    print(">> Hotel no encontrado.")
            except ValueError:
                print(">> Error: El ID debe ser un número.")

        elif option == '3':
            try:
                hid = int(input("ID del Hotel a modificar: "))
                name = input("Nuevo nombre (Enter para omitir): ")
                loc = input("Nueva ubicación (Enter para omitir): ")
                # Convertir cadenas vacías a None
                name = name if name else None
                loc = loc if loc else None
                
                if hotel_sys.modify_hotel_info(hid, name, loc):
                    print(">> Hotel modificado correctamente.")
                else:
                    print(">> No se pudo modificar (ID no existe).")
            except ValueError:
                print(">> Error: El ID debe ser un número.")

        elif option == '4':
            try:
                hid = int(input("ID del Hotel a borrar: "))
                if hotel_sys.delete_hotel(hid):
                    print(">> Hotel eliminado.")
                else:
                    print(">> Hotel no encontrado.")
            except ValueError:
                print(">> Error: El ID debe ser un número.")

        # --- GESTIÓN DE CLIENTES ---
        elif option == '5':
            try:
                cid = int(input("ID del Cliente (número): "))
                name = input("Nombre del Cliente: ")
                email = input("Email: ")
                if customer_sys.create_customer(cid, name, email):
                    print(">> Cliente creado exitosamente.")
                else:
                    print(">> Error: El ID ya existe.")
            except ValueError:
                print(">> Error: El ID debe ser un número.")

        elif option == '6':
            try:
                cid = int(input("ID del Cliente a buscar: "))
                info = customer_sys.display_customer_info(cid)
                if info:
                    print(f">> Cliente: {info}")
                else:
                    print(">> Cliente no encontrado.")
            except ValueError:
                print(">> Error: El ID debe ser un número.")

        elif option == '7':
            try:
                cid = int(input("ID del Cliente a modificar: "))
                name = input("Nuevo nombre (Enter para omitir): ")
                email = input("Nuevo Email (Enter para omitir): ")
                name = name if name else None
                email = email if email else None

                if customer_sys.modify_customer_info(cid, name, email):
                    print(">> Cliente modificado.")
                else:
                    print(">> No se pudo modificar (ID no existe).")
            except ValueError:
                print(">> Error: El ID debe ser un número.")

        elif option == '8':
            try:
                cid = int(input("ID del Cliente a borrar: "))
                if customer_sys.delete_customer(cid):
                    print(">> Cliente eliminado.")
                else:
                    print(">> Cliente no encontrado.")
            except ValueError:
                print(">> Error: El ID debe ser un número.")

        # --- GESTIÓN DE RESERVACIONES ---
        elif option == '9':
            try:
                rid = input("ID de Reservación (ej. RES-01): ")
                cid = int(input("ID del Cliente: "))
                hid = int(input("ID del Hotel: "))
                
                if reservation_sys.create_reservation(rid, cid, hid):
                    print(">> Reservación creada exitosamente.")
                else:
                    print(">> Error: Verifique que Cliente/Hotel existan "
                          "o que la reservación no esté duplicada.")
            except ValueError:
                print(">> Error: IDs de Cliente y Hotel deben ser números.")

        elif option == '10':
            rid = input("ID de Reservación a cancelar: ")
            if reservation_sys.cancel_reservation(rid):
                print(">> Reservación cancelada.")
            else:
                print(">> Reservación no encontrada.")

        elif option == '0':
            print("Saliendo del sistema...")
            sys.exit()

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()