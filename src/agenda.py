"""
27/11/2023

Práctica del examen para realizar en casa
-----------------------------------------

* El programa debe estar correctamente documentado.

* Debes intentar ajustarte lo máximo que puedas a lo que se pide en los comentarios TODO.

* Tienes libertad para desarrollar los métodos o funciones que consideres, pero estás obligado a usar como mínimo todos los que se solicitan en los comentarios TODO.

* Además, tu programa deberá pasar correctamente las pruebas unitarias que se adjuntan en el fichero test_agenda.py, por lo que estás obligado a desarrollar los métodos que se importan y prueban en la misma: pedir_email(), validar_email() y validar_telefono()

"""

import os
import pathlib
from os import path

# Constantes globales
RUTA = pathlib.Path(__file__).parent.absolute() 

NOMBRE_FICHERO = 'contactos.csv'

RUTA_FICHERO = path.join(RUTA, NOMBRE_FICHERO)

#TODO: Crear un conjunto con las posibles opciones del menú de la agenda
OPCIONES_MENU = {1, 2, 3, 4, 5, 6, 7, 8}
#TODO: Utiliza este conjunto en las funciones agenda() y pedir_opcion()


def borrar_consola():
    """ Limpia la consola
    """
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def cargar_contactos(contactos: list):
    """
    Carga los contactos iniciales de la agenda desde RUTA_FICHERO y extrae información de contacto.

    Args:
        contactos (list): Lista de diccionarios que contiene los contactos actuales.

    """
    try:
        with open(RUTA_FICHERO, 'r') as fichero:
            for linea in fichero:
                contacto = linea.split(";")
                nombre = contacto[0]
                apellidos = contacto[1]
                email = contacto[2].strip()
                telefonos = contacto[3:] if len(contacto) else []
                telefonos = [telefono.strip() for telefono in telefonos]
                diccionario = {
                    'nombre': nombre,
                    'apellido': apellidos,
                    'email': email,
                    'telefonos': telefonos
                }
                for contacto in contactos:
                    if email == contacto['email']:
                        raise NameError
                contactos.append(diccionario)
    except NameError:
        print("\n\n **CONTACTO YÁ INCLUIDO EN LA LISTA**\n\n")
    except:
        print("Fichero no válido")


def buscar_contacto(contactos:list, email:str) -> int:
    """
    Busca un contacto en la lista por su dirección de correo electrónico.
    
    Args:
        contactos (list): Lista de diccionarios que contiene los contactos.
        email (str): Dirección de correo electrónico a buscar.
        
    Returns:
        int or None: Devuelve el índice del contacto o None.
    """
    
    i = 0
    for contacto in contactos:
        if contacto['email'] == email:
            return i
        else:
            i += 1
    return None

def formatear_telefonos(telefonos: list) -> list:
    """
    Formatea una lista de números de teléfono.
    
    Args:
        telefonos (list): Lista de números de teléfono a formatear.

    Returns:
        list: Lista de números de teléfono formateados. None si la lista de teléfonos está vacía.
    """
    if telefonos == []:
        return None
    telefonos_formateado = []
    for numero in telefonos:
        numero = numero.replace(" ", "")
        if len(numero) == 12:
            telefonos_formateado.append(numero[:3] + "-" + numero[3:])
        else:
            telefonos_formateado.append(numero)
    return telefonos_formateado


def mostrar_contactos(contactos: list):
    """
    Muestra los contactos de la agenda ordenados alfabéticamente por nombre.
    
    Args:
        contactos (list): Lista de diccionarios que contiene los contactos.
    """
    nombres = []
    for contacto in contactos:
        nombres.append(contacto['nombre'])
    nombres.sort()
    print(f"AGENDA ({len(contactos)})")
    
    for nombre in nombres:
        for contacto in contactos:
            if nombre == contacto['nombre']:
                telefonos_formateados = formatear_telefonos(contacto['telefonos'])
                if telefonos_formateados == None:
                    telefonos = "Ninguno"
                else:
                    telefonos = " / ".join(telefonos_formateados)
                print("------")
                print(f"Nombre: {contacto['nombre']} {contacto['apellido']} ({contacto['email']})")
                print(f"Teléfonos: {telefonos}\n")

def eliminar_contacto(contactos: list, email: str):
    """
    Elimina un contacto de la agenda basándose en su dirección de correo electrónico.

    Args:
        contactos (list): Lista de diccionarios que contiene los contactos.
        email (str): Dirección de correo electrónico del contacto a eliminar.
    """
    try:
        pos = buscar_contacto(contactos, email)
        if pos != None:
            del contactos[pos]
            print("Se eliminó 1 contacto")
        else:
            print("No se encontró el contacto para eliminar")
    except Exception as e:
        print(f"**Error** {e}")
        print("No se eliminó ningún contacto")

def vaciar_agenda(contactos:list):
    """
    Vacia completamente la lista de contactos en la agenda.

    Args:
        contactos (list): Lista de diccionarios que contiene los contactos.
    """
    contactos.clear()
    print("--- Agenda vaciada correctamente \n\n")

def modificar_contacto(contactos:list, email:str):
    """
    Modifica un contacto en la agenda basándose en su dirección de correo electrónico.

    Args:
        contactos (list): Lista de diccionarios que contiene los contactos.
        email (str): Dirección de correo electrónico del contacto a modificar.
        
    """
    opciones = ["nombre", "apellido", "email", "telefonos"]
    try:
        pos = buscar_contacto(contactos, email)
        if pos != None:
            print("Selecciona qué quieres modificar de este contacto:")
            for i in range(1, len(opciones) + 1):
                print(f"{i}. {opciones[i - 1].capitalize()}")
            seleccion = input()
            borrar_consola()
            match seleccion:
                case "1":
                    print("--- Modificando nombre ---")
                    print(f"A qué nombre quieres cambiar {contactos[pos]['nombre']}")
                    contactos[pos]['nombre'] = pedir_nombre()
                case "2":
                    print("--- Modificando apellido ---")
                    print(f"Qué apellido le quieres poner a {contactos[pos]['nombre']}")
                    contactos[pos]['apellido'] = pedir_apellido()
                case "3":
                    print("--- Modificando email ---")
                    print(f"Qué email quieres cambiar a {contactos[pos]['email']}")
                    contactos[pos]['email'] = pedir_email(contactos)
                case "4":
                    telefonos_formateados = formatear_telefonos(contactos[pos]['telefonos'])
                    if telefonos_formateados == None:
                        telefonos = "Ninguno"
                    else:
                        telefonos = " / ".join(telefonos_formateados)
                    print("--- Modificando teléfonos ---")
                    print(f"Cambiando: {telefonos}")
                    print("Introduce TODOS LOS NÚMEROS que quieres que se guarden con el contacto")
                    contactos[pos]['telefonos'] = pedir_telefono()
                case other:
                    print("No has introducido una opción válida")
                    return
                
            print("\nContacto modificado correctamente\n\n")
            
        else:
            print("No se encontró el contacto para modificar")
    except Exception as e:
        print(f"**Error** {e}")
        print("No se modificó ningún contacto\n\n")

def mostrar_menu():
    """
    Muestra el menú de opciones para la agenda.
    """
    print("MENÚ AGENDA")
    print("------")
    print("1. Nuevo contacto")
    print("2. Modificar contacto")
    print("3. Eliminar contacto")
    print("4. Vaciar agenda")
    print("5. Cargar agenda inicial")
    print("6. Mostrar contactos por criterio")
    print("7. Mostrar la agenda completa")
    print("8. Salir")
    print()
    
def pedir_opcion():
    """
    Solicita al usuario que ingrese una opción numérica válida.

    Returns:
        int: Devuelve el número ingresado o -1 si la opción no es válida
    """
    try:
        opcion = int(input("Ingrese una opción válida: "))
        return opcion
    except ValueError:
        return -1

    
def validar_email(email:str, contactos:list):
    """
    Valida que el correo electrónico no esté vacío, contenga "@" y ".", y no exista en la lista de contactos.

    Args:
        email (str): correo electrónico a validar.
        contactos (list): Lista de diccionarios que contiene los contactos.
        
    """
    if email.strip() == "":
        raise ValueError("el email no puede ser una cadena vacía")

    if "@" not in email or "." not in email:
        raise ValueError("el email no es un correo válido")

    for contacto in contactos:
        if contacto['email'] == email:
            raise ValueError("el email ya existe en la agenda")

def pedir_email(contactos:list) -> str:
    """
    Pide al usuario que ingrese un email y lo valida utilizando la función validar_email.

    Args:
        contactos (list): Lista de diccionarios que contiene los contactos.

    Returns:
        str: correo electronico.
    """
    email = input("Ingrese un email: ")
    validar_email(email, contactos)
    return email

def pedir_nombre() -> str:
    """
    Solicita al usuario un nombre

    Returns:
        str: nombre
    """
    nombre_ok = True
    while nombre_ok:
        print("1. Introduce el nombre")
        nombre = input()
        try:
            if nombre.strip() == '' or nombre.replace(".", "").isdigit():
                raise ValueError("Nombre no válido")
            return nombre.capitalize()
        except ValueError as e:
            print(e)

def pedir_apellido() -> str:
    """
    Solicita al usuario un apellido

    Returns:
        str: apellido
    """
    apellido_ok = True
    while apellido_ok:
        print("2. Introduce el apellido")
        apellido = input()
        try:
            if apellido.strip() == '' or apellido.replace(".", "").isdigit():
                raise ValueError("Apellido no válido")
            return apellido.capitalize()
        except ValueError as e:
            print(e)
            
def validar_telefono(telefono:str) ->bool:
    """
    Valida que un teléfono debe estar compuesto solo por 9 números, aunque debe permitirse que se introduzcan espacios entre los números.
    Además, un número de teléfono puede incluir de manera opcional un prefijo +34.
    De igual manera, aunque existan espacios entre el prefijo y los 9 números al introducirlo, debe almacenarse sin espacios.
    
    Args:
        telefono (str): Cadena de número de teléfono a validar.

    Returns:
        bool: True si la cadena de número de teléfono es válida, False en caso contrario.
    """
    telefono = telefono.replace(" ", "")
    if telefono.startswith("+34"):
        if len(telefono) != 12 or telefono[4:].isdigit() == False:
            return False
        return True
    elif len(telefono) != 9 or telefono.isdigit() == False:
        return False
    else:
        return True

def pedir_telefono() -> list:
    """
    Solicita al usuario que ingrese números de teléfono hasta que introduzca el enter.

    Returns:
        list: Lista de números de teléfono validados introducidos por el usuario.
    """
    
    print("4. Introduce los telefonos <ENTER> para salir")
    telefono = input()
    lista_telefonos = []
    while telefono != "":
        if validar_telefono(telefono):
            lista_telefonos.append(telefono)
        else:
            print("Teléfono no válido")
        print("4. Introduce los telefonos <ENTER> para salir")
        telefono = input()
    return lista_telefonos

def agregar_contacto(contactos:list):
    """
    Agrega un nuevo contacto a la lista de contactos.
    """
    borrar_consola()
    print("---- Agregando contacto.....")
    try:
        nuevo_contacto = {
            'nombre': pedir_nombre(),
            'apellido': pedir_apellido(),
            'email': pedir_email(contactos),
            'telefonos': pedir_telefono()
        }
        contactos.append(nuevo_contacto)
        print("--- Contacto añadido correctamente ---")
    except ValueError as e:
        print(f"Error: {e}")
    
    
def buscar_por_criterios(contactos:list, criterio:str, busqueda:str) -> list:
    """
    Busca contactos en la lista según un criterio y un término de búsqueda

    Args:
        contactos (list): Lista de diccionarios que contiene los contactos
        criterio (str): Criterio por el cual se realizará la búsqueda
        busqueda (str): Término de búsqueda

    Returns:
        list or None: Lista de contactos que coinciden con la búsqueda. Devuelve None si no se encuentran coincidencias.
    """
    lista_contacto = []
    for contacto in contactos:
        if contacto[criterio] == busqueda:
            lista_contacto.append(contacto)
            return lista_contacto
    return None


def buscar_teléfono(contactos:list , telefono:str) -> list:
    """
    Busca contactos en la lista por número de teléfono.

    Args:
        contactos (list): Lista de diccionarios que contiene los contactos.
        telefono (str): Número de teléfono a buscar.

    Returns:
        list or None: Lista de contactos que contienen el número de teléfono buscado. Devuelve None si no se encuentran coincidencias.
    """
    lista_contacto = []
    for contacto in contactos:
        telefonos = contacto['telefonos']
        if telefono in telefonos:
            lista_contacto.append(contacto)
            return lista_contacto
    return None
        
        
def mostrar_contactos_por_criterio(contactos:list):
    """
    Muestra los contactos de la agenda dependiendo de lo que el usuario eleija

    Args:
        contactos (list): Lista de diccionarios que contiene los contactos.
    """
    opciones = ["nombre", "apellido", "email", "telefonos"]
    try:
        print("Selecciona qué quieres buscar en la agenda:")
        for i in range(1, len(opciones) + 1):
            print(f"{i}. {opciones[i - 1].capitalize()}")
        seleccion = input()
        borrar_consola()
        match seleccion:
            case "1":
                print("-- Buscando por nombre --")
                print("Introduce el nombre qué quieres buscar en la agenda: ")
                nombre = pedir_nombre()
                contacto = buscar_por_criterios(contactos, "nombre", nombre)
                mostrar_contactos(contacto)
            case "2":
                print("-- Buscando por apellido --")
                print("Introduce el apellido qué quieres buscar en la agenda: ")
                apellido = pedir_apellido()
                contacto = buscar_por_criterios(contactos, "apellido", apellido)
                mostrar_contactos(contacto)
            case "3":
                print("-- Buscando por email --")
                print("Introduce el email qué quieres buscar en la agenda: ")
                email = input()
                contacto = buscar_por_criterios(contactos, "email", email)
                mostrar_contactos(contacto)
            case "4":
                print("-- Buscando por teléfono --")
                print("Introduce el teléfono qué quieres buscar en la agenda: ")
                telefono = input()
                contacto = buscar_teléfono(contactos , telefono)
                mostrar_contactos(contacto)
            case other:
                print("No has introducido una opción válida")
                return  
    except:
        print("No se encontró el contacto a buscar \n\n")
      
def agenda(contactos: list):
    """ 
    Ejecuta el menú de la agenda con varias opciones
    
    Args:
        contactos (list): Lista de diccionarios que contiene los contactos.

    """
    opcion = pedir_opcion()
    while opcion != 8:
        if opcion in OPCIONES_MENU - {8}:
            borrar_consola()
            if opcion == 1:
                agregar_contacto(contactos)
            elif opcion == 2:
                email = input("Introduce el email del usuario a modificar: ")
                modificar_contacto(contactos, email)
            elif opcion == 3:
                email = input("Introduce el email a eliminar: ")
                eliminar_contacto(contactos, email)
            elif opcion == 4:
                vaciar_agenda(contactos)
            elif opcion == 5:
                cargar_contactos(contactos)
            elif opcion == 6:
                mostrar_contactos_por_criterio(contactos)
            elif opcion == 7:
                mostrar_contactos(contactos)

            mostrar_menu()
            opcion = pedir_opcion()
        else:
            opcion = pedir_opcion()
    print("-- Hasta luego! ---")


def pulse_tecla_para_continuar():
    """ 
    Muestra un mensaje y realiza una pausa hasta que se pulse una tecla
    """
    print("\n Pulsa una tecla para continuar....")
    input()


def main():
    """ 
    Función principal del programa
    """
    contactos = []
    
    cargar_contactos(contactos)
    
    agregar_contacto(contactos)
    pulse_tecla_para_continuar()
    borrar_consola()
    
    eliminar_contacto(contactos, "rciruelo@gmail.com")
    pulse_tecla_para_continuar()
    borrar_consola()
    
    mostrar_contactos(contactos)
    pulse_tecla_para_continuar()
    borrar_consola()
    
    mostrar_menu()
    agenda(contactos)



if __name__ == "__main__":
    main()