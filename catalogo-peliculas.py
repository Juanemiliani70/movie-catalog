import tkinter as tk
from client.gui_app import Frame, barra_menu  


def main():
       root = tk.Tk()
       root.title('Catálogo de Películas')
       root.iconbitmap('img/catalogo.ico')
       root.resizable(0, 0)
       barra_menu(root)
       app = Frame(root)
       app.mainloop()

if __name__ == '__main__':
    main()