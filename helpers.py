import os, platform

def limpiar_pantalla():
    os.system('cls') if platform.system() == 'Windows' else os.system('clear')
       
def leer_texto(longitud_min=0,longitud_max=100,mensaje=None):
     print(mensaje) if mensaje else None     
     while True:
          texto = input("> ")
          if len(texto) >= longitud_min and len(texto) <= longitud_max:
               return(texto)
          else:
            print(mensaje)

def dni_valido(dni, lista):
    if len(dni) != 8:
     print("el DNI no tiene 8 digitos")
     return False
    else:
     for cliente in lista:
        if cliente.dni == dni:
           print("ya existe un cliente con el DNI ingresado")
           return False        
    return True
        