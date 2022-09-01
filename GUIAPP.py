import tkinter as tk
from terminalVeterinario import *



'''root = Tk()
root.title('MyPetRecord')
root.geometry("1280x720")
root.configure(bg='#5C9C81')'''

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('MyPetRecord')
        self.geometry("1280x720")
        self.resizable(False, False)

        ## Creating a container
        container = tk.Frame(self, bg="#5C9C81")
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.screenIngresoLlave = screenIngresoLlave
        self.screenBuscarMascota = screenBuscarMascota
        self.screenDatosTotalMascota = screenDatosTotalMascota
        self.screenFormularioFicha = screenFormularioVerFicha
        self.screenFormularioCrearFicha = screenFormularioCrearFicha
        self.screenFormularioAgregarMascota = screenFormularioAgregarMascota
        self.screenFormularioFichaAuthCirugia = screenFormularioFichaAuthCirugia
        self.screenFormularioFichaHospt = screenFormularioFichaHospt
        self.screenFormularioFichaSedacion = screenFormularioFichaSedacion
        self.screenAbstractMedico = screenAbstractMedico
           
        for F in {screenIngresoLlave, screenBuscarMascota, screenDatosTotalMascota,
        screenFormularioVerFicha,screenFormularioCrearFicha, screenFormularioAgregarMascota,
        screenFormularioFichaAuthCirugia, screenFormularioFichaHospt, screenFormularioFichaSedacion, screenAbstractMedico}:
            frame = F(self, container)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(screenAbstractMedico)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class screenIngresoLlave(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.configure(background='#5C9C81')
        self.labelTitle = tk.Label(self, text="Bienvenido al sistema MyPetRecord", font=('MS Shell Dlg 2', '20'), bg='#5C9C81', fg='white')
        self.labelTitle.place(x='436',y='25')
        self.labelSubTitle = tk.Label(self, text="Porfavor, ingrese la llave de acceso", font=('MS Shell Dlg 2', '14'), bg='#5C9C81', fg='white')
        self.labelSubTitle.place(x='496',y='115')
        self.entradaKey = tk.Entry(self, width = 63, font=('MS Shell Dlg 2', '14'))
        self.entradaKey.place(x='330', y='210')
        self.botonConf = tk.Button(self, width='10', text='Confirmar')
        self.botonConf.place(x='615', y='260')

class screenBuscarMascota(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.configure(background='#5C9C81')
        self.entradaBuscar = tk.Entry(self, width = 62, font=('MS Shell Dlg 2', '14'))
        self.entradaBuscar.place(x='154', y='30')
        self.botonBuscar = tk.Button(self, width= '10', text='Buscar')
        self.botonBuscar.place(x='795', y='32')
        self.labelCodigoInvalido = tk.Label(self, text="Ingrese un código válido", font=('MS Shell Dlg 2', '8'))


class screenDatosTotalMascota(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.configure(background='#5C9C81')

        listaprueba = ['Nombre:', 'nose', 'lol', 'a', 'b', 'c', 'd']
        listaString = tk.StringVar(value=listaprueba)

        self.listDatosBasicos = tk.Listbox(
			self,
			listvariable=listaString,
            width=40,
			height=8,
			selectmode='browse',
            font=('Segoe UI', '14'))
        self.listDatosBasicos.place(x='50', y='60')

        self.listDatosTablaMedica = tk.Listbox(
			self,
			listvariable=listaString,
            width=40,
			height=8,
			selectmode='browse',
            font=('Segoe UI', '14'))
        self.listDatosTablaMedica.place(x='50', y='348')

        self.listFichasMedicas= tk.Listbox(
			self,
			listvariable=listaString,
            width=36,
			height=19,
			selectmode='browse',
            font=('Segoe UI', '14'))
        self.listFichasMedicas.place(x='580', y='60')

        self.buttonVerFicha = tk.Button(self, width= '25', height= '3',text='Ver Ficha')
        self.buttonVerFicha.place(x='1000', y='60')

        self.botonVolverSDatosTotal = tk.Button(self, width= '25', height= '3',text='Volver')
        self.botonVolverSDatosTotal.place(x='580', y='600')

        self.buttonCrearFicha = tk.Button(self, width= '25', height= '6',text='Crear Ficha')
        self.buttonCrearFicha.place(x='1000', y='459')

        self.labelErrorFicha = tk.Label(self, text="Seleccione una ficha", font=('MS Shell Dlg 2', '8'))


class screenFormularioVerFicha(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.configure(background='#5C9C81')
        #Agregar Labels
        self.labelSucursalSVerFicha = tk.Label(self, text="Sucursal Veterinaria", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelSucursalSVerFicha.place(x='40',y='30')
        
        self.labelVetACargoSVerFicha = tk.Label(self, text="Veterinario a cargo", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelVetACargoSVerFicha.place(x='40',y='75')
        
        self.labelFechaConsultaSVerFicha = tk.Label(self, text="Fecha Consulta", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelFechaConsultaSVerFicha.place(x='40',y='120')
        
        self.labelTratamientosConsultaSVerFicha = tk.Label(self, text="Tratamientos Consulta", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelTratamientosConsultaSVerFicha.place(x='40',y='165')
        
        self.labelMedicamentosConsultaSVerFicha = tk.Label(self, text="Medicamentos Consulta", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelMedicamentosConsultaSVerFicha.place(x='40',y='210')
        
        self.labelCausaVisitaSVerFicha = tk.Label(self, text="Causa Visita", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelCausaVisitaSVerFicha.place(x='40',y='255')
        
        self.labelVacSuministradasSVerFicha = tk.Label(self, text="Vacunas Suministradas", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelVacSuministradasSVerFicha.place(x='40',y='300')
        
        self.labelFrecRespiratoriaSVerFicha = tk.Label(self, text="Frecuencia Respiratoria", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelFrecRespiratoriaSVerFicha.place(x='40',y='345')
        
        self.labelFrecCardiacaSVerFicha = tk.Label(self, text="Frecuencia Cardiaca", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelFrecCardiacaSVerFicha.place(x='40',y='390')

        self.labelPesoSVerFicha = tk.Label(self, text="Peso", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelPesoSVerFicha.place(x='40',y='435')
        
        self.labelEdadSVerFicha = tk.Label(self, text="Edad", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelEdadSVerFicha.place(x='40',y='480')

        self.labelTemperaturaSVerFicha = tk.Label(self, text="Temperatura", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelTemperaturaSVerFicha.place(x='40',y='525')
        
        #Agregar Entrys
        self.entradaSucursalSVerFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaSucursalSVerFicha.place(x='260', y='30')

        self.entradaVetACargoSVerFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaVetACargoSVerFicha.place(x='260', y='75')

        self.entradaFechaConsultaSVerFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaFechaConsultaSVerFicha.place(x='260', y='120')

        self.entradaTratamientosConsultaSVerFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaTratamientosConsultaSVerFicha.place(x='260', y='165')

        self.entradaMedicamentosConsultaSVerFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaMedicamentosConsultaSVerFicha.place(x='260', y='210')

        self.entradaCausaVisitaSVerFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaCausaVisitaSVerFicha.place(x='260', y='255')

        self.entradaVacSuministradasSVerFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaVacSuministradasSVerFicha.place(x='260', y='300')

        self.entradaFrecRespiratoriaSVerFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaFrecRespiratoriaSVerFicha.place(x='260', y='345')

        self.entradaFrecCardiacaSVerFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaFrecCardiacaSVerFicha.place(x='260', y='390')

        self.entradaPesoSVerFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaPesoSVerFicha.place(x='260', y='435')

        self.entradaEdadSVerFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaEdadSVerFicha.place(x='260', y='480')

        self.entradaTemperaturaSVerFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaTemperaturaSVerFicha.place(x='260', y='525')

        #Agregar Buttons
        self.botonVolverSVerFicha = tk.Button(self, width= '25', height= '3',text='Volver')
        self.botonVolverSVerFicha.place(x='260', y='605')

        self.botonVerFichaHosp = tk.Button(self, width= '25', height= '4',text='Ver Ficha Hospitalizacion')
        self.botonVerFichaHosp.place(x='690', y='30')

        self.botonVerFichaSedacion = tk.Button(self, width= '25', height= '4',text='Ver Ficha Sedación')
        self.botonVerFichaSedacion.place(x='690', y='165')

        self.botonVerFichaOperacion = tk.Button(self, width= '25', height= '4',text='Ver Ficha Operación')
        self.botonVerFichaOperacion.place(x='690', y='300')


class screenFormularioCrearFicha(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.configure(background='#5C9C81')
        #Agregar Labels
        self.labelSucursalSCrearFicha = tk.Label(self, text="Sucursal Veterinaria", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelSucursalSCrearFicha.place(x='40',y='30')
        
        self.labelVetACargoSCrearFicha = tk.Label(self, text="Veterinario a cargo", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelVetACargoSCrearFicha.place(x='40',y='75')
        
        self.labelFechaConsultaSCrearFicha = tk.Label(self, text="Fecha Consulta", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelFechaConsultaSCrearFicha.place(x='40',y='120')
        
        self.labelTratamientosConsultaSCrearFicha = tk.Label(self, text="Tratamientos Consulta", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelTratamientosConsultaSCrearFicha.place(x='40',y='165')
        
        self.labelMedicamentosConsultaSCrearFicha = tk.Label(self, text="Medicamentos Consulta", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelMedicamentosConsultaSCrearFicha.place(x='40',y='210')
        
        self.labelCausaVisitaSCrearFicha = tk.Label(self, text="Causa Visita", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelCausaVisitaSCrearFicha.place(x='40',y='255')
        
        self.labelVacSuministradasSCrearFicha = tk.Label(self, text="Vacunas Suministradas", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelVacSuministradasSCrearFicha.place(x='40',y='300')
        
        self.labelFrecRespiratoriaSCrearFicha = tk.Label(self, text="Frecuencia Respiratoria", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelFrecRespiratoriaSCrearFicha.place(x='40',y='345')
        
        self.labelFrecCardiacaSCrearFicha = tk.Label(self, text="Frecuencia Cardiaca", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelFrecCardiacaSCrearFicha.place(x='40',y='390')

        self.labelPesoSCrearFicha = tk.Label(self, text="Peso", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelPesoSCrearFicha.place(x='40',y='435')
        
        self.labelEdadSCrearFicha = tk.Label(self, text="Edad", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelEdadSCrearFicha.place(x='40',y='480')

        self.labelTemperaturaSCrearFicha = tk.Label(self, text="Temperatura", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelTemperaturaSCrearFicha.place(x='40',y='525')
        
        #Agregar Entrys
        self.entradaSucursalSCrearFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaSucursalSCrearFicha.place(x='260', y='30')

        self.entradaVetACargoSCrearFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaVetACargoSCrearFicha.place(x='260', y='75')

        self.entradaFechaConsultaSCrearFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaFechaConsultaSCrearFicha.place(x='260', y='120')

        self.entradaTratamientosConsultaSCrearFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaTratamientosConsultaSCrearFicha.place(x='260', y='165')

        self.entradaMedicamentosConsultaSCrearFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaMedicamentosConsultaSCrearFicha.place(x='260', y='210')

        self.entradaCausaVisitaSCrearFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaCausaVisitaSCrearFicha.place(x='260', y='255')

        self.entradaVacSuministradasSCrearFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaVacSuministradasSCrearFicha.place(x='260', y='300')

        self.entradaFrecRespiratoriaSCrearFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaFrecRespiratoriaSCrearFicha.place(x='260', y='345')

        self.entradaFrecCardiacaSCrearFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaFrecCardiacaSCrearFicha.place(x='260', y='390')

        self.entradaPesoSCrearFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaPesoSCrearFicha.place(x='260', y='435')

        self.entradaEdadSCrearFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaEdadSCrearFicha.place(x='260', y='480')

        self.entradaTemperaturaSCrearFicha = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaTemperaturaSCrearFicha.place(x='260', y='525')

        #Agregar Buttons
        self.botonVolverSCrearFicha = tk.Button(self, width= '25', height= '3',text='Volver')
        self.botonVolverSCrearFicha.place(x='260', y='605')

        self.botonAgregarFichaGeneralSCrearFicha = tk.Button(self, width='25', height='4', text='Agregar Ficha General')
        self.botonAgregarFichaGeneralSCrearFicha.place(x='690', y='30')

        self.botonCrearFichaHospSCrearFicha = tk.Button(self, width= '25', height= '4',text='Agregar Ficha Hospitalizacion')
        self.botonCrearFichaHospSCrearFicha.place(x='690', y='165')

        self.botonCrearFichaSedacionSCrearFicha = tk.Button(self, width= '25', height= '4',text='Agregar Ficha Sedación')
        self.botonCrearFichaSedacionSCrearFicha.place(x='690', y='325')

        self.botonCrearFichaOperacionSCrearFicha = tk.Button(self, width= '25', height= '4',text='Agregar Ficha Operación')
        self.botonCrearFichaOperacionSCrearFicha.place(x='690', y='480')
    

class screenFormularioAgregarMascota(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.configure(background='#5C9C81')
        self.labelNombreMascotaSAgregarMascota = tk.Label(self, text="Nombre Mascota", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelNombreMascotaSAgregarMascota.place(x='100', y='50')

        self.labelEspecieSAgregarMascota = tk.Label(self, text="Especie ", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelEspecieSAgregarMascota.place(x='100', y='120')

        self.labelColorSAgregarMascota = tk.Label(self, text="Color", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelColorSAgregarMascota.place(x='100', y='190')

        self.labelRazaSAgregarMascota = tk.Label(self, text="Raza", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelRazaSAgregarMascota.place(x='100', y='260')

        self.labelNombreTutorSAgregarMascota = tk.Label(self, text="Nombre Tutor", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelNombreTutorSAgregarMascota.place(x='100', y='330')
        
        self.labelRutTutorSAgregarMascota = tk.Label(self, text="Rut Tutor", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelRutTutorSAgregarMascota.place(x='100', y='400')

        self.labelNumeroTelefonoSAgregarMascota = tk.Label(self, text="Número de Teléfono", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelNumeroTelefonoSAgregarMascota.place(x='100', y='470')

        self.labelDireccionTutorSAgregarMascota = tk.Label(self, text="Dirección Tutor", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelDireccionTutorSAgregarMascota.place(x='100', y='540')


        #Agregar Entrys
        self.entradaNombreMascotaSAgregarMascota = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaNombreMascotaSAgregarMascota.place(x='300', y='50')

        self.entradaEspecieSAgregarMascota = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaEspecieSAgregarMascota.place(x='300', y='120')

        self.entradaColorSAgregarMascota = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaColorSAgregarMascota.place(x='300', y='190')

        self.entradaRazaSAgregarMascota = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaRazaSAgregarMascota.place(x='300', y='260')
        
        self.entradaNombreTutorSAgregarMascota = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaNombreTutorSAgregarMascota.place(x='300', y='330')
        
        self.entradaNombreMascotaSAgregarMascota = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaNombreMascotaSAgregarMascota.place(x='300', y='400')
        
        self.entradaNumeroTelefonoSAgregarMascota = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaNumeroTelefonoSAgregarMascota.place(x='300', y='470')

        self.entradaDireccionTutorSAgregarMascota = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaDireccionTutorSAgregarMascota.place(x='300', y='540')

        #Agregar buttons
        self.botonVolverSCrearFicha = tk.Button(self, width= '25', height= '3',text='Volver')
        self.botonVolverSCrearFicha.place(x='160', y='610')
        
        self.botonAgregarMascota = tk.Button(self, width= '25', height= '3',text='Agregar Mascota')
        self.botonAgregarMascota.place(x='420', y='610')


class screenFormularioFichaAuthCirugia(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.configure(background='#5C9C81')
        self.labelNombrePacienteSFichaAuthCirugia = tk.Label(self, text="Nombre Paciente", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelNombrePacienteSFichaAuthCirugia.place(x='40',y='30')
        
        self.labelPesoSFichaAuthCirugia = tk.Label(self, text="Peso", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelPesoSFichaAuthCirugia.place(x='40',y='70')
        
        self.labelEspecieSFichaAuthCirugia = tk.Label(self, text="Especie", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelEspecieSFichaAuthCirugia.place(x='40',y='110')
        
        self.labelEdadSFichaAuthCirugia = tk.Label(self, text="Edad", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelEdadSFichaAuthCirugia.place(x='40',y='150')
        
        self.labelRazaSFichaAuthCirugia = tk.Label(self, text="Raza", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelRazaSFichaAuthCirugia.place(x='40',y='190')
        
        self.labelColorSFichaAuthCirugia = tk.Label(self, text="Color", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelColorSFichaAuthCirugia.place(x='40',y='230')
        
        self.labelDiagnosticoSFichaAuthCirugia = tk.Label(self, text="Diagnóstico", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelDiagnosticoSFichaAuthCirugia.place(x='40',y='270')
        
        self.labelCirugiaARealizarSFichaAuthCirugia = tk.Label(self, text="Cirugía a Realizar", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelCirugiaARealizarSFichaAuthCirugia.place(x='40',y='360')
        
        self.labelNombreDelTutorSFichaAuthCirugia = tk.Label(self, text="Nombre del Tutor", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelNombreDelTutorSFichaAuthCirugia.place(x='40',y='400')

        self.labelRutTutorSFichaAuthCirugia = tk.Label(self, text="Rut Tutor", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelRutTutorSFichaAuthCirugia.place(x='40',y='440')
        
        self.labelNumeroTelefonoSFichaAuthCirugia = tk.Label(self, text="Número de Teléfono", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelNumeroTelefonoSFichaAuthCirugia.place(x='40',y='480')

        self.labelDireccionSFichaAuthCirugia = tk.Label(self, text="Dirección", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelDireccionSFichaAuthCirugia.place(x='40',y='520')

        self.labelAuthTutorSFichaAuthCirugia = tk.Label(self, text="Autorizacion tutor", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelAuthTutorSFichaAuthCirugia.place(x='40',y='560')

        self.labelErrorCamposSFichaAuthCirugia = tk.Label(self, text="Temperatura", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')

        #Agregar Entrys
        self.entradaNombrePacienteSFichaAuthCirugia = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaNombrePacienteSFichaAuthCirugia.place(x='200',y='30')

        self.entradaPesoSFichaAuthCirugia = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaPesoSFichaAuthCirugia.place(x='200',y='70')

        self.entradaEspecieSFichaAuthCirugia = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaEspecieSFichaAuthCirugia.place(x='200',y='110')

        self.entradaEdadConsultaSFichaAuthCirugia = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaEdadConsultaSFichaAuthCirugia.place(x='200',y='150')

        self.entradaRazaSFichaAuthCirugia = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaRazaSFichaAuthCirugia.place(x='200',y='190')

        self.entradaColorSFichaAuthCirugia = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaColorSFichaAuthCirugia.place(x='200',y='230')

        self.entradaDiagnosticoSFichaAuthCirugia = tk.Text(self, width = 40, height= 3, font=('MS Shell Dlg 2', '12'))
        self.entradaDiagnosticoSFichaAuthCirugia.place(x='200',y='270')

        self.entradaCirugiaARealizarSFichaAuthCirugia = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaCirugiaARealizarSFichaAuthCirugia.place(x='200',y='360')

        self.entradaNombreTutorSFichaAuthCirugia = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaNombreTutorSFichaAuthCirugia.place(x='200',y='400')

        self.entradaRutSFichaAuthCirugia = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaRutSFichaAuthCirugia.place(x='200',y='440')

        self.entradaNumTelefonoSFichaAuthCirugia = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaNumTelefonoSFichaAuthCirugia.place(x='200',y='480')

        self.entradaDireccionSFichaAuthCirugia = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaDireccionSFichaAuthCirugia.place(x='200',y='520')

        self.entradaAuthTutorSFichaAuthCirugia = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaAuthTutorSFichaAuthCirugia.place(x='200',y='560')

        #Agregar botones
        self.botonAgregarFichaSFichaAuthCirugia = tk.Button(self, width= '25', height= '3',text='Agregar Ficha Operación')
        self.botonAgregarFichaSFichaAuthCirugia.place(x='350',y='620')

        self.botonVolverSFichaAuthCirugia = tk.Button(self, width= '25', height= '3',text='Volver')
        self.botonVolverSFichaAuthCirugia.place(x='90', y='620')


class screenFormularioFichaHospt(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.configure(background='#5C9C81')
        #Agregar Labels
        self.labelNombreMascotaSCrearFichaHosp = tk.Label(self, text="Nombre Mascota", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelNombreMascotaSCrearFichaHosp.place(x='100', y='30')

        self.labelEspecieSCrearFichaHosp = tk.Label(self, text="Especie ", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelEspecieSCrearFichaHosp.place(x='100', y='80')

        self.labelPesoSCrearFichaHosp = tk.Label(self, text="Peso", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelPesoSCrearFichaHosp.place(x='100', y='130')

        self.labelEdadSCrearFichaHosp = tk.Label(self, text="Edad", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelEdadSCrearFichaHosp.place(x='100', y='180')

        self.labelRazaSCrearFichaHosp = tk.Label(self, text="Raza", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelRazaSCrearFichaHosp.place(x='100', y='230')

        self.labelColorSCrearFichaHosp = tk.Label(self, text="Color", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelColorSCrearFichaHosp.place(x='100', y='280')

        self.labelMotivoHospSCrearFichaHosp = tk.Label(self, text="Motivo de Hospitalización", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelMotivoHospSCrearFichaHosp.place(x='100', y='330')

        self.labelDiagnosticoSCrearFichaHosp = tk.Label(self, text="Diagnóstico", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelDiagnosticoSCrearFichaHosp.place(x='100', y='470')

        self.labelAuthTutorSCrearFichaHosp = tk.Label(self, text="Autorización tutor", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelAuthTutorSCrearFichaHosp.place(x='100', y='560')     


        #Agregar Entrys
        self.entradaNombrePacienteSCrearFichaHosp = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaNombrePacienteSCrearFichaHosp.place(x='300', y='30')

        self.entradaPesoSCrearFichaHosp = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaPesoSCrearFichaHosp.place(x='300', y='80')

        self.entradaEspecieSCrearFichaHosp = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaEspecieSCrearFichaHosp.place(x='300', y='130')

        self.entradaEdadSCrearFichaHosp = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaEdadSCrearFichaHosp.place(x='300', y='180')

        self.entradaRazaSCrearFichaHosp = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaRazaSCrearFichaHosp.place(x='300', y='230')

        self.entradaColorSCrearFichaHosp = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaColorSCrearFichaHosp.place(x='300', y='280')

        self.entradaMotivoHospSCrearFichaHosp = tk.Text(self, width = 40, height=6, font=('MS Shell Dlg 2', '12'))
        self.entradaMotivoHospSCrearFichaHosp.place(x='300', y='330')
        
        self.entradaDiagnosticoSCrearFichaHosp = tk.Text(self, width = 40, height=3,  font=('MS Shell Dlg 2', '12'))
        self.entradaDiagnosticoSCrearFichaHosp.place(x='300', y='470')
        
        self.entradaAuthTutorSCrearFichaHosp = tk.Checkbutton(self, bg='#5C9C81')
        self.entradaAuthTutorSCrearFichaHosp.place(x='300', y='560')

        #Agregar buttons
        self.botonVolverSCrearFichaHosp = tk.Button(self, width= '25', height= '3',text='Volver')
        self.botonVolverSCrearFichaHosp.place(x='160', y='620')
        
        self.botonAgregarFichaHosp = tk.Button(self, width= '25', height= '3',text='Agregar Ficha Hospitalización')
        self.botonAgregarFichaHosp.place(x='420', y='620')


class screenFormularioFichaSedacion(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.configure(background='#5C9C81')
        self.labelNombrePacienteSCrearFichaSedacion = tk.Label(self, text="Nombre Paciente", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelNombrePacienteSCrearFichaSedacion.place(x='100', y='30')

        self.labelEspecieSCrearFichaSedacion = tk.Label(self, text="Especie", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelEspecieSCrearFichaSedacion.place(x='100', y='90')

        self.labelRazaSCrearFichaSedacion = tk.Label(self, text="Raza", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelRazaSCrearFichaSedacion.place(x='100', y='150')
        
        self.labelNombreTutorSCrearFichaSedacion = tk.Label(self, text="Nombre tutor", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelNombreTutorSCrearFichaSedacion.place(x='100', y='210')

        self.labelRutTutorSCrearFichaSedacion = tk.Label(self, text="Rut", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelRutTutorSCrearFichaSedacion.place(x='100', y='270')
        
        self.labelNumeroTelefonoSCrearFichaSedacion = tk.Label(self, text="Número de Teléfono", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelNumeroTelefonoSCrearFichaSedacion.place(x='100', y='330')

        self.labelDireccionSCrearFichaSedacion = tk.Label(self, text="Dirección", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelDireccionSCrearFichaSedacion.place(x='100', y='390')

        self.labelauthTutorSCrearFichaSedacion = tk.Label(self, text="Autorización Tutor", font=('MS Shell Dlg 2', '12'), bg='#5C9C81')
        self.labelauthTutorSCrearFichaSedacion.place(x='100', y='450')

        #Agregar Entrys
        self.entradaNombrePacienteSCrearFichaSedacion = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaNombrePacienteSCrearFichaSedacion.place(x='300', y='30')

        self.entradaEspecieSCrearFichaSedacion = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaEspecieSCrearFichaSedacion.place(x='300', y='90')

        self.entradaNombreTutorSCrearFichaSedacion = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaNombreTutorSCrearFichaSedacion.place(x='300', y='150')

        self.entradaRutTutorSCrearFichaSedacion = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaRutTutorSCrearFichaSedacion.place(x='300', y='210')

        self.entradaRazaSCrearFichaSedacion = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaRazaSCrearFichaSedacion.place(x='300', y='270')

        self.entradaNumTelefonoSCrearFichaSedacion = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaNumTelefonoSCrearFichaSedacion.place(x='300', y='330')

        self.entradaDireccionSCrearFichaSedacion = tk.Entry(self, width = 40, font=('MS Shell Dlg 2', '12'))
        self.entradaDireccionSCrearFichaSedacion.place(x='300', y='390')
        
        self.entradaAuthTutorSCrearFichaSedacion = tk.Checkbutton(self, bg='#5C9C81')
        self.entradaAuthTutorSCrearFichaSedacion.place(x='300', y='450')

        #Agregar buttons
        self.botonVolverSCrearFichaSedacion = tk.Button(self, width= '25', height= '3',text='Volver')
        self.botonVolverSCrearFichaSedacion.place(x='160', y='570')
        
        self.botonAgregarFichaSedacion = tk.Button(self, width= '25', height= '3',text='Agregar Ficha Hospitalización')
        self.botonAgregarFichaSedacion.place(x='420', y='570')


class screenAbstractMedico(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.configure(background='#5C9C81')
        self.abstractTextSAbstract = tk.Text(self, width = 70, height=25, font=('MS Shell Dlg 2', '12'))
        self.abstractTextSAbstract.place(x='320', y='90')
        
        self.botonVolverSAbstract = tk.Button(self, width= '25', height= '3',text='Volver')
        self.botonVolverSAbstract.place(x='530', y='620')

app = App()
app.mainloop()