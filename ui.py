import database as db 
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING
import helpers 

class CenterWidgetMixin():
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int((ws/2) - (w/2))
        y = int((hs/2) - (h/2))
        #self.geometry(f"WIDTHxHEIGTH+OFFSET_X+OFFSET_Y")
        self.geometry(f"{w}x{h+10}+{x}+{y}")

class CreateClientWindow(Toplevel,CenterWidgetMixin):
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Crear cliente")
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()
    


    def build(self):
        frame = Frame(self)
        frame.pack(padx=20,pady=10)

        Label(frame, text="DNI").grid(row=0,column=0)
        Label(frame, text="Nombre").grid(row=0,column=1)
        Label(frame, text="Apellido").grid(row=0,column=2)

        dni = Entry(frame)
        dni.bind("<KeyRelease>",lambda event: self.validate(event,0))
        dni.grid(row=1,column=0)
        
        nombre = Entry(frame)        
        nombre.bind("<KeyRelease>",lambda event: self.validate(event,1))
        nombre.grid(row=1,column=1)        

        apellido = Entry(frame)
        apellido.bind("<KeyRelease>",lambda event: self.validate(event,2))
        apellido.grid(row=1,column=2)   

        frame = Frame(self)
        frame.pack(pady=10)

        crear = Button(frame, text="Crear", command=self.create_client)
        crear.configure(state=DISABLED)
        crear.grid(row=0,column=0)
        Button(frame, text="Cancelar",command=self.close).grid(row=0,column=1)

        self.validaciones = [0,0,0]    
        self.crear = crear 
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
    
    def validate(self, evento, index):
        valor = evento.widget.get()
        valido = helpers.dni_valido(valor,db.Clientes.lista) if index == 0  \
                 else (valor.isalpha() and len(valor) >= 3 and len(valor) <=30)
        evento.widget.configure({"bg":"Green" if valido else "Red"})
        self.validaciones[index] = valido
        self.crear.config(state=NORMAL if self.validaciones == [1,1,1] else DISABLED)

    def create_client(self):
            self.master.treeview.insert(parent="",index="end",iid=self.dni.get(),
                            values=(self.dni.get(),self.nombre.get(),self.apellido.get()))
            db.Clientes.crear(self.dni.get(),self.nombre.get(),self.apellido.get())
            self.close()
    
    def close(self):
        self.destroy()
        self.update()

class EditClientWindow(Toplevel,CenterWidgetMixin):
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Editar cliente")
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()
    


    def build(self):
        frame = Frame(self)
        frame.pack(padx=20,pady=10)

        Label(frame, text="DNI").grid(row=0,column=0)
        Label(frame, text="Nombre").grid(row=0,column=1)
        Label(frame, text="Apellido").grid(row=0,column=2)

        dni = Entry(frame)        
        dni.grid(row=1,column=0)
        
        nombre = Entry(frame)        
        nombre.bind("<KeyRelease>",lambda event: self.validate(event,0))
        nombre.grid(row=1,column=1)        

        apellido = Entry(frame)
        apellido.bind("<KeyRelease>",lambda event: self.validate(event,1))
        apellido.grid(row=1,column=2)  

        client = self.master.treeview.focus()
        campos = self.master.treeview.item(client,"values")

        dni.insert(0,campos[0])
        dni.config(state=DISABLED)
        nombre.insert(0,campos[1])
        apellido.insert(0,campos[2])

        frame = Frame(self)
        frame.pack(pady=10)

        edit = Button(frame, text="Actualizar", command=self.edit_client)        
        edit.grid(row=0,column=0)
        Button(frame, text="Cancelar",command=self.close).grid(row=0,column=1)

        self.validaciones = [1,1]    
        self.edit = edit
        self.dni = dni 
        self.nombre = nombre
        self.apellido = apellido
    
    def validate(self, evento, index):
        valor = evento.widget.get()
        valido = (valor.isalpha() and len(valor) >= 3 and len(valor) <=30)
        evento.widget.configure({"bg":"Green" if valido else "Red"})
        self.validaciones[index] = valido
        self.edit.config(state=NORMAL if self.validaciones == [1,1] else DISABLED)

    def edit_client(self):
            cliente = self.master.treeview.focus()
            self.master.treeview.item(cliente, value=(self.dni.get(),self.nombre.get(),self.apellido.get()))
            db.Clientes.modificar(self.dni.get(),self.nombre.get(),self.apellido.get())
            self.close()
    
    def close(self):
        self.destroy()
        self.update()





        
class MainWindow(Tk,CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title('Gestor de clientes')
        self.build()
        self.center()
        self.set_style()
    
    def build(self):
        frame = Frame(self)
        frame.pack()

        treeview = ttk.Treeview(frame)
        treeview['columns'] = ('DNI','NOMBRE','APELLIDO')
        

        treeview.column("#0",width=0, stretch=NO)
        treeview.column("DNI",anchor=CENTER)
        treeview.column("NOMBRE",anchor=CENTER)        
        treeview.column("APELLIDO",anchor=CENTER)                

        treeview.heading("DNI",text="DNI",anchor=CENTER)
        treeview.heading("NOMBRE",text="NOMBRE", anchor=CENTER)        
        treeview.heading("APELLIDO",text="APELLIDO",anchor=CENTER)                

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT,fill=Y)

        treeview["yscrollcommand"] = scrollbar.set
        treeview.pack()

        for cliente in db.Clientes.lista:
            treeview.insert(parent="",index="end",iid=cliente.dni,
                            values=(cliente.dni,cliente.nombre,cliente.apellido))
        frame = Frame(self)
        frame.pack(pady=20)

        Button(frame, text="Crear",command=self.create).grid(row=0,column=0)
        Button(frame, text="Modificar",command=self.edit).grid(row=0,column=1)
        Button(frame, text="Borrar",command=self.delete).grid(row=0,column=2)
        treeview.pack()

        self.treeview = treeview

    def create(self):
        CreateClientWindow(self)
    
    def edit(self):
        if self.treeview.focus():
            EditClientWindow(self)
    
    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente,"values")
            confirmar = askokcancel(title="Confirmar borrado",
                                    message=f"Borrar {campos[1]} {campos[2]}?",
                                    icon=WARNING)
            if confirmar:
                self.treeview.delete(cliente)
                db.Clientes.borrar(campos[0])
    


    def set_style(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
    

if __name__ == "__main__":
    app = MainWindow()    
    app.mainloop()

