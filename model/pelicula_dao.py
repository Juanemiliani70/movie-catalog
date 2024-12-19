from .conexion_db import ConexionDB
from tkinter import messagebox
import sqlite3

def crear_tabla():
    conexion = ConexionDB()

    sql = '''
    CREATE TABLE IF NOT EXISTS peliculas (
        id_pelicula INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(100),
        duracion VARCHAR(10),
        genero VARCHAR(100)
    )
    '''
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        messagebox.showinfo('Crear Registro', 'Se creó la tabla en la base de datos')
    except sqlite3.Error as e:
        messagebox.showwarning('Crear Registro', f'Error al crear la tabla: {str(e)}')


def borrar_tabla():
    conexion = ConexionDB()

    sql = 'DROP TABLE IF EXISTS peliculas'
    
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        messagebox.showinfo('Borrar Registro', 'La tabla de la base de datos se borró con éxito')
    except sqlite3.Error as e:
        messagebox.showerror('Borrar Registro', f'Error al borrar la tabla: {str(e)}')

class Pelicula:
    def __init__(self, nombre, duracion, genero):
        self.id_pelicula = None  
        self.nombre = nombre
        self.duracion = duracion
        self.genero = genero

    def __str__(self):
        return f'Pelicula[{self.nombre}, {self.duracion}, {self.genero}]'

    def guardar(self):
        conexion = ConexionDB()

        sql = '''INSERT INTO peliculas (nombre, duracion, genero)
                 VALUES(?, ?, ?)'''

        try:
            conexion.cursor.execute(sql, (self.nombre, self.duracion, self.genero))
            conexion.cerrar()  
            messagebox.showinfo("Registro exitoso", f"La película '{self.nombre}' fue guardada exitosamente.")
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error al guardar la película: {str(e)}")

    @staticmethod
    def listar():
        conexion = ConexionDB()

        lista_peliculas = []
        sql = 'SELECT * FROM peliculas'

        try:
            conexion.cursor.execute(sql)
            lista_peliculas = conexion.cursor.fetchall()
            conexion.cerrar()
        except sqlite3.Error as e:
            messagebox.showwarning('Conexión al Registro', f'Error al obtener los registros: {str(e)}')

        return lista_peliculas
    
    def editar(self):
        if self.id_pelicula is None:
            messagebox.showerror('Edición de datos', 'La película no tiene un ID asignado.')
            return
        
        conexion = ConexionDB()

        sql = '''UPDATE peliculas
                 SET nombre = ?, duracion = ?, genero = ?
                 WHERE id_pelicula = ?'''

        try:
            conexion.cursor.execute(sql, (self.nombre, self.duracion, self.genero, self.id_pelicula))
            conexion.cerrar()
            messagebox.showinfo('Edición de datos', f'Película "{self.nombre}" editada con éxito')
        except sqlite3.Error as e:
            messagebox.showerror('Edición de datos', f'Error al editar la película: {str(e)}')

    def eliminar(self):
        if self.id_pelicula is None:
            messagebox.showerror('Eliminación de datos', 'La película no tiene un ID asignado.')
            return

        conexion = ConexionDB()

        sql = '''DELETE FROM peliculas WHERE id_pelicula = ?'''

        try:
            conexion.cursor.execute(sql, (self.id_pelicula,))
            conexion.cerrar()
            messagebox.showinfo('Eliminar Registro', f'Película "{self.nombre}" eliminada con éxito')
        except sqlite3.Error as e:
            messagebox.showerror('Eliminar Registro', f'Error al eliminar la película: {str(e)}')
