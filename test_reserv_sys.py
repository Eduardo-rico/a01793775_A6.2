import os
import json
import unittest
import reservation_system as rs


class PruebasSistemaReservas(unittest.TestCase):

    def setUp(self):
        self.archivo_hoteles = "prueba_hoteles.json"
        self.archivo_clientes = "prueba_clientes.json"
        self.archivo_reservas = "prueba_reservas.json"

        rs.ARCHIVO_HOTELES = self.archivo_hoteles
        rs.ARCHIVO_CLIENTES = self.archivo_clientes
        rs.ARCHIVO_RESERVAS = self.archivo_reservas

        with open(self.archivo_hoteles, "w", encoding="utf-8") as f:
            json.dump([], f)
        with open(self.archivo_clientes, "w", encoding="utf-8") as f:
            json.dump([], f)
        with open(self.archivo_reservas, "w", encoding="utf-8") as f:
            json.dump([], f)

    def tearDown(self):
        for archivo in (self.archivo_hoteles, self.archivo_clientes, self.archivo_reservas):
            if os.path.exists(archivo):
                os.remove(archivo)
        # Restablecer los nombres de archivo por defecto.
        rs.ARCHIVO_HOTELES = "hoteles.json"
        rs.ARCHIVO_CLIENTES = "clientes.json"
        rs.ARCHIVO_RESERVAS = "reservas.json"

    def test_crear_y_mostrar_hotel(self):
        hotel = rs.Hotel.crear_hotel(rs.Hotel(10, "Hotel Prueba", "Dirección Prueba", 80, 80))
        info = rs.Hotel.mostrar_hotel(10)
        self.assertIsNotNone(info)
        self.assertEqual(info["nombre"], "Hotel Prueba")

    def test_modificar_hotel_inexistente(self):
        rs.Hotel.modificar_hotel(999, nombre="Hotel Inexistente")
        info = rs.Hotel.mostrar_hotel(999)
        self.assertIsNone(info)

    def test_eliminar_hotel(self):
        rs.Hotel.crear_hotel(rs.Hotel(11, "Hotel A Eliminar", "Dirección A", 50, 50))
        rs.Hotel.eliminar_hotel(11)
        info = rs.Hotel.mostrar_hotel(11)
        self.assertIsNone(info)

    def test_reservar_y_cancelar_habitacion(self):
        # Probar la reserva y cancelación de una habitación.
        rs.Hotel.crear_hotel(rs.Hotel(12, "Hotel Reserva", "Dirección Reserva", 20, 20))
        resultado_reserva = rs.Hotel.reservar_habitacion(12)
        self.assertTrue(resultado_reserva)
        info = rs.Hotel.mostrar_hotel(12)
        self.assertEqual(info["habitaciones_disponibles"], 19)
        resultado_cancelacion = rs.Hotel.cancelar_reserva(12)
        self.assertTrue(resultado_cancelacion)
        info = rs.Hotel.mostrar_hotel(12)
        self.assertEqual(info["habitaciones_disponibles"], 20)

    def test_crear_y_eliminar_cliente(self):
        # Crear un cliente y comprobar su eliminación.
        rs.Cliente.crear_cliente(rs.Cliente(20, "María López", "maria@example.com"))
        cliente = rs.Cliente.mostrar_cliente(20)
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente["nombre"], "María López")
        rs.Cliente.eliminar_cliente(20)
        cliente = rs.Cliente.mostrar_cliente(20)
        self.assertIsNone(cliente)

    def test_crear_y_cancelar_reserva(self):
        rs.Hotel.crear_hotel(rs.Hotel(13, "Hotel Reserva Prueba", "Dirección 13", 30, 30))
        rs.Cliente.crear_cliente(rs.Cliente(30, "Carlos Ruiz", "carlos@example.com"))
        reserva = rs.Reserva.crear_reserva(30, 13)
        self.assertIsNotNone(reserva)
        cancelacion = rs.Reserva.cancelar_reserva(reserva.id)
        self.assertTrue(cancelacion)

    def test_reserva_fallida_por_no_disponibilidad(self):
        rs.Hotel.crear_hotel(rs.Hotel(14, "Hotel Sin Disponibilidad", "Dirección 14", 10, 0))
        rs.Cliente.crear_cliente(rs.Cliente(40, "David Gómez", "david@example.com"))
        reserva = rs.Reserva.crear_reserva(40, 14)
        self.assertIsNone(reserva)

    def test_cancelar_reserva_inexistente(self):
        # Intentar cancelar una reserva que no existe.
        resultado = rs.Reserva.cancelar_reserva(999)
        self.assertFalse(resultado)


if __name__ == "__main__":
    unittest.main()
