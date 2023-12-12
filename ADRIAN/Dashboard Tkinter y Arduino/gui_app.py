import tkinter as tk
from PIL import Image, ImageTk
import serial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import sqlite3
import datetime

def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu, width ='300', height ='300')

    menu_inicio =tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label ='Inicio',menu=menu_inicio)

    menu_inicio.add_command(label='Conectar')
    menu_inicio.add_command(label='Pausar')
    menu_inicio.add_command(label='Salir', command=root.destroy)

    barra_menu.add_cascade(label ='Configuración')
    barra_menu.add_cascade(label ='Ayuda')
    
class Frame(tk.Frame):
    
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.grid(sticky='news')
        
        #Variables de temperatura y humedad
        self.temperatura_valores =[]
        self.humedad_valores = []
        
        # Crea una conexión a la base de datos
        self.conn = sqlite3.connect('datos.db')
        # Crea una tabla para almacenar los datos de temperatura, humedad y fecha
        self.conn.execute('CREATE TABLE IF NOT EXISTS mediciones (id INTEGER PRIMARY KEY AUTOINCREMENT, temperatura REAL, humedad REAL, fecha TEXT)')
        
        # Asigna la imagen como un atributo de instancia de la clase
        self.img = Image.open('Dashboard/img/paisaje.jpg')
        self.background_image = ImageTk.PhotoImage(self.img)
        
        #Establecemos la conexión serial con el arduino
        try:
            self.conexion = serial.Serial('COM3', 9600) # Cambia el nombre del puerto según corresponda
        except serial.SerialException:
            print("No se pudo establecer la conexión con el puerto serie, revise la conexión o el puerto de conexión")
            self.conexion = None
        
        #Llamamos a las funciones que requerimos
        self.campos_dashboard()
        self.update()   
        self.tabla_mediciones()
        
    def campos_dashboard(self):
        
        # Crea un Label con la imagen como fondo y lo coloca detrás de todos los widgets en el Frame
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)
        background_label.lower()
            
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
                         
        # Humedad
            
        #Nombre de humedad
        self.label_humedad = tk.Label(self, text = 'Humedad: ')
        self.label_humedad.config(font = ('Arial', 15))
        self.label_humedad.grid(row = 2, column=0, padx =10, pady = 10)
            
        #Valor de Humedad
        self.hum_value = tk.Label(self, text='0.0',font=('Helvetica', 16),relief="sunken",borderwidth=5,width=5, height=2)
        self.hum_value.grid(row=2, column=1,padx=10, pady=10)
            
        #BOTONES--------------------------------------------
            
        # Botón Encender Ventilador
        self.boton_led = tk.Button(self, text="Encender LED", command=self.control_led, width='15',font=("Arial", 14, 'bold'))
        self.boton_led.grid(row=3, column=0,padx=10, pady=20,columnspan=3)
        
        #Gráfico de Temperatura
        self.grafico_temperatura = plt.Figure(figsize=(5, 4), dpi=40)
        self.ax1 = self.grafico_temperatura.add_subplot(111)
        self.canvas1 = FigureCanvasTkAgg(self.grafico_temperatura, master=self)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=1, column=2, columnspan=2, padx=10, pady=10)
        
        #Gráfico de Humedad
        self.grafico_humedad = plt.Figure(figsize=(5, 4), dpi=40)
        self.ax2 = self.grafico_humedad.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(self.grafico_humedad, master=self)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().grid(row=2, column=2, columnspan=2, padx=10, pady=10)
        
    def update_values(self, temperature, humidity):
                
        # Actualiza los valores de temperatura y humedad en las etiquetas
        self.temp_value.config(text=str(temperature)+'°C')
        self.hum_value.config(text=str(humidity)+'%')
            
        self.temperatura_valores.append(temperature)
        self.humedad_valores.append(humidity)
        
        # Envia los datos de temperatura al gráfico 1
        y1 = self.temperatura_valores
        self.ax1.clear()
        self.ax1.plot(y1)
        self.canvas1.draw()
                
        # Envia los datos de humedad al gráfico 2
        
        y2 = self.humedad_valores
        self.ax2.clear()
        self.ax2.plot(y2)
        self.canvas2.draw()
        
        # Obtiene la fecha actual en formato ISO
        fecha_actual = datetime.datetime.now().isoformat()
        
        # Guarda los valores en la base de datos junto con la fecha
        self.conn.execute('INSERT INTO mediciones (temperatura, humedad, fecha) VALUES (?, ?, ?)', (temperature, humidity, fecha_actual))
        self.conn.commit()
            
    def update(self):
        
        if self.conexion is not None:
            try:
                # Lee los datos del sensor desde el Arduino
                line = self.conexion.readline().decode('utf-8').rstrip()
                if line:
                    valores = line.split()
                    temperature = float(valores[1][:-2])
                    humidity = float(valores[3][:-1])
                    self.update_values(temperature, humidity)
            except serial.SerialException:
                print("No se pudo establecer la conexión con el puerto serie, revise la conexión o el puerto de conexión")
            
        self.after(1000, self.update)
            
    def control_led(self):
        
        if self.conexion is not None:
            try:
        
                if self.boton_led["text"] == "Encender LED":
                    self.conexion.write(b"1")  # Envía el comando "1" al puerto serial para encender el LED
                    self.boton_led["text"] = "Apagar LED"
                else:
                    self.conexion.write(b"0")  # Envía el comando "0" al puerto serial para apagar el LED
                    self.boton_led["text"] = "Encender LED"
            except serial.SerialException:
                print("Error de lectura desde el puerto serie")     
    
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
        
    def actualizar_tabla(self):
        
        # Borra los datos existentes en la tabla
        self.tabla.delete(*self.tabla.get_children())
        
        # Obtén los datos de la base de datos
        datos = self.conn.execute('SELECT fecha, temperatura, humedad FROM mediciones').fetchall()
        
        # Agrega los datos a la tabla
        for dato in datos:
            self.tabla.insert('', tk.END, values=dato)
            
        # Configura el temporizador para volver a actualizar la tabla cada segundondo
        self.after(1000, self.actualizar_tabla)
        
