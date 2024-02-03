import os 
import helpers
import database as db

def iniciar():
    while True:
        helpers.limpiar_pantalla()
        print('==============================')
        print('========bienvenidos===========')
        print('==============================')
        print('[1] Listar los clientes')
        print('[2] Buscar cliente')
        print('[3] Añadir cliente')
        print('[4] Modificar cliente')
        print('[5] Borrar un cliente')
        print('[6] Cerrar el gestor')

        opcion = input("> ")
        helpers.limpiar_pantalla()

        if opcion == '1':
            print("listando los clientes...\n")
            for cliente in db.Clientes.lista:
                print(cliente)
        elif opcion == '2':
            print("buscando cliente...\n")
            dni_ingresado = helpers.leer_texto(8,8,"DNI").upper()
            cliente = db.Clientes.buscar(dni_ingresado)
            print(cliente) if cliente else print("cliente no encontrado")
                
        elif opcion == '3':
            print("añadir cliente...\n")
            dni = None             
            while True:
                dni = helpers.leer_texto(8,8,"Ingrese DNI")            
                if helpers.dni_valido(dni,db.Clientes.lista):
                    break
            apellido = helpers.leer_texto(3,30,"Ingrese apellido").capitalize()
            nombre = helpers.leer_texto(3,30,"Ingrese nombre").capitalize()
            db.Clientes.crear(dni,nombre,apellido)
            print("cliente añadido.")
        elif opcion == '4':
            print("modificando cliente...\n")
            dni_ingresado = helpers.leer_texto(8,8,"DNI").upper()
            cliente = db.Clientes.buscar(dni_ingresado)
            if cliente:                 
                apellido = helpers.leer_texto(3,30,f"Ingrese apellido - [{cliente.apellido}]").capitalize()
                nombre = helpers.leer_texto(3,30,f"Ingrese apellido - [{cliente.nombre}]").capitalize()
                db.Clientes.modificar(cliente.dni,nombre,apellido)
                print("cliente modificado.")
            else: 
                print("cliente no encontrado")
            
        elif opcion == '5':
            print("borrando cliente...\n")
            dni_ingresado = helpers.leer_texto(8,8,"DNI").upper()            
            print("cliente borrado.") if db.Clientes.borrar(dni_ingresado) else print("cliente no encontrado")
        
        elif opcion == '6':
            print("saliendo...\n")                        
            break 

        input("\npresiona enter para continuar...")
