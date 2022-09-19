import tkinter as tk
import customtkinter as ctk
from terminalVeterinario import *


terminalVet = Terminal()
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

        self.mascotaUtilizada:Mascota = None

        self.frames = {}

        self.screenIngresoLlave = screenIngresoLlave
        self.screenBuscarMascota = screenBuscarMascota
        self.screenDatosTotalMascota = screenDatosTotalMascota
        self.screenFormularioVerFicha = screenFormularioVerFicha
        self.screenFormularioCrearFicha = screenFormularioCrearFicha
        self.screenFormularioAgregarMascota = screenFormularioAgregarMascota
        self.screenFormularioFichaAuthCirugia = screenFormularioFichaAuthCirugia
        self.screenFormularioFichaHospt = screenFormularioFichaHospt
        self.screenFormularioFichaSedacion = screenFormularioFichaSedacion
        self.screenAbstractMedico = screenAbstractMedico

        self.framesTotales = {screenIngresoLlave, screenBuscarMascota, screenDatosTotalMascota, 
        screenFormularioVerFicha,screenFormularioCrearFicha, screenFormularioAgregarMascota, 
        screenFormularioFichaAuthCirugia, screenFormularioFichaHospt, screenFormularioFichaSedacion, 
        screenAbstractMedico}
        
        for F in self.framesTotales:
            frame = F(self, container)
            self.frames[F] = frame
            frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')


        if(terminalVet.validarTokenDeActivacion() == False):
            self.show_frame(screenIngresoLlave)
        else:
            self.show_frame(screenBuscarMascota)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def update_frame(self, cont, parent, container):
        frame = self.frames[cont]
        for F in self.framesTotales:
            if(F == type(frame)):
                frame.destroy()
                newFrame = F(parent, container)
                self.frames[cont] = newFrame
        newFrame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

    def setMascotaApp(self, mascotaUtilizar:Mascota):
        self.mascotaUtilizada = mascotaUtilizar

    def getMascotaApp(self):
        return self.mascotaUtilizada


class screenIngresoLlave(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple20 = ("Helvetica", 20)
        Font_tuple14 = ("Helvetica", 16)
        Font_tuple12 = ("Helvetica", 12)
        self.labelTitle = ctk.CTkLabel(self, text="Bienvenido al sistema MyPetRecord", text_font=Font_tuple20, text_color='black')
        self.labelTitle.pack(padx=10, pady=30)
        self.labelSubTitle = ctk.CTkLabel(self, text="Porfavor, ingrese la llave de acceso", text_font=Font_tuple14,text_color='black')
        #self.labelSubTitle.pack(padx=10, pady=30)
        self.entradaKey = ctk.CTkEntry(self, width = 500, text_font=Font_tuple14, fg_color="#F0EFEB", placeholder_text="Ingrese llave de acceso", placeholder_text_color="silver", justify = "center", text_color='black')
        self.entradaKey.pack(padx=10, pady=(150,30))
        self.botonConf = ctk.CTkButton(self, width=10, text='Confirmar', command=lambda: self.clickConfirmar(parent))
        self.botonConf.pack(padx=10, pady=30)
        self.labelErrorIngreso = ctk.CTkLabel(self, text="Llave no existente", text_font=Font_tuple12, text_color='red')

    def clickConfirmar(self, parent):
        keyAConf = self.entradaKey.get()
        if(terminalVet.validarLlaveConServidor(keyAConf) == False):
            self.labelErrorIngreso.pack(padx=20, pady=20)
        else:
            parent.show_frame(parent.screenBuscarMascota)


class screenBuscarMascota(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 14)
        self.searchFrame = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
        self.searchFrame.grid(row=0, column=0, padx=20 , pady=20)

        self.frameMensajes = ctk.CTkFrame(self.searchFrame, corner_radius=10, fg_color="#C5DEDD")

        self.entradaBuscar = ctk.CTkEntry(self.searchFrame, width = 600, text_font=Font_tuple, border_width=0, placeholder_text="Ingrese Codigo Mascota", placeholder_text_color="silver", text_color="#0D1D29", fg_color="#F0EFEB")
        self.entradaBuscar.grid(row=0, column=0, padx=10, pady=10)

        self.botonBuscar = ctk.CTkButton(self.searchFrame, width= 10, text="Buscar", text_font=Font_tuple, command= lambda: self.clickBuscar(parent, container), fg_color="#28587A")
        self.botonBuscar.grid(row=0, column=1, padx=10, pady=10)

        self.labelCodigoInvalido = ctk.CTkLabel(self.frameMensajes, text="Ingrese un código válido", text_font=Font_tuple, text_color='red')

        self.botonEntrar = ctk.CTkButton(self.searchFrame, width=8, text='Ingresar', text_font=Font_tuple, fg_color="#28587A", command=lambda: parent.update_frame(parent.screenDatosTotalMascota, parent, container))

    def clickBuscar(self, parent, container):
        codigoMascota = self.entradaBuscar.get()
        resultado = terminalVet.verificarMascotaEnSistema(codigoMascota)
        Font_tuple = ("Helvetica", 14)
        self.frameMensajes.grid(row=1, column=0, padx=10, pady=10)
        if(resultado[0] == "MalCodigo"):
            self.labelCodigoInvalido.grid(row=0, column=0,padx=10, pady=10)
        elif(resultado[0]=="MascotaLocal"):
            mascotaMostrar:Mascota = resultado[1]
            parent.setMascotaApp(mascotaMostrar)
            infoBasica = f'Codigo mascota:  {str(mascotaMostrar.getId())} , Nombre mascota:  {str(mascotaMostrar.getNombreMascota())} , Especie:   {str(mascotaMostrar.getEspecie())} \nRaza:   {str(mascotaMostrar.getRaza())}  , Dueño/a:   {str(mascotaMostrar.getNombreTutor())}'
            self.labelInfoBasica = ctk.CTkLabel(self.frameMensajes, justify='left', text= infoBasica, text_font=Font_tuple, text_color='black', width=100)
            self.labelInfoBasica.grid(row=1, column=0, padx=10, pady=30)
            self.botonEntrar.grid(row=1, column=1, padx=10, pady=10)
            

class screenDatosTotalMascota(ctk.CTkFrame): #HACERLA DPS
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ('Helvetica', 13)
        mascotaActual:Mascota = parent.getMascotaApp()
        if(mascotaActual != None):
            
            self.frameListaboxDatos = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameListaboxDatos.grid(row=0, column=0, padx=20 , pady=20)

            self.frameListboxFichas = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameListboxFichas.grid(row=0, column=1, padx=20 , pady=20)

            self.frameBotones = ctk.CTkFrame(self, corner_radius=10, fg_color="#C5DEDD")
            self.frameBotones.grid(row=0, column=2, padx=20 , pady=20)

            nombreMascota = str(mascotaActual.getNombreMascota())
            especieMascota = str(mascotaActual.getEspecie())
            razaMascota = str(mascotaActual.getRaza())
            colorMascota = str(mascotaActual.getColorMascota())
            rutTutor = str(mascotaActual.getRutTutor())
            numTelefono = str(mascotaActual.getNumeroTelefono())
            direccion = str(mascotaActual.getDireccion())


            listaDatosBasicos = [f'Nombre : {nombreMascota}', f'Especie: {especieMascota}', f'Raza: {razaMascota}', f'Color: {colorMascota}', f'RUT: {rutTutor}', f'Teléfono: {numTelefono}', f'Dirección :{direccion}']
            listaString = tk.StringVar(value=listaDatosBasicos)

            self.listDatosBasicos = tk.Listbox(
                self.frameListaboxDatos,
                listvariable=listaString,
                width=40,
                height=7,
                selectmode='browse',
                font=('Helvetica', '13'))
            self.listDatosBasicos.grid(row=0, column=0, padx=10, pady=10)

            i = 0
            alergiasTabla = mascotaActual.getAlergias()
            alergias = ''
            
            while(i <= (len(alergiasTabla)-1)):
                alergias = alergias + str(alergiasTabla[i][1])
                i += 1

            alergiasString = f'Alergias: {alergias}'
            alergiasMostrar = tk.StringVar(value=alergiasString)
            
            self.listaAlergias = tk.Listbox(
                self.frameListaboxDatos,
                listvariable=alergiasMostrar,
                width=40,
                height=7,
                selectmode='browse',
                font=('Helvetica', '13'))
            self.listaAlergias.grid(row = 1, column=0, padx=10, pady=10)

            operacionesTabla = mascotaActual.getRegistroDeOperaciones()
            operaciones = ''
            i = 0
            while(i <= (len(operacionesTabla)-1)):
                print('a')
                operaciones = operaciones + str(operacionesTabla[i][1])
                i += 1
            operacionesString = f'Operaciones: {operaciones}'
            
            operacionesMostrar = tk.StringVar(value=operacionesString)
            self.listaOperaciones = tk.Listbox(
                self.frameListaboxDatos,
                listvariable=operacionesMostrar,
                width=40,
                height=7,
                selectmode='browse',
                font=('Helvetica', '13'))
            self.listaOperaciones.grid(row = 2, column=0, padx=10, pady=10)

            vacunasTabla = mascotaActual.getVacunasSuministradas()
            vacunas = ''
            i = 0
            while(i <= (len(vacunasTabla)-1)):
                vacunas = vacunas + str(vacunasTabla[i][1])
                i += 1
            vacunasString = f'Vacunas: {vacunas}'
            vacunasMostrar = tk.StringVar(value=vacunasString)

            self.listaVacunas = tk.Listbox(
                self.frameListaboxDatos,
                listvariable=vacunasMostrar,
                width=40,
                height=7,
                selectmode='browse',
                font=('Helvetica', '13'))
            self.listaVacunas.grid(row = 3, column=0, padx=10, pady=10)

            idsFichas = mascotaActual.getIdsFichas()
            listaFechas = []
            i = 0
            while(i <= (len(idsFichas)-1)):
                aux = mascotaActual.getFechaConsulta(idsFichas[i])
                listaFechas.append(aux)
                i += 1

            fechasString = []
            i = 0
            while(i <= (len(listaFechas)-1)):
                stringAux = f'Ficha del : {listaFechas[i]}'
                fechasString.append(stringAux)
                i += 1

            #vacunasString = f'Ficha del : {vacunas}'
            fechasMostrar = tk.StringVar(value=fechasString)

            self.listFichasMedicas= tk.Listbox(
                self.frameListboxFichas,
                listvariable=fechasMostrar,
                width=36,
                height=20,
                selectmode='browse',
                font=('Helvetica', '13'))
            self.listFichasMedicas.grid(row = 0, column=0, padx=10, pady=10)

            self.buttonVerFicha = ctk.CTkButton(self.frameBotones, width= 175, height= 100,text='Ver Ficha', hover_color="#142C3D", text_font=Font_tuple,command=lambda: self.verSeleccionado(self.listFichasMedicas, parent, container, mascotaActual))
            self.buttonVerFicha.pack(padx=10, pady=20)

            self.botonVolverSDatosTotal = ctk.CTkButton(self.frameBotones, width= 175, height= 100,text='Volver', text_font=Font_tuple, command=lambda: parent.show_frame(parent.screenBuscarMascota), hover_color="#142C3D")
            self.botonVolverSDatosTotal.pack(padx=10, pady=20)

            self.buttonCrearFicha = ctk.CTkButton(self.frameBotones, width= 175, height= 100,text='Crear Ficha', hover_color="#142C3D", text_font=Font_tuple, command=lambda: parent.update_frame(parent.screenFormularioCrearFicha, parent, container))
            self.buttonCrearFicha.pack(padx=10, pady=20)

            self.labelErrorFicha = ctk.CTkLabel(self, text="Seleccione una ficha")

    def verSeleccionado(self, lista, parent, container, mascotaActual):
        item = lista.curselection()
        auxTexto = lista.get(item)
        textoSplit = auxTexto.split('Ficha del : ')
        fechaSolo = textoSplit[1]
        
        mascotaActual.setActualFichaMedicaConsulta(fechaSolo)
        parent.update_frame(parent.screenFormularioVerFicha, parent, container)
        
        
class screenFormularioVerFicha(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ('Helvetica', 12)
        #Agregar Labels--------------------------------------------------------------------------------------------------------------------------------
        mascotaActual:Mascota = parent.getMascotaApp()
        if(mascotaActual != None):
            
            idFicha = mascotaActual.getidFichaActual()

            self.frameForm = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameForm.grid(row=0, column=0, padx=20, pady=20)

            self.frameButtons = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameButtons.grid(row=0, column=1, padx=20, pady=20)

            self.labelSucursalSVerFicha = ctk.CTkLabel(self.frameForm, text="Sucursal Veterinaria", text_font=Font_tuple, text_color='black')
            self.labelSucursalSVerFicha.grid(row = 0, column = 0, padx=20, pady=12)
            
            self.labelVetACargoSVerFicha = ctk.CTkLabel(self.frameForm, text="Veterinario a cargo", text_font=Font_tuple, text_color='black')
            self.labelVetACargoSVerFicha.grid(row = 1, column = 0, padx=20, pady=12)
            
            self.labelFechaConsultaSVerFicha = ctk.CTkLabel(self.frameForm, text="Fecha Consulta", text_font=Font_tuple, text_color='black')
            self.labelFechaConsultaSVerFicha.grid(row = 2, column = 0, padx=20, pady=12)
            
            self.labelTratamientosConsultaSVerFicha = ctk.CTkLabel(self.frameForm, text="Tratamientos Consulta", text_font=Font_tuple, text_color='black')
            self.labelTratamientosConsultaSVerFicha.grid(row = 3, column = 0, padx=20, pady=12)
            
            self.labelMedicamentosConsultaSVerFicha = ctk.CTkLabel(self.frameForm, text="Medicamentos Consulta", text_font=Font_tuple, text_color='black')
            self.labelMedicamentosConsultaSVerFicha.grid(row = 4, column = 0, padx=20, pady=12)
            
            self.labelCausaVisitaSVerFicha = ctk.CTkLabel(self.frameForm, text="Causa Visita", text_font=Font_tuple, text_color='black')
            self.labelCausaVisitaSVerFicha.grid(row = 5, column = 0, padx=20, pady=12)
            
            self.labelVacSuministradasSVerFicha = ctk.CTkLabel(self.frameForm, text="Vacunas Suministradas", text_font=Font_tuple, text_color='black')
            self.labelVacSuministradasSVerFicha.grid(row = 6, column = 0, padx=20, pady=12)
            
            self.labelFrecRespiratoriaSVerFicha = ctk.CTkLabel(self.frameForm, text="Frecuencia Respiratoria", text_font=Font_tuple, text_color='black')
            self.labelFrecRespiratoriaSVerFicha.grid(row = 7, column = 0, padx=20, pady=12)
            
            self.labelFrecCardiacaSVerFicha = ctk.CTkLabel(self.frameForm, text="Frecuencia Cardiaca", text_font=Font_tuple, text_color='black')
            self.labelFrecCardiacaSVerFicha.grid(row = 8, column = 0, padx=20, pady=12)

            self.labelPesoSVerFicha = ctk.CTkLabel(self.frameForm, text="Peso", text_font=Font_tuple, text_color='black')
            self.labelPesoSVerFicha.grid(row = 9, column = 0, padx=20, pady=12)
            
            self.labelEdadSVerFicha = ctk.CTkLabel(self.frameForm, text="Edad", text_font=Font_tuple, text_color='black')
            self.labelEdadSVerFicha.grid(row = 10, column = 0, padx=20, pady=12)

            self.labelTemperaturaSVerFicha = ctk.CTkLabel(self.frameForm, text="Temperatura", text_font=Font_tuple, text_color='black')
            self.labelTemperaturaSVerFicha.grid(row = 11, column = 0, padx=20, pady=12)
            
            #Agregar Entrys------------------------------------------------------------------------------------------------------------------------------
            textVarSucursal = tk.StringVar()
            textVarVetACargo = tk.StringVar()
            textVarFecha = tk.StringVar()
            textVarTratamiento = tk.StringVar()
            textVarMedicamento = tk.StringVar()
            textVarCausa = tk.StringVar()
            textVarVacunas = tk.StringVar()
            textVarFrecResp = tk.StringVar()
            textVarFrecCardio = tk.StringVar()
            textVarPeso = tk.StringVar()
            textVarEdad = tk.StringVar()
            textVarTemp = tk.StringVar()

            textVarSucursal.set(str(mascotaActual.getSucursalVeterinaria(idFicha)))
            self.entradaSucursalSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=textVarSucursal, state=DISABLED)
            self.entradaSucursalSVerFicha.grid(row = 0, column = 1, padx=20, pady=12)

            textVarVetACargo.set(str(mascotaActual.getVeterinarioACargo(idFicha)))
            self.entradaVetACargoSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=textVarVetACargo, state=DISABLED)
            self.entradaVetACargoSVerFicha.grid(row = 1, column = 1, padx=20, pady=12)
            
            textVarFecha.set(str(mascotaActual.getFechaConsulta(idFicha)))
            self.entradaFechaConsultaSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=textVarFecha, state=DISABLED)
            self.entradaFechaConsultaSVerFicha.grid(row = 2, column = 1, padx=20, pady=12)


            tratamientos = mascotaActual.getTratamiento(idFicha)
            tratamientosString = ''
            
            for i in range(len(tratamientos)):
                if(i == len(tratamientos)-1):
                    tratamientosString = tratamientosString + tratamientos[i]['nombreTratamiento'] + '.'
                else:
                    tratamientosString = tratamientosString + tratamientos[i]['nombreTratamiento'] + ','
            textVarTratamiento.set(str(tratamientosString))
            self.entradaTratamientosConsultaSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=textVarTratamiento, state=DISABLED)
            self.entradaTratamientosConsultaSVerFicha.grid(row = 3, column = 1, padx=20, pady=12)
            
            medicamentos = mascotaActual.getMedicamentosConsulta(idFicha)
            medicamentosString = ''
            
            for i in range(len(tratamientos)):
                if(i == len(medicamentos)-1):
                    medicamentosString = medicamentosString + medicamentos[i]['nomMedicamento'] + '.'
                else:
                    medicamentosString = medicamentosString + medicamentos[i]['nomMedicamento'] + ','
            textVarMedicamento.set(str(medicamentosString))
            self.entradaMedicamentosConsultaSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=textVarMedicamento, state=DISABLED)
            self.entradaMedicamentosConsultaSVerFicha.grid(row = 4, column = 1, padx=20, pady=12)

            #Trat
            causaVisita = mascotaActual.getTratamiento(idFicha)
            causaVisitaString = ''
            
            for i in range(len(tratamientos)):
                if(i == len(causaVisita)-1):
                    causaVisitaString = causaVisitaString + causaVisita[i]['causaVisita'] + '.'
                else:
                    causaVisitaString = causaVisitaString + causaVisita[i]['causaVisita'] + ','
            textVarCausa.set(str(causaVisitaString))
            self.entradaCausaVisitaSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=textVarCausa, state=DISABLED)
            self.entradaCausaVisitaSVerFicha.grid(row = 5, column = 1, padx=20, pady=12)

            vacunas = mascotaActual.getVacunasSuministradasConsulta(idFicha)
            vacunasString = ''
            
            for i in range(len(tratamientos)):
                if(i == len(vacunas)-1):
                    vacunasString = vacunasString + vacunas[i]['nomVacuna'] + '.'
                else:
                    vacunasString = vacunasString + vacunas[i]['nomVacuna'] + ','

            textVarVacunas.set(str(vacunasString))
            self.entradaVacSuministradasSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=textVarVacunas, state=DISABLED)
            self.entradaVacSuministradasSVerFicha.grid(row = 6, column = 1, padx=20, pady=12)

            textVarFrecResp.set(str(mascotaActual.getFrecRespiratoria(idFicha)))
            self.entradaFrecRespiratoriaSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=textVarFrecResp, state=DISABLED)
            self.entradaFrecRespiratoriaSVerFicha.grid(row = 7, column = 1, padx=20, pady=12)

            textVarFrecCardio.set(str(mascotaActual.getFrecCardiaca(idFicha)))
            self.entradaFrecCardiacaSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=textVarFrecCardio, state=DISABLED)
            self.entradaFrecCardiacaSVerFicha.grid(row = 8, column = 1, padx=20, pady=12)

            textVarPeso.set(str(mascotaActual.getPeso(idFicha)))
            self.entradaPesoSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=textVarPeso, state=DISABLED)
            self.entradaPesoSVerFicha.grid(row = 9, column = 1, padx=20, pady=12)

            textVarEdad.set(str(mascotaActual.getEdad(idFicha)))
            self.entradaEdadSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=textVarEdad, state=DISABLED)
            self.entradaEdadSVerFicha.grid(row = 10, column = 1, padx=20, pady=12)

            textVarTemp.set(str(mascotaActual.getTemp(idFicha)))
            self.entradaTemperaturaSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=textVarTemp, state=DISABLED)
            self.entradaTemperaturaSVerFicha.grid(row = 11, column = 1, padx=20, pady=12)

            #Agregar Buttons
            self.botonVolverSVerFicha = ctk.CTkButton(self.frameButtons, width= 200, height= 80, text='Volver', text_font=Font_tuple, hover_color="#142C3D", command=lambda: self.volverSDTotalMascota(parent, container, mascotaActual, idFicha))
            self.botonVolverSVerFicha.pack(padx= 10, pady = (33,40))

            if (mascotaActual.getHospitalizacion(idFicha) == True):
                self.botonVerFichaHosp = ctk.CTkButton(self.frameButtons, width= 200, height= 80, text='Ver Ficha Hospitalizacion', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenFormularioFichaHospt, parent, container))
                self.botonVerFichaHosp.pack(padx= 10, pady = 40)
            
            if(mascotaActual.getSedacion(idFicha) == True):
                self.botonVerFichaSedacion = ctk.CTkButton(self.frameButtons, width= 200, height= 80, text='Ver Ficha Sedación', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenFormularioFichaSedacion, parent, container))
                self.botonVerFichaSedacion.pack(padx= 10, pady = 40)

            if(mascotaActual.getOperacion(idFicha) == True):
                self.botonVerFichaOperacion = ctk.CTkButton(self.frameButtons, width= 200, height= 80, text='Ver Ficha Operación', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenFormularioFichaAuthCirugia, parent, container))
                self.botonVerFichaOperacion.pack(padx= 10, pady = (40, 33))

    def volverSDTotalMascota(self, parent, container, mascotaActual, idFicha):
        mascotaActual.quitarActualFichaMedicaConsulta(idFicha)
        parent.update_frame(parent.screenDatosTotalMascota, parent, container)

    
class screenFormularioCrearFicha(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ('Helvetica', 12)
        #Agregar Labels--------------------------------------------------------------------------------------------------------------------------------
        self.frameFormSCrearFicha = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
        self.frameFormSCrearFicha.grid(row=0, column=0, padx=20, pady=20)

        self.frameButtonsSCrearFicha = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
        self.frameButtonsSCrearFicha.grid(row=0, column=1, padx=20, pady=20)

        self.frameButtonsVolver = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
        self.frameButtonsVolver.grid(row=0, column=2, padx=20, pady=20)

        self.labelSucursalSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Sucursal Veterinaria", text_font=Font_tuple, text_color='black')
        self.labelSucursalSCrearFicha.grid(row = 0, column = 0, padx=20, pady=12)
        
        self.labelVetACargoSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Veterinario a cargo", text_font=Font_tuple, text_color='black')
        self.labelVetACargoSCrearFicha.grid(row = 1, column = 0, padx=20, pady=12)
        
        self.labelFechaConsultaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Fecha Consulta", text_font=Font_tuple, text_color='black')
        self.labelFechaConsultaSCrearFicha.grid(row = 2, column = 0, padx=20, pady=12)
        
        self.labelTratamientosConsultaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Tratamientos Consulta", text_font=Font_tuple, text_color='black')
        self.labelTratamientosConsultaSCrearFicha.grid(row = 3, column = 0, padx=20, pady=12)
        
        self.labelMedicamentosConsultaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Medicamentos Consulta", text_font=Font_tuple, text_color='black')
        self.labelMedicamentosConsultaSCrearFicha.grid(row = 4, column = 0, padx=20, pady=12)
        
        self.labelCausaVisitaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Causa Visita", text_font=Font_tuple, text_color='black')
        self.labelCausaVisitaSCrearFicha.grid(row = 5, column = 0, padx=20, pady=12)
        
        self.labelVacSuministradasSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Vacunas Suministradas", text_font=Font_tuple, text_color='black')
        self.labelVacSuministradasSCrearFicha.grid(row = 6, column = 0, padx=20, pady=12)
        
        self.labelFrecRespiratoriaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Frecuencia Respiratoria", text_font=Font_tuple, text_color='black')
        self.labelFrecRespiratoriaSCrearFicha.grid(row = 7, column = 0, padx=20, pady=12)
        
        self.labelFrecCardiacaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Frecuencia Cardiaca", text_font=Font_tuple, text_color='black')
        self.labelFrecCardiacaSCrearFicha.grid(row = 8, column = 0, padx=20, pady=12)

        self.labelPesoSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Peso", text_font=Font_tuple, text_color='black')
        self.labelPesoSCrearFicha.grid(row = 9, column = 0, padx=20, pady=12)
        
        self.labelEdadSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Edad", text_font=Font_tuple, text_color='black')
        self.labelEdadSCrearFicha.grid(row = 10, column = 0, padx=20, pady=12)

        self.labelTemperaturaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Temperatura", text_font=Font_tuple, text_color='black')
        self.labelTemperaturaSCrearFicha.grid(row = 11, column = 0, padx=20, pady=12)
        
        #Agregar Entrys------------------------------------------------------------------------------------------------------------------------------

        self.entradaSucursalSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey')
        self.entradaSucursalSCrearFicha.grid(row = 0, column = 1, padx=20, pady=12)

        self.entradaVetACargoSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey')
        self.entradaVetACargoSCrearFicha.grid(row = 1, column = 1, padx=20, pady=12)

        self.entradaFechaConsultaSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey')
        self.entradaFechaConsultaSCrearFicha.grid(row = 2, column = 1, padx=20, pady=12)

        self.entradaTratamientosConsultaSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey')
        self.entradaTratamientosConsultaSCrearFicha.grid(row = 3, column = 1, padx=20, pady=12)

        self.entradaMedicamentosConsultaSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey')
        self.entradaMedicamentosConsultaSCrearFicha.grid(row = 4, column = 1, padx=20, pady=12)

        self.entradaCausaVisitaSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey')
        self.entradaCausaVisitaSCrearFicha.grid(row = 5, column = 1, padx=20, pady=12)

        self.entradaVacSuministradasSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey')
        self.entradaVacSuministradasSCrearFicha.grid(row = 6, column = 1, padx=20, pady=12)

        self.entradaFrecRespiratoriaSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey')
        self.entradaFrecRespiratoriaSCrearFicha.grid(row = 7, column = 1, padx=20, pady=12)

        self.entradaFrecCardiacaSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey')
        self.entradaFrecCardiacaSCrearFicha.grid(row = 8, column = 1, padx=20, pady=12)

        self.entradaPesoSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey')
        self.entradaPesoSCrearFicha.grid(row = 9, column = 1, padx=20, pady=12)

        self.entradaEdadSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey')
        self.entradaEdadSCrearFicha.grid(row = 10, column = 1, padx=20, pady=12)

        self.entradaTemperaturaSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey')
        self.entradaTemperaturaSCrearFicha.grid(row = 11, column = 1, padx=20, pady=12)

        #Agregar Buttons
        self.botonVolverSCrearFicha = ctk.CTkButton(self.frameButtonsVolver, width= 200, height= 80, text='Volver', text_font=Font_tuple, hover_color="#142C3D")
        self.botonVolverSCrearFicha.pack(padx= 10, pady = (33,40))

        self.botonAgregarFichaGeneralSCrearFicha = ctk.CTkButton(self.frameButtonsSCrearFicha, width=250, height=80, text='Agregar Ficha General', text_font=Font_tuple, hover_color="#142C3D")
        self.botonAgregarFichaGeneralSCrearFicha.pack(padx=10, pady=40)

        self.botonAgregarFichaHosp = ctk.CTkButton(self.frameButtonsSCrearFicha, width= 250, height= 80, text='Agregar Ficha Hospitalizacion', text_font=Font_tuple, hover_color="#142C3D")
        self.botonAgregarFichaHosp.pack(padx= 10, pady = 40)

        self.botonAgregarFichaSedacion = ctk.CTkButton(self.frameButtonsSCrearFicha, width= 250, height= 80, text='Agregar Ficha Sedación', text_font=Font_tuple, hover_color="#142C3D")
        self.botonAgregarFichaSedacion.pack(padx= 10, pady = 40)

        self.botonAgregarFichaOperacion = ctk.CTkButton(self.frameButtonsSCrearFicha, width= 250, height= 80, text='Agregar Ficha Operación', text_font=Font_tuple, hover_color="#142C3D")
        self.botonAgregarFichaOperacion.pack(padx= 10, pady = (40, 33))
    

class screenFormularioAgregarMascota(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 12)

        self.frameFormSAgregarMascota = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
        self.frameFormSAgregarMascota.grid(row=0, column=0, padx=20, pady=20)

        self.frameButtonsSAgregarMascota = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
        self.frameButtonsSAgregarMascota.grid(row=0, column=1, padx=20, pady=20)

        self.labelNombreMascotaSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Nombre Mascota", text_font=Font_tuple, text_color="black")
        self.labelNombreMascotaSAgregarMascota.grid(row=0, column=0, padx=20, pady=20)

        self.labelEspecieSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Especie ", text_font=Font_tuple, text_color="black")
        self.labelEspecieSAgregarMascota.grid(row=1, column=0, padx=20, pady=20)

        self.labelColorSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Color", text_font=Font_tuple, text_color="black")
        self.labelColorSAgregarMascota.grid(row=2, column=0, padx=20, pady=20)

        self.labelRazaSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Raza", text_font=Font_tuple, text_color="black")
        self.labelRazaSAgregarMascota.grid(row=3, column=0, padx=20, pady=20)

        self.labelNombreTutorSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Nombre Tutor", text_font=Font_tuple, text_color="black")
        self.labelNombreTutorSAgregarMascota.grid(row=4, column=0, padx=20, pady=20)
        
        self.labelRutTutorSAgregarMascota =ctk.CTkLabel(self.frameFormSAgregarMascota, text="Rut Tutor", text_font=Font_tuple, text_color="black")
        self.labelRutTutorSAgregarMascota.grid(row=5, column=0, padx=20, pady=20)

        self.labelNumeroTelefonoSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Número de Teléfono", text_font=Font_tuple, text_color="black")
        self.labelNumeroTelefonoSAgregarMascota.grid(row=6, column=0, padx=20, pady=20)

        self.labelDireccionTutorSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Dirección Tutor", text_font=Font_tuple, text_color="black")
        self.labelDireccionTutorSAgregarMascota.grid(row=7, column=0, padx=20, pady=20)


        #Agregar Entrys
        self.entradaNombreMascotaSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaNombreMascotaSAgregarMascota.grid(row=0, column=1, padx=20, pady=20)

        self.entradaEspecieSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaEspecieSAgregarMascota.grid(row=1, column=1, padx=20, pady=20)

        self.entradaColorSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaColorSAgregarMascota.grid(row=2, column=1, padx=20, pady=20)

        self.entradaRazaSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaRazaSAgregarMascota.grid(row=3, column=1, padx=20, pady=20)
        
        self.entradaNombreTutorSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaNombreTutorSAgregarMascota.grid(row=4, column=1, padx=20, pady=20)
        
        self.entradaNombreMascotaSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaNombreMascotaSAgregarMascota.grid(row=5, column=1, padx=20, pady=20)
        
        self.entradaNumeroTelefonoSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaNumeroTelefonoSAgregarMascota.grid(row=6, column=1, padx=20, pady=20)

        self.entradaDireccionTutorSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaDireccionTutorSAgregarMascota.grid(row=7, column=1, padx=20, pady=20)

        #Agregar buttons
        self.botonVolverSCrearFicha = ctk.CTkButton(self.frameButtonsSAgregarMascota, width= 200, height= 120,text='Volver', hover_color="#142C3D")
        self.botonVolverSCrearFicha.pack(padx= 10, pady = 40)
        
        self.botonAgregarMascota = ctk.CTkButton(self.frameButtonsSAgregarMascota, width= 200, height= 120,text='Agregar Mascota', hover_color="#142C3D")
        self.botonAgregarMascota.pack(padx= 10, pady = 40)


class screenFormularioFichaAuthCirugia(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 13)
        mascotaActual:Mascota = parent.getMascotaApp()
        if(mascotaActual != None):
            
            idFicha = mascotaActual.getidFichaActual()
            self.frameFormSFichaAuthCirugia = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameFormSFichaAuthCirugia.grid(row=0, column=0, padx=20, pady=10)
    
            self.frameButtonsSFichaAuthCirugia = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameButtonsSFichaAuthCirugia.grid(row=0, column=1, padx=20, pady=10)
    
            self.frameText = ctk.CTkFrame(self.frameFormSFichaAuthCirugia, corner_radius=0, fg_color="#4e5257")
            self.frameText.grid(row=6, column=1, padx=20, pady=10)
    
            self.labelNombrePacienteSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Nombre Paciente", text_font=Font_tuple, text_color="black")
            self.labelNombrePacienteSFichaAuthCirugia.grid(row=0, column=0, padx=20, pady=10)
    
            self.labelPesoSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Peso", text_font=Font_tuple, text_color="black")
            self.labelPesoSFichaAuthCirugia.grid(row=1, column=0, padx=20, pady=10)
    
            self.labelEspecieSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Especie", text_font=Font_tuple, text_color="black")
            self.labelEspecieSFichaAuthCirugia.grid(row=2, column=0, padx=20, pady=10)
    
            self.labelEdadSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Edad", text_font=Font_tuple, text_color="black")
            self.labelEdadSFichaAuthCirugia.grid(row=3, column=0, padx=20, pady=10)
            
            self.labelRazaSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Raza", text_font=Font_tuple, text_color="black")
            self.labelRazaSFichaAuthCirugia.grid(row=4, column=0, padx=20, pady=10)
            
            self.labelColorSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Color", text_font=Font_tuple, text_color="black")
            self.labelColorSFichaAuthCirugia.grid(row=5, column=0, padx=20, pady=10)
            
            self.labelDiagnosticoSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Diagnóstico", text_font=Font_tuple, text_color="black")
            self.labelDiagnosticoSFichaAuthCirugia.grid(row=6, column=0, padx=20, pady=10)
            
            self.labelCirugiaARealizarSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Cirugía a Realizar", text_font=Font_tuple, text_color="black")
            self.labelCirugiaARealizarSFichaAuthCirugia.grid(row=7, column=0, padx=20, pady=10)
            
            self.labelNombreDelTutorSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Nombre del Tutor", text_font=Font_tuple, text_color="black")
            self.labelNombreDelTutorSFichaAuthCirugia.grid(row=8, column=0, padx=20, pady=10)
    
            self.labelRutTutorSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Rut Tutor", text_font=Font_tuple, text_color="black")
            self.labelRutTutorSFichaAuthCirugia.grid(row=9, column=0, padx=20, pady=10)
            
            self.labelNumeroTelefonoSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Número de Teléfono", text_font=Font_tuple, text_color="black")
            self.labelNumeroTelefonoSFichaAuthCirugia.grid(row=10, column=0, padx=20, pady=10)
    
            self.labelDireccionSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Dirección", text_font=Font_tuple, text_color="black")
            self.labelDireccionSFichaAuthCirugia.grid(row=11, column=0, padx=20, pady=10)
    
            self.labelAuthTutorSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Autorizacion tutor", text_font=Font_tuple, text_color="black")
            self.labelAuthTutorSFichaAuthCirugia.grid(row=12, column=0, padx=20, pady=10)
    
            self.labelErrorCamposSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Error en el formato", text_font=Font_tuple, text_color="black")
    
            #Agregar Entrys
            textVarNombrePaciente = tk.StringVar()
            textVarPeso = tk.StringVar()
            textVarEspecie = tk.StringVar()
            textVarEdad = tk.StringVar()
            textVarRaza = tk.StringVar()
            textVarColor = tk.StringVar()
            textVarCirugia = tk.StringVar()
            textVarNombreTutor = tk.StringVar()
            textVarRut = tk.StringVar()
            textVarTelefono = tk.StringVar()
            textVarDireccion = tk.StringVar()
            
            textVarNombrePaciente.set(mascotaActual.getNombreMascota())
            self.entradaNombrePacienteSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB", text=textVarNombrePaciente,  state=DISABLED)
            self.entradaNombrePacienteSFichaAuthCirugia.grid(row=0, column=1, padx=20, pady=10)

            textVarPeso.set(mascotaActual.getPeso(idFicha))
            self.entradaPesoSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB", text=textVarPeso,  state=DISABLED)
            self.entradaPesoSFichaAuthCirugia.grid(row=1, column=1, padx=20, pady=10)

            textVarEspecie.set(mascotaActual.getEspecie())
            self.entradaEspecieSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB", text=textVarEspecie,  state=DISABLED)
            self.entradaEspecieSFichaAuthCirugia.grid(row=2, column=1, padx=20, pady=10)

            textVarEdad.set(mascotaActual.getEdad(idFicha))
            self.entradaEdadConsultaSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB", text=textVarEdad,  state=DISABLED)
            self.entradaEdadConsultaSFichaAuthCirugia.grid(row=3, column=1, padx=20, pady=10)
            
            textVarRaza.set(mascotaActual.getRaza())
            self.entradaRazaSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB", text=textVarRaza,  state=DISABLED)
            self.entradaRazaSFichaAuthCirugia.grid(row=4, column=1, padx=20, pady=10)

            textVarColor.set(mascotaActual.getColorMascota())
            self.entradaColorSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB", text=textVarColor,  state=DISABLED)
            self.entradaColorSFichaAuthCirugia.grid(row=5, column=1, padx=20, pady=10)

            operacion = mascotaActual.getOperacionFicha(idFicha)

            
            self.entradaDiagnosticoSFichaAuthCirugia = tk.Text(self.frameText, width = 44, height= 3, background="#F0EFEB", font=("Helvetica", 12), state=NORMAL)
            self.entradaDiagnosticoSFichaAuthCirugia.delete(1.0, END)
            self.entradaDiagnosticoSFichaAuthCirugia.grid(row=0, column=0, padx=2, pady=2)
            self.entradaDiagnosticoSFichaAuthCirugia.insert(END, operacion['diagnostico'])
            self.entradaDiagnosticoSFichaAuthCirugia.configure(state="disabled")


            textVarCirugia.set(operacion['cirugiaARealizar'])
            self.entradaCirugiaARealizarSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB", text=textVarCirugia,  state=DISABLED)
            self.entradaCirugiaARealizarSFichaAuthCirugia.grid(row=7, column=1, padx=20, pady=10)

            textVarNombreTutor.set(mascotaActual.getNombreTutor())
            self.entradaNombreTutorSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB", text=textVarNombreTutor,  state=DISABLED)
            self.entradaNombreTutorSFichaAuthCirugia.grid(row=8, column=1, padx=20, pady=10)

            textVarRut.set(mascotaActual.getRutTutor())
            self.entradaRutSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB", text=textVarRut,  state=DISABLED)
            self.entradaRutSFichaAuthCirugia.grid(row=9, column=1, padx=20, pady=10)

            textVarTelefono.set(mascotaActual.getNumeroTelefono())
            self.entradaNumTelefonoSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB", text=textVarTelefono,  state=DISABLED)
            self.entradaNumTelefonoSFichaAuthCirugia.grid(row=10, column=1, padx=20, pady=10)

            textVarDireccion.set(mascotaActual.getDireccion())
            self.entradaDireccionSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB", text=textVarDireccion,  state=DISABLED)
            self.entradaDireccionSFichaAuthCirugia.grid(row=11, column=1, padx=20, pady=10)

            var = tk.IntVar()
            var.set(1)

            if(operacion['autTutor'] == True):
                self.entradaAuthTutorSFichaAuthCirugia = ctk.CTkCheckBox(self.frameFormSFichaAuthCirugia, fg_color="#0D1D29", border_width=2, border_color="black", variable=var, onvalue=1, text="", state=DISABLED)
            else:
                self.entradaAuthTutorSFichaAuthCirugia = ctk.CTkCheckBox(self.frameFormSFichaAuthCirugia, fg_color="#0D1D29", border_width=2, border_color="black", variable=var, offvalue=0, state=DISABLED, text="")
            self.entradaAuthTutorSFichaAuthCirugia.grid(row=12, column=1, padx=20, pady=10)
    
            #Agregar botones
            self.botonAgregarFichaSFichaAuthCirugia = ctk.CTkButton(self.frameButtonsSFichaAuthCirugia, width= 250, height= 120, text='Agregar Ficha Operación', text_font=Font_tuple, hover_color="#142C3D")
            self.botonAgregarFichaSFichaAuthCirugia.pack(padx= 10, pady = 40)
    
            self.botonVolverSFichaAuthCirugia = ctk.CTkButton(self.frameButtonsSFichaAuthCirugia, width= 250, height= 120, text='Volver', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenFormularioVerFicha, parent, container))
            self.botonVolverSFichaAuthCirugia.pack(padx= 10, pady = 40)


class screenFormularioFichaHospt(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 12)
        Font_tuple10 = ("Helvetica", 10)

        self.frameFormSCrearFichaHosp = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
        self.frameFormSCrearFichaHosp.grid(row=0, column=0, padx=20, pady=10)

        self.frameButtonsSCrearFichaHosp = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
        self.frameButtonsSCrearFichaHosp.grid(row=0, column=1, padx=20, pady=10)

        self.frameText1 = ctk.CTkFrame(self.frameFormSCrearFichaHosp, corner_radius=0, fg_color="#4e5257")
        self.frameText1.grid(row=6, column=1, padx=20, pady=10)

        self.frameText2 = ctk.CTkFrame(self.frameFormSCrearFichaHosp, corner_radius=0, fg_color="#4e5257")
        self.frameText2.grid(row=7, column=1, padx=20, pady=10)

        #Agregar Labels
        self.labelNombreMascotaSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Nombre Mascota", text_font=Font_tuple, text_color="black")
        self.labelNombreMascotaSCrearFichaHosp.grid(row=0, column=0, padx=20, pady=10)

        self.labelEspecieSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Especie ", text_font=Font_tuple, text_color="black")
        self.labelEspecieSCrearFichaHosp.grid(row=1, column=0, padx=20, pady=10)

        self.labelPesoSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Peso", text_font=Font_tuple, text_color="black")
        self.labelPesoSCrearFichaHosp.grid(row=2, column=0, padx=20, pady=10)

        self.labelEdadSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Edad", text_font=Font_tuple, text_color="black")
        self.labelEdadSCrearFichaHosp.grid(row=3, column=0, padx=20, pady=10)

        self.labelRazaSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Raza", text_font=Font_tuple, text_color="black")
        self.labelRazaSCrearFichaHosp.grid(row=4, column=0, padx=20, pady=10)

        self.labelColorSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Color", text_font=Font_tuple, text_color="black")
        self.labelColorSCrearFichaHosp.grid(row=5, column=0, padx=20, pady=10)

        self.labelMotivoHospSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Motivo de Hospitalización", text_font=Font_tuple, text_color="black")
        self.labelMotivoHospSCrearFichaHosp.grid(row=6, column=0, padx=20, pady=10)

        self.labelDiagnosticoSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Diagnóstico", text_font=Font_tuple, text_color="black")
        self.labelDiagnosticoSCrearFichaHosp.grid(row=7, column=0, padx=20, pady=10)

        self.labelAuthTutorSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Autorización tutor", text_font=Font_tuple, text_color="black")
        self.labelAuthTutorSCrearFichaHosp.grid(row=8, column=0, padx=20, pady=10)   


        #Agregar Entrys
        self.entradaNombrePacienteSCrearFichaHosp = ctk.CTkEntry(self.frameFormSCrearFichaHosp, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaNombrePacienteSCrearFichaHosp.grid(row=0, column=1, padx=20, pady=10)

        self.entradaPesoSCrearFichaHosp = ctk.CTkEntry(self.frameFormSCrearFichaHosp, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaPesoSCrearFichaHosp.grid(row=1, column=1, padx=20, pady=10)

        self.entradaEspecieSCrearFichaHosp = ctk.CTkEntry(self.frameFormSCrearFichaHosp, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaEspecieSCrearFichaHosp.grid(row=2, column=1, padx=20, pady=10)

        self.entradaEdadSCrearFichaHosp = ctk.CTkEntry(self.frameFormSCrearFichaHosp, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaEdadSCrearFichaHosp.grid(row=3, column=1, padx=20, pady=10)

        self.entradaRazaSCrearFichaHosp = ctk.CTkEntry(self.frameFormSCrearFichaHosp, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaRazaSCrearFichaHosp.grid(row=4, column=1, padx=20, pady=10)

        self.entradaColorSCrearFichaHosp = ctk.CTkEntry(self.frameFormSCrearFichaHosp, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaColorSCrearFichaHosp.grid(row=5, column=1, padx=20, pady=10)

        self.entradaMotivoHospSCrearFichaHosp = tk.Text(self.frameText1, width = 40, height=6, font=("Helvetica", "12"), background="#F0EFEB")
        self.entradaMotivoHospSCrearFichaHosp.grid(row=0, column=0, padx=2, pady=2)
        
        self.entradaDiagnosticoSCrearFichaHosp = tk.Text(self.frameText2, width = 40, height=3, font=("Helvetica", "12"), background="#F0EFEB")
        self.entradaDiagnosticoSCrearFichaHosp.grid(row=0, column=0, padx=2, pady=2)
        
        self.entradaAuthTutorSCrearFichaHosp = ctk.CTkCheckBox(self.frameFormSCrearFichaHosp, text="", fg_color="#0D1D29", border_width=2, border_color="grey")
        self.entradaAuthTutorSCrearFichaHosp.grid(row=8, column=1, padx=20, pady=10)

        #Agregar buttons
        self.botonVolverSCrearFichaHosp = ctk.CTkButton(self.frameButtonsSCrearFichaHosp, width=200, height=120, text='Volver', text_font=Font_tuple, hover_color="#142C3D")
        self.botonVolverSCrearFichaHosp.pack(padx= 10, pady = 40)
        
        self.botonAgregarFichaHosp = ctk.CTkButton(self.frameButtonsSCrearFichaHosp, width=200, height=120, text='Agregar Ficha Hospitalización', text_font=Font_tuple10, hover_color="#142C3D")
        self.botonAgregarFichaHosp.pack(padx= 10, pady = 40)


class screenFormularioFichaSedacion(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 12)
        Font_tuple10 = ("Helvetica", 10)
        self.frameFormSCrearFichaSedacion = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
        self.frameFormSCrearFichaSedacion.grid(row=0, column=0, padx=20, pady=10)

        self.frameButtonsSCrearFichaSedacion = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
        self.frameButtonsSCrearFichaSedacion.grid(row=0, column=1, padx=20, pady=10)

        self.labelNombrePacienteSCrearFichaSedacion = ctk.CTkLabel( self.frameFormSCrearFichaSedacion, text="Nombre Paciente", text_font=Font_tuple, text_color="black")
        self.labelNombrePacienteSCrearFichaSedacion.grid(row=0, column=0, padx=20, pady=10)

        self.labelEspecieSCrearFichaSedacion = ctk.CTkLabel( self.frameFormSCrearFichaSedacion, text="Especie", text_font=Font_tuple, text_color="black")
        self.labelEspecieSCrearFichaSedacion.grid(row=1, column=0, padx=20, pady=10)

        self.labelRazaSCrearFichaSedacion = ctk.CTkLabel( self.frameFormSCrearFichaSedacion, text="Raza", text_font=Font_tuple, text_color="black")
        self.labelRazaSCrearFichaSedacion.grid(row=2, column=0, padx=20, pady=10)
        
        self.labelNombreTutorSCrearFichaSedacion = ctk.CTkLabel( self.frameFormSCrearFichaSedacion, text="Nombre tutor", text_font=Font_tuple, text_color="black")
        self.labelNombreTutorSCrearFichaSedacion.grid(row=3, column=0, padx=20, pady=10)

        self.labelRutTutorSCrearFichaSedacion = ctk.CTkLabel( self.frameFormSCrearFichaSedacion, text="Rut", text_font=Font_tuple, text_color="black")
        self.labelRutTutorSCrearFichaSedacion.grid(row=4, column=0, padx=20, pady=10)
        
        self.labelNumeroTelefonoSCrearFichaSedacion = ctk.CTkLabel( self.frameFormSCrearFichaSedacion, text="Número de Teléfono", text_font=Font_tuple, text_color="black")
        self.labelNumeroTelefonoSCrearFichaSedacion.grid(row=5, column=0, padx=20, pady=10)

        self.labelDireccionSCrearFichaSedacion = ctk.CTkLabel( self.frameFormSCrearFichaSedacion, text="Dirección", text_font=Font_tuple, text_color="black")
        self.labelDireccionSCrearFichaSedacion.grid(row=6, column=0, padx=20, pady=10)

        self.labelauthTutorSCrearFichaSedacion = ctk.CTkLabel( self.frameFormSCrearFichaSedacion, text="Autorización Tutor", text_font=Font_tuple, text_color="black")
        self.labelauthTutorSCrearFichaSedacion.grid(row=7, column=0, padx=20, pady=10)

        #Agregar Entrys
        self.entradaNombrePacienteSCrearFichaSedacion = ctk.CTkEntry( self.frameFormSCrearFichaSedacion, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaNombrePacienteSCrearFichaSedacion.grid(row=0, column=1, padx=20, pady=10)

        self.entradaEspecieSCrearFichaSedacion = ctk.CTkEntry( self.frameFormSCrearFichaSedacion, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaEspecieSCrearFichaSedacion.grid(row=1, column=1, padx=20, pady=10)

        self.entradaNombreTutorSCrearFichaSedacion = ctk.CTkEntry( self.frameFormSCrearFichaSedacion, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaNombreTutorSCrearFichaSedacion.grid(row=2, column=1, padx=20, pady=10)

        self.entradaRutTutorSCrearFichaSedacion = ctk.CTkEntry( self.frameFormSCrearFichaSedacion, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaRutTutorSCrearFichaSedacion.grid(row=3, column=1, padx=20, pady=10)

        self.entradaRazaSCrearFichaSedacion = ctk.CTkEntry( self.frameFormSCrearFichaSedacion, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaRazaSCrearFichaSedacion.grid(row=4, column=1, padx=20, pady=10)

        self.entradaNumTelefonoSCrearFichaSedacion = ctk.CTkEntry( self.frameFormSCrearFichaSedacion, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaNumTelefonoSCrearFichaSedacion.grid(row=5, column=1, padx=20, pady=10)

        self.entradaDireccionSCrearFichaSedacion = ctk.CTkEntry( self.frameFormSCrearFichaSedacion, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB")
        self.entradaDireccionSCrearFichaSedacion.grid(row=6, column=1, padx=20, pady=10)
        
        self.entradaAuthTutorSCrearFichaSedacion = ctk.CTkCheckBox(self.frameFormSCrearFichaSedacion, text="", fg_color="#0D1D29", border_width=2, border_color="grey")
        self.entradaAuthTutorSCrearFichaSedacion.grid(row=7, column=1, padx=20, pady=10)

        #Agregar buttons
        self.botonVolverSCrearFichaSedacion = ctk.CTkButton(self.frameButtonsSCrearFichaSedacion, width= 200, height= 120,text='Volver', text_font=Font_tuple10, hover_color="#142C3D")
        self.botonVolverSCrearFichaSedacion.pack(padx= 10, pady = 40)
        
        self.botonAgregarFichaSedacion = ctk.CTkButton(self.frameButtonsSCrearFichaSedacion, width= 200, height= 120,text='Agregar Ficha Hospitalización', text_font=Font_tuple10, hover_color="#142C3D")
        self.botonAgregarFichaSedacion.pack(padx= 10, pady = 40)


class screenAbstractMedico(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.configure(background='#5C9C81')
        self.abstractTextSAbstract = tk.Text(self, width = 70, height=25)
        self.abstractTextSAbstract.place(x='320', y='90')
        
        self.botonVolverSAbstract = ctk.CTkButton(self, width= 25, height= 3,text='Volver')
        self.botonVolverSAbstract.place(x='530', y='620')

app = App()
app.mainloop()