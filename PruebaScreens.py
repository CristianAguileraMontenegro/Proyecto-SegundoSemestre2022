import tkinter as tk
from tkinter import *
import customtkinter as ctk
from  tkcalendar import *
import datetime
from calendario import Calendario


today = datetime.date.today()
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"



class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title('MyPetRecord')
        self.geometry("1280x720")
        self.resizable(False, False)

        ## Creating a container
        container = ctk.CTkFrame(self, corner_radius=0, fg_color="#BCD4E6")
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.screenCalendarioVacunacion = screenCalendarioVacunacion

        for F in {screenCalendarioVacunacion}:
            frame = F(self, container)
            self.frames[F] = frame
            frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

        self.show_frame(screenCalendarioVacunacion)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
class screenCalendarioVacunacion(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple20 = ("Helvetica", 20)
        Font_tuple14 = ("Helvetica", 16)
        Font_tuple12 = ("Helvetica", 12)

        self.grid_columnconfigure(0, weight=1)
        frame_0 = tk.Frame(self)
        frame_0.grid_columnconfigure(0, weight=1)
        frame_0.grid(row=0, column=0, sticky='nsew')

        self.grid_columnconfigure(1, weight=1)
        frame_1 = tk.Frame(self)
        frame_1.grid_columnconfigure(1, weight=1)
        frame_1.grid(row=1, column=0, sticky='nsew')

        self.labelTitle = ctk.CTkLabel(frame_0, text="Calendario de vacunación MyPetRecord", text_font=Font_tuple20, text_color='black')
        self.labelTitle.grid(row=0, column=0, padx=10 , pady=10)
        self.labelSubTitle = ctk.CTkLabel(frame_0, text="Nombre Veterinaria", text_font=Font_tuple14,text_color='black')
        self.labelSubTitle.grid(row=1, column=0, padx=10 , pady=10)

        self.calendario = Calendar(frame_0, selectmode='day',date_pattern='dd/mm/yyyy',  year=today.year, month=today.month, day=today.day)
        self.calendario.grid(row=3, column=0, padx=10 , pady=10)

        self.calendarioVacunacion = Calendario('1') #solo uno para pruebas, despues cambiar
        self.calendarioVacunacion.solicitarDatosCalendarioBaseDeDatos()
        self.indicarFechasEnCalendarioPostCargaBaseDeDatos(parent)

         #calendario
        #self.fechasCalendario:datetime.date = []
        #elementos calendario

        self.ingresarCita = ctk.CTkButton(frame_0, width=10, text='Ingresar cita de vacunación', command=lambda: self.mostarElementos())
        self.ingresarCita.grid(row=4, column=0, padx=10 , pady=10)

        self.confirmarCita = ctk.CTkButton(frame_0, width=10, text='Confirmar cita de vacunación', command=lambda: self.clickConfirmarFecha(parent))
        self.confirmarCita.grid(row=5, column=0, padx=10 , pady=10)

        self.verCitas= ctk.CTkButton(frame_0, width=10, text='Revisar de vacunación', command=lambda: self.mostarFechas(parent))
        self.verCitas.grid(row=6, column=0, padx=10 , pady=10)


        
        #componentes botones
        self.horaLabel = tk.Label(frame_0, text='Hora :' )
        self.horaLabel.grid(row=4, column=1, padx=10, pady=10)

        self.hora = Spinbox(frame_0, from_= 0, to = 24,width=5, state = 'readonly')  
        self.hora.grid(row=4, column=2, padx=10 , pady=10)

        self.minutosLabel = tk.Label(frame_0, text='Minutos :' )
        self.minutosLabel.grid(row=4, column=3, padx=10, pady=10)

        self.minutos = Spinbox(frame_0, from_= 0, to = 60,width=5, state = 'readonly')  
        self.minutos.grid(row=4, column=4, padx=10 , pady=10)

        self.rutLabel = tk.Label(frame_0, text='Rut :' )
        self.rutLabel.grid(row=5, column=1, padx=10 , pady=10)

        self.entradaRut = ctk.CTkEntry(frame_0, width = 140, text_font=Font_tuple14, fg_color="#F0EFEB", placeholder_text="Rut", placeholder_text_color="silver", justify = "center", text_color='black')
        self.entradaRut.grid(row=5, column=2, padx=10 , pady=10)

        self.numeroDeTelefonoLabel = tk.Label(frame_0, text='Telefono :' )
        self.numeroDeTelefonoLabel.grid(row=5, column=3, padx=10 , pady=10)

        self.numeroDeTelefono = ctk.CTkEntry(frame_0, width = 160, text_font=Font_tuple14, fg_color="#F0EFEB", placeholder_text="Telefono", placeholder_text_color="silver", justify = "center", text_color='black')
        self.numeroDeTelefono.grid(row=5, column=4, padx=10 , pady=10)
        
        self.frameListaboxDatos = ctk.CTkFrame(frame_1, corner_radius=10, fg_color="#99C1DE")
        self.frameListaboxDatos.grid(row=2, column=1, padx=20 , pady=20)


        self.ocularElementos()

       


        #horas cita
        
        #self.IndicadorDeHora = ctk
        #self.botonConf = ctk.CTkButton(self, width=10, text='Confirmar', command=lambda: self.clickConfirmar(parent))
        #self.botonConf.pack(padx=10, pady=30)
        #self.labelErrorIngreso = ctk.CTkLabel(self, text="Llave no existente", text_font=Font_tuple12, text_color='red')
        
    def clickConfirmarFecha(self, parent):

        fechaSeleccionada = self.calendario.get_date()
        self.indicarFechasEnCalendario(parent, fechaSeleccionada)

        #obtenermos la hora y minutos
        horaSeleccionada = self.hora.get()
        minutosSeleccionados = self.minutos.get()

        rutIngresado = self.entradaRut.get()
        numeroIngresado = self.numeroDeTelefono.get()

        if self.calendarioVacunacion.verificarFecha(fechaSeleccionada) == False:
            fechas = {'fecha': fechaSeleccionada, 'ruts':[], 'numeros':[], 'horas':[], 'minutos':[]}
            fechas["ruts"].append(rutIngresado)
            fechas["numeros"].append(numeroIngresado)
            fechas["horas"].append(horaSeleccionada)
            fechas["minutos"].append(minutosSeleccionados)
    
            print(str(fechas["fecha"]))
            self.calendarioVacunacion.agregarFechas(fechas)
            print(str(self.calendarioVacunacion.getFechas()))
        else:
           self.calendarioVacunacion.agregarDatosAFecha(fechaSeleccionada, rutIngresado, numeroIngresado, horaSeleccionada, minutosSeleccionados)

    def indicarFechasEnCalendario(self, parent, fechaSeleccionada):

        fecha = fechaSeleccionada.split('/') #la transformamos a string para poder ocuparla y marcar la casilla

        fechaSeleccionada2 = datetime.date(int(fecha[2]), int(fecha[1]), int(fecha[0])) #marcamos la casilla
        self.calendario.calevent_create(fechaSeleccionada2, "", tags="vacuna") #el vento nos permite mostrar la casilla
        self.calendario.tag_config("vacuna", background="green")
    
    def indicarFechasEnCalendarioPostCargaBaseDeDatos(self, parent):

        fechas = self.calendarioVacunacion.getFechas()
        for i in range(len(fechas)):
            fechaSeleccionada = fechas[i]["fecha"].split('/') #la transformamos a string para poder ocuparla y marcar la casilla

            fechaAIndicar = datetime.date(int(fechaSeleccionada[2]), int(fechaSeleccionada[1]), int(fechaSeleccionada[0])) #marcamos la casilla
            self.calendario
            self.calendario.calevent_create(fechaAIndicar, "", tags="vacuna") #el vento nos permite mostrar la casilla
            self.calendario.tag_config("vacuna", background="green")



    def mostarFechas(self, parent):
        fechaSeleccionada = self.calendario.get_date() #obtenemos la fecha seleccionada

        fechaObtenida = self.calendarioVacunacion.getFecha(fechaSeleccionada) #obtenemos los datos de la fecha seleccionada

        self.lista = tk.Listbox(self.frameListaboxDatos, width=70, height=7, selectmode='browse', font=('Helvetica', '13')) #creanis la lista pra mostrar nuestros datos
        self.lista.grid(row=0, column=0, padx=10, pady=10)

        for i in range(len(fechaObtenida["ruts"])): #iteramos por el maximo largo
            datos = 'rut :'+str(fechaObtenida["ruts"][i])+' numero de telefono :'+str(fechaObtenida["numeros"][i])+' Hora de atención:'+str(fechaObtenida["horas"][i])+':'+str(fechaObtenida["minutos"][i])
            print(str(datos))
            self.lista.insert(END, datos)


    def mostarElementos(self):
        self.hora.grid()
        self.horaLabel.grid()
        self.minutos.grid()
        self.minutosLabel.grid()
        self.entradaRut.grid()
        self.rutLabel.grid()
        self.numeroDeTelefono.grid()
        self.numeroDeTelefonoLabel.grid()
       

    def ocularElementos(self):
        self.hora.grid_remove()
        self.horaLabel.grid_remove()
        self.minutos.grid_remove()
        self.minutosLabel.grid_remove()
        self.entradaRut.grid_remove()
        self.rutLabel.grid_remove()
        self.numeroDeTelefono.grid_remove()
        self.numeroDeTelefonoLabel.grid_remove()



app = App()
app.mainloop()