import re
import os
import platform


def limpiar_pantalla():
    os.system('cls') if platform.system() == "Windows" else os.system('clear')


def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    print(mensaje) if mensaje else None
    while True:
        texto = input("> ")
        if len(texto) >= longitud_min and len(texto) <= longitud_max:
            return texto


def numero_valido(dni, lista):
    if not re.match('[0-9]{4}[A-Z]{3}', dni):
        print("numero de serie incorrecto, debe cumplir el formato.")
        return False
    for cliente in lista:
        if cliente.dni == dni:
            print("numero de serie utilizado por otro cliente.")
            return False
    return True