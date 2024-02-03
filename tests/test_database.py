import unittest
import database as db 
import copy 
import helpers
import config
import csv

class TestDatabase(unittest.TestCase):
        
        def setUp(self):
            db.Clientes.lista = [
                db.Cliente("23415776","Carlos","Perez"),
                db.Cliente("25415776","Raul","Perez"),
                db.Cliente("26415776","federico","Perez")
            ]
        
        def test_buscar_cliente(self):
            cliente_exisistente = db.Clientes.buscar("25415776")
            cliente_inexisistente = db.Clientes.buscar("27415776")
            self.assertIsNotNone(cliente_exisistente)
            self.assertIsNone(cliente_inexisistente)
        
        def test_crear(self):
             nuevo_cliente = db.Clientes.crear("28415776","Miguel","Mutti")
             self.assertEqual(len(db.Clientes.lista),4)
             self.assertEqual(nuevo_cliente.dni,"28415776")
             self.assertEqual(nuevo_cliente.nombre,"Miguel")
             self.assertEqual(nuevo_cliente.apellido,"Mutti")

        def test_modificar_cliente(self):
             cliente_a_modificar = copy.copy(db.Clientes.buscar("26415776"))
             cliente_modificado = db.Clientes.modificar("26415776","Alicia","Machado")
             self.assertEqual(cliente_a_modificar.nombre,"federico" )
             self.assertEqual(cliente_modificado.nombre,"Alicia" )
        
        def test_borrar_cliente(self):
             cliente_a_borrar = db.Clientes.borrar("26415776")
             cliente_rebuscado = db.Clientes.buscar("26415776")
             self.assertEqual(cliente_a_borrar.dni,"26415776")
             self.assertIsNone(cliente_rebuscado)
        
        def test_dni_valido(self):
             self.assertFalse(helpers.dni_valido("23415776",db.Clientes.lista))
             self.assertTrue(helpers.dni_valido("27415776",db.Clientes.lista))
        
        def test_escritura_csv(self):
             db.Clientes.borrar("23415776")
             db.Clientes.borrar("25415776")
             db.Clientes.modificar("26415776","Cambio Nombre","Cambio Apellido")
             dni,nombre,apellido = None,None,None
             with open(config.DATABASE_PATH,newline="\n") as fichero:
                  reader = csv.reader(fichero,delimiter=";")
                  dni,nombre,apellido = next(reader)
            
             self.assertEqual(dni,"26415776")
             self.assertEqual(nombre,"Cambio Nombre")
             self.assertEqual(apellido,"Cambio Apellido")
                  
                  
