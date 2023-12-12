import tkinter as tk
##from PIL import Image, ImageTk
##import serial
#####3import matplotlib.pyplot as plt
##from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
##import sqlite3
import datetime
#!/usr/bin/python
#para correr este programa utilizar python3 example.py
import tsys01
from time import sleep
sensor = tsys01.TSYS01(6) #hace falta especificar el bus de la raspberry que es la 6 (es el del navigator). Se puede comprobar con el i2cdetect -y 6

if not sensor.init():
    print("Error initializing sensor")
    ###exit(1)

###NO SE SI ESTA BIEN PONERLO COMO GLOBAL LA VARIABLE SENSOR


def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu, width ='300', height ='300')

    menu_inicio =tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label ='Inicio',menu=menu_inicio)

    menu_inicio.add_command(label='Conectar')
    menu_inicio.add_command(label='Pausar')
    menu_inicio.add_command(label='Salir', command=root.destroy)

    ##barra_menu.add_cascade(label ='Configuración')
    ##barra_menu.add_cascade(label ='Ayuda')
    
class Frame(tk.Frame):
    
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.grid(sticky='news')
        
        
        #Variables de temperatura y Presión
        self.temperatura_valores =[]
        self.presion_valores = []
       
        
        #Llamamos a las funciones que requerimos
        self.campos_dashboard()
        self.update()   
        self.tabla_mediciones()
        
    def campos_dashboard(self):
        
            
        # Ajusta el tamaño del Frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
            
        #-----------------------LABELS-------------------------------------
            
        #Título del Dashboard
        self.title_app = tk.Label(self, text="Dashboard Home")
        self.title_app.config(font=("Arial", 20, 'bold'), justify="center")
        self.title_app.grid(row=0, column=0, columnspan=7, padx=10, pady=50, sticky='ew')
            
        # Temperatura:
            
        #Nombre de Temperatura
        self.label_temperatura = tk.Label(self, text = 'Temperatura: ')
        self.label_temperatura.config(font = ('Arial', 15))
        self.label_temperatura.grid(row = 1, column=0, padx=10, pady = 10)
        
        #Valor de temperatura
        self.temp_value = tk.Label(self, text='0.0',font=('Helvetica', 16),relief="sunken",borderwidth=5,width=5, height=2)
        self.temp_value.grid(row=1, column=1, padx = 10,pady=10)
                         
        # Presión
            
        #Nombre de Presión
        self.label_Presión = tk.Label(self, text = 'Presión: ')
        self.label_Presión.config(font = ('Arial', 15))
        self.label_Presión.grid(row = 2, column=0, padx =10, pady = 10)
            
        #Valor de Presión
        self.hum_value = tk.Label(self, text='0.0',font=('Helvetica', 16),relief="sunken",borderwidth=5,width=5, height=2)
        self.hum_value.grid(row=2, column=1,padx=10, pady=10)
            
        
    def update_values(self, temperature, pressure):
                
        # Actualiza los valores de temperatura y Presión en las etiquetas 
        self.temp_value.config(text=str(temperature)+'°C')
        self.hum_value.config(text=str(pressure)+'%')
            
        self.temperatura_valores.append(temperature)
        self.presion_valores.append(pressure)

        
        # Obtiene la fecha actual en formato ISO
        fecha_actual = datetime.datetime.now().isoformat()
        
        # Guarda los valores en la base de datos junto con la fecha
        #self.conn.execute('INSERT INTO mediciones (temperatura, Presión, fecha) VALUES (?, ?, ?)', (temperature, pressure, fecha_actual))
        #self.conn.commit()
            
    def update(self):
        
        
        temperature = sensor.temperature()###PROBAR A PONER AQUI EL SELF
        pressure = 12
        self.update_values(temperature, pressure)
            
            
        self.after(1000, self.update)
     
    
    def tabla_mediciones(self):
                
       # Define los encabezados de columna y las opciones de la tabla
        self.tabla = ttk.Treeview(self, column=('fecha', 'temperatura'), show='headings')
        self.tabla.heading('fecha', text='Fecha', anchor='center')
        self.tabla.heading('temperatura', text='Temperatura', anchor='center')
        self.tabla.column('fecha', anchor='center')
        self.tabla.column('temperatura', anchor='center')
        self.tabla.grid(row=1, column=6, rowspan=2, sticky='nse', padx=10, pady=10)
        
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.scroll.grid(row=1, column=6, rowspan=2, sticky='nse', padx=10, pady=10)
        self.tabla.configure(yscrollcommand=self.scroll.set)

        # Ajusta el scrollbar al tamaño de la tabla
        self.grid_rowconfigure(1, weight=1) 
        
        # Configura el temporizador para volver a actualizar la tabla cada segundo
        self.after(1000, self.actualizar_tabla)
