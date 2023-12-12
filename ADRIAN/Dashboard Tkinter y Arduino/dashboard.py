import tkinter as tk
from client.gui_app import Frame,barra_menu

def main():
    
    root = tk.Tk()
    root.title('Dashboard Home')
    root.iconbitmap('Dashboard/img/icono.ico')
    root.geometry('880x595') #AnchoxAlto
    root.resizable(0,0)
    
    barra_menu(root)
    dashboard = Frame(root = root)
    
    dashboard.mainloop()
    
if __name__ == '__main__':
    main()
