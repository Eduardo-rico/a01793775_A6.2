#!/usr/bin/env python3
"""
Programa: reservation_system.py

Descripción:
    Este programa implementa un sistema de reservas simple con tres
    abstracciones principales: Hotel, Cliente y Reserva. Los datos se
    persisten en archivos JSON. El programa soporta los siguientes
    comportamientos persistentes:

    Hoteles:
      - Crear hotel
      - Eliminar hotel
      - Mostrar información del hotel
      - Modificar información del hotel
      - Reservar una habitación
      - Cancelar una reserva

    Clientes:
      - Crear cliente
      - Eliminar cliente
      - Mostrar información del cliente
      - Modificar información del cliente

    Reservas:
      - Crear una reserva (vinculando un cliente y un hotel)
      - Cancelar una reserva

    Los datos inválidos se manejan mostrando mensajes de error en la
    consola, sin detener la ejecución.

Uso:
    Ejecuta el módulo como script para ver una demostración simple:
    python reservation_system.py
"""

import json
import os

# Nombres de los archivos para persistencia
ARCHIVO_HOTELES = "hoteles.json"
ARCHIVO_CLIENTES = "clientes.json"
ARCHIVO_RESERVAS = "reservas.json"


class Hotel:
    def __init__(self, id_hotel, nombre, direccion, total_habitaciones,
                 habitaciones_disponibles):
        self.id = id_hotel
        self.nombre = nombre
        self.direccion = direccion
        self.total_habitaciones = total_habitaciones
        self.habitaciones_disponibles = habitaciones_disponibles

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "total_habitaciones": self.total_habitaciones,
            "habitaciones_disponibles": self.habitaciones_disponibles,
        }

    @staticmethod
    def cargar_hoteles():
        try:
            with open(ARCHIVO_HOTELES, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    @staticmethod
    def guardar_hoteles(hoteles):
        try:
            with open(ARCHIVO_HOTELES, "w", encoding="utf-8") as f:
                json.dump(hoteles, f, indent=4)
        except Exception as e:
            print(f"Error al guardar hoteles: {e}")

    @staticmethod
    def crear_hotel(hotel):
        hoteles = Hotel.cargar_hoteles()
        hoteles.append(hotel.a_diccionario())
        Hotel.guardar_hoteles(hoteles)
        return hotel

    @staticmethod
    def eliminar_hotel(id_hotel):
        hoteles = Hotel.cargar_hoteles()
        nuevos_hoteles = [h for h in hoteles if h.get("id") != id_hotel]
        if len(nuevos_hoteles) == len(hoteles):
            print(f"Hotel con id {id_hotel} no encontrado.")
        Hotel.guardar_hoteles(nuevos_hoteles)

    @staticmethod
    def mostrar_hotel(id_hotel):
        hoteles = Hotel.cargar_hoteles()
        for h in hoteles:
            if h.get("id") == id_hotel:
                return h
        print(f"Hotel con id {id_hotel} no encontrado.")
        return None

    @staticmethod
    def modificar_hotel(id_hotel, **kwargs):
        hoteles = Hotel.cargar_hoteles()
        modificado = False
        for h in hoteles:
            if h.get("id") == id_hotel:
                for clave, valor in kwargs.items():
                    if clave in h:
                        h[clave] = valor
                modificado = True
                break
        if not modificado:
            print(f"Hotel con id {id_hotel} no encontrado.")
        Hotel.guardar_hoteles(hoteles)

    @staticmethod
    def reservar_habitacion(id_hotel):
        hoteles = Hotel.cargar_hoteles()
        modificado = False
        for h in hoteles:
            if h.get("id") == id_hotel:
                if h.get("habitaciones_disponibles", 0) > 0:
                    h["habitaciones_disponibles"] -= 1
                    modificado = True
                else:
                    print("No hay habitaciones disponibles para reservar.")
                break
        if not modificado:
            print(f"Hotel con id {id_hotel} no encontrado o sin habitaciones.")
        Hotel.guardar_hoteles(hoteles)
        return modificado

    @staticmethod
    def cancelar_reserva(id_hotel):
        hoteles = Hotel.cargar_hoteles()
        modificado = False
        for h in hoteles:
            if h.get("id") == id_hotel:
                if h.get("habitaciones_disponibles", 0) < h.get("total_habitaciones", 0):
                    h["habitaciones_disponibles"] += 1
                    modificado = True
                else:
                    print("Todas las habitaciones ya están disponibles.")
                break
        if not modificado:
            print(f"Hotel con id {id_hotel} no encontrado.")
        Hotel.guardar_hoteles(hoteles)
        return modificado


class Cliente:
    def __init__(self, id_cliente, nombre, correo):
        self.id = id_cliente
        self.nombre = nombre
        self.correo = correo

    def a_diccionario(self):
        return {"id": self.id, "nombre": self.nombre, "correo": self.correo}

    @staticmethod
    def cargar_clientes():
        try:
            with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    @staticmethod
    def guardar_clientes(clientes):
        try:
            with open(ARCHIVO_CLIENTES, "w", encoding="utf-8") as f:
                json.dump(clientes, f, indent=4)
        except Exception as e:
            print(f"Error al guardar clientes: {e}")

    @staticmethod
    def crear_cliente(cliente):
        clientes = Cliente.cargar_clientes()
        clientes.append(cliente.a_diccionario())
        Cliente.guardar_clientes(clientes)
        return cliente

    @staticmethod
    def eliminar_cliente(id_cliente):
        clientes = Cliente.cargar_clientes()
        nuevos_clientes = [c for c in clientes if c.get("id") != id_cliente]
        if len(nuevos_clientes) == len(clientes):
            print(f"Cliente con id {id_cliente} no encontrado.")
        Cliente.guardar_clientes(nuevos_clientes)

    @staticmethod
    def mostrar_cliente(id_cliente):
        clientes = Cliente.cargar_clientes()
        for c in clientes:
            if c.get("id") == id_cliente:
                return c
        print(f"Cliente con id {id_cliente} no encontrado.")
        return None

    @staticmethod
    def modificar_cliente(id_cliente, **kwargs):
        clientes = Cliente.cargar_clientes()
        modificado = False
        for c in clientes:
            if c.get("id") == id_cliente:
                for clave, valor in kwargs.items():
                    if clave in c:
                        c[clave] = valor
                modificado = True
                break
        if not modificado:
            print(f"Cliente con id {id_cliente} no encontrado.")
        Cliente.guardar_clientes(clientes)


class Reserva:
    def __init__(self, id_reserva, id_cliente, id_hotel):
        self.id = id_reserva
        self.id_cliente = id_cliente
        self.id_hotel = id_hotel

    def a_diccionario(self):
        return {
            "id": self.id,
            "id_cliente": self.id_cliente,
            "id_hotel": self.id_hotel,
        }

    @staticmethod
    def cargar_reservas():
        try:
            with open(ARCHIVO_RESERVAS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    @staticmethod
    def guardar_reservas(reservas):
        try:
            with open(ARCHIVO_RESERVAS, "w", encoding="utf-8") as f:
                json.dump(reservas, f, indent=4)
        except Exception as e:
            print(f"Error al guardar reservas: {e}")

    @staticmethod
    def crear_reserva(id_cliente, id_hotel):
        # Primero, intenta reservar una habitación en el hotel.
        if not Hotel.reservar_habitacion(id_hotel):
            print("Error: No se pudo reservar habitación. Reserva no creada.")
            return None
        reservas = Reserva.cargar_reservas()
        id_reserva = (
            max([r.get("id", 0) for r in reservas]) + 1
            if reservas
            else 1
        )
        reserva = Reserva(id_reserva, id_cliente, id_hotel)
        reservas.append(reserva.a_diccionario())
        Reserva.guardar_reservas(reservas)
        return reserva

    @staticmethod
    def cancelar_reserva(id_reserva):
        reservas = Reserva.cargar_reservas()
        reserva_a_cancelar = None
        for r in reservas:
            if r.get("id") == id_reserva:
                reserva_a_cancelar = r
                break
        if reserva_a_cancelar is None:
            print(f"Reserva con id {id_reserva} no encontrada.")
            return False
        id_hotel = reserva_a_cancelar.get("id_hotel")
        if not Hotel.cancelar_reserva(id_hotel):
            print("Error: No se pudo cancelar la reserva en el hotel.")
        reservas = [r for r in reservas if r.get("id") != id_reserva]
        Reserva.guardar_reservas(reservas)
        return True


def main():
    print("Demostración del Sistema de Reservas")
    hotel = Hotel.crear_hotel(
        Hotel(100, "hotel 100", "Calle general 123", 200, 100)
    )
    cliente = Cliente.crear_cliente(
        Cliente(1, "juan pérez", "juanperez@gmail.com")
    )
    reserva = Reserva.crear_reserva(cliente.id, hotel.id)
    if reserva:
        print("Reserva creada con éxito:")
        print(reserva.a_diccionario())
    else:
        print("Error: No se pudo crear la reserva.")


if __name__ == "__main__":
    main()
