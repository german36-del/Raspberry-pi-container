import tkinter as tk
from gui_app import Frame,barra_menu

def main():
    
    root = tk.Tk()
    root.title('Dashboard Home')
    ##root.iconbitmap('Dashboard/img/icono.ico')
    root.geometry('880x595') #AnchoxAlto
    ##no redimensionable
    ##root.resizable(0,0)
    
    barra_menu(root)
    dashboard = Frame(root = root)
    
    dashboard.mainloop()
    
   ##solo se ejecuta este código si es el archivo principal 
if __name__ == '__main__':
    main()
