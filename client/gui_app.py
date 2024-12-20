import tkinter as tk
from tkinter import ttk
from model.pelicula_dao import crear_tabla, borrar_tabla
from model.pelicula_dao import Pelicula
from tkinter import messagebox

def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu)  

    menu_inicio = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label='Inicio', menu=menu_inicio)
    menu_inicio.add_command(label='Crear registro en DB', command=crear_tabla)
    menu_inicio.add_command(label='Eliminar registro en DB', command=borrar_tabla)
    menu_inicio.add_command(label='Salir', command=root.destroy)

    barra_menu.add_cascade(label='Consultas')
    barra_menu.add_cascade(label='Configuración')
    barra_menu.add_cascade(label='Ayuda')

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.grid() 

        self.id_pelicula = None  
        self.campos_peliculas()  
        self.deshabilitar_campos() 
        self.crear_tabla_peliculas()  
        self.tabla_peliculas()  
    
    def campos_peliculas(self):
        self.label_nombre = tk.Label(self, text='Nombre:')
        self.label_nombre.config(font=('Arial', 12, 'bold'))
        self.label_nombre.grid(row=0, column=0, padx=10, pady=10)

        self.label_duracion = tk.Label(self, text='Duración:')
        self.label_duracion.config(font=('Arial', 12, 'bold'))
        self.label_duracion.grid(row=1, column=0, padx=10, pady=10)

        self.label_genero = tk.Label(self, text='Género:')
        self.label_genero.config(font=('Arial', 12, 'bold'))
        self.label_genero.grid(row=2, column=0, padx=10, pady=10)

        self.mi_nombre = tk.StringVar()
        self.entry_nombre = tk.Entry(self, textvariable=self.mi_nombre)
        self.entry_nombre.config(width=50, font=('Arial', 12))
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

        self.mi_duracion = tk.StringVar()
        self.entry_duracion = tk.Entry(self, textvariable=self.mi_duracion)
        self.entry_duracion.config(width=50, font=('Arial', 12))
        self.entry_duracion.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

        self.mi_genero = tk.StringVar()
        self.entry_genero = tk.Entry(self, textvariable=self.mi_genero)
        self.entry_genero.config(width=50, font=('Arial', 12))
        self.entry_genero.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

        self.boton_nuevo = tk.Button(self, text="Nuevo", command=self.habilitar_campos)
        self.boton_nuevo.config(width=20, font=('Arial', 12, 'bold'), fg='#DAD5D6', bg='#158645', cursor='hand2', activebackground='#35BD6F')
        self.boton_nuevo.grid(row=3, column=0, padx=10, pady=10)

        self.boton_guardar = tk.Button(self, text="Guardar", command=self.guardar_pelicula)
        self.boton_guardar.config(width=20, font=('Arial', 12, 'bold'), fg='#DAD5D6', bg='#1658A2', cursor='hand2', activebackground='#3586DF')
        self.boton_guardar.grid(row=3, column=1, padx=10, pady=10)

        self.boton_cancelar = tk.Button(self, text="Cancelar", command=self.deshabilitar_campos)
        self.boton_cancelar.config(width=20, font=('Arial', 12, 'bold'), fg='#DAD5D6', bg='#BD152E', cursor='hand2', activebackground='#E15370')
        self.boton_cancelar.grid(row=3, column=2, padx=10, pady=10)

    def habilitar_campos(self):
        self.mi_nombre.set('')
        self.mi_duracion.set('')
        self.mi_genero.set('')
        
        self.entry_nombre.config(state='normal')
        self.entry_duracion.config(state='normal')
        self.entry_genero.config(state='normal')
        
        self.boton_guardar.config(state='normal')
        self.boton_cancelar.config(state='normal')

    def deshabilitar_campos(self):
        self.entry_nombre.config(state='disabled')
        self.entry_duracion.config(state='disabled')
        self.entry_genero.config(state='disabled')
        
        self.boton_guardar.config(state='disabled')
        self.boton_cancelar.config(state='disabled')

    def guardar_pelicula(self):
        nueva_pelicula = Pelicula(self.mi_nombre.get(), self.mi_duracion.get(), self.mi_genero.get())
    
        if self.id_pelicula is None:
           nueva_pelicula.guardar()  
        else:
            nueva_pelicula.id_pelicula = self.id_pelicula 
            nueva_pelicula.editar()  
        
        self.tabla_peliculas()
        self.deshabilitar_campos()


    def crear_tabla_peliculas(self):
        self.tabla = ttk.Treeview(self, column=('Nombre', 'Duracion', 'Genero'))
        self.tabla.grid(row=4, column=0, columnspan=4, sticky='nse')

        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.scroll.grid(row=4, column=4, sticky='nse')
        self.tabla.configure(yscrollcommand=self.scroll.set)

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='NOMBRE')
        self.tabla.heading('#2', text='DURACION')
        self.tabla.heading('#3', text='GENERO')

    def tabla_peliculas(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

       
        self.lista_peliculas = Pelicula.listar()
        for p in self.lista_peliculas:
            self.tabla.insert('', 'end', text=p[0], values=(p[1], p[2], p[3]))

        
        self.boton_editar = tk.Button(self, text="Editar", command=self.editar_datos)
        self.boton_editar.config(width=20, font=('Arial', 12, 'bold'), fg='#DAD5D6', bg='#158645', cursor='hand2', activebackground='#35BD6F')
        self.boton_editar.grid(row=5, column=0, padx=10, pady=10)

        self.boton_eliminar = tk.Button(self, text="Eliminar", command=self.eliminar_pelicula)
        self.boton_eliminar.config(width=20, font=('Arial', 12, 'bold'), fg='#DAD5D6', bg='#BD152E', cursor='hand2', activebackground='#E15370')
        self.boton_eliminar.grid(row=5, column=1, padx=10, pady=10)

    def editar_datos(self):
        seleccion = self.tabla.selection()
        if seleccion:
           self.id_pelicula = self.tabla.item(seleccion)['text']  
           self.nombre_pelicula = self.tabla.item(seleccion)['values'][0]
           self.duracion_pelicula = self.tabla.item(seleccion)['values'][1]
           self.genero_pelicula = self.tabla.item(seleccion)['values'][2]

        
           self.pelicula_editar = Pelicula(self.nombre_pelicula, self.duracion_pelicula, self.genero_pelicula)
           self.pelicula_editar.id_pelicula = self.id_pelicula 
       
           self.habilitar_campos()

        
           self.entry_nombre.delete(0, 'end')
           self.entry_nombre.insert(0, self.nombre_pelicula)

           self.entry_duracion.delete(0, 'end')
           self.entry_duracion.insert(0, self.duracion_pelicula)

           self.entry_genero.delete(0, 'end')
           self.entry_genero.insert(0, self.genero_pelicula)
        else:
            messagebox.showerror('Edición de datos', 'No ha seleccionado ningún registro')

    def eliminar_pelicula(self):
        seleccion = self.tabla.selection()
        if seleccion:
            id_pelicula = self.tabla.item(seleccion)['text']
        
            pelicula_a_eliminar = Pelicula(self.tabla.item(seleccion)['values'][0],
                                       self.tabla.item(seleccion)['values'][1],
                                       self.tabla.item(seleccion)['values'][2])
        
       
            pelicula_a_eliminar.id_pelicula = id_pelicula
        
        
            pelicula_a_eliminar.eliminar() 
            self.tabla_peliculas()
        else:
            messagebox.showwarning("Selección inválida", "Por favor, seleccione una película para eliminar.")
