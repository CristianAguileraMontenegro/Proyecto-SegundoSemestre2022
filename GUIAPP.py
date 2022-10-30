import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox # pip3 install ttkwidgets
import customtkinter as ctk
from terminalVeterinario import *
import datetime #para sacar la fecha actual
from  tkcalendar import *
from calendario import Calendario
from itertools import cycle
import re
import threading

terminalVet = Terminal()
today = datetime.date.today()
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title('MyPetRecord')
        self.geometry("1366x768")
        self.resizable(False, False)

        ## Creating a container
        container = ctk.CTkFrame(self, corner_radius=0, fg_color="#BCD4E6")
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.mascotaUtilizada:Mascota = None
        self.calendario:Calendario = None
        self.idNuevaMascota = None
        self.flagEditar = False

        self.frames = {}

        self.screenIngresoLlave = screenIngresoLlave
        self.screenPantallaInicial = screenPantallaInicial
        self.screenBuscarMascota = screenBuscarMascota
        self.screenDatosTotalMascota = screenDatosTotalMascota
        self.screenFormularioVerFicha = screenFormularioVerFicha
        self.screenFormularioEditarFicha = screenFormularioEditarFicha
        self.screenFormularioCrearFicha = screenFormularioCrearFicha
        self.screenFormularioAgregarMascota = screenFormularioAgregarMascota
        self.screenFormularioFichaAuthCirugia = screenFormularioFichaAuthCirugia
        self.screenFormularioEditarFichaAuthCirugia = screenFormularioEditarFichaAuthCirugia
        self.screenFormularioCrearFichaAuthCirugia = screenFormularioCrearFichaAuthCirugia
        self.screenFormularioFichaHospt = screenFormularioFichaHospt
        self.screenFormularioEditarFichaHospt = screenFormularioEditarFichaHospt
        self.screenFormularioCrearFichaHospt = screenFormularioCrearFichaHospt
        self.screenFormularioFichaSedacion = screenFormularioFichaSedacion
        self.screenFormularioCrearFichaSedacion = screenFormularioCrearFichaSedacion
        self.screenCalendarioVacunacion = screenCalendarioVacunacion
        self.screenAbstractMedico = screenAbstractMedico

        self.framesTotales = {screenIngresoLlave, screenPantallaInicial, screenBuscarMascota, screenDatosTotalMascota, 
        screenFormularioVerFicha, screenFormularioEditarFicha, screenFormularioCrearFicha, screenFormularioAgregarMascota,
        screenFormularioFichaAuthCirugia, screenFormularioEditarFichaAuthCirugia,screenFormularioCrearFichaAuthCirugia,
        screenFormularioEditarFichaHospt, screenFormularioFichaHospt, screenFormularioCrearFichaHospt, screenFormularioFichaSedacion, 
        screenFormularioCrearFichaSedacion, screenCalendarioVacunacion, screenAbstractMedico}
        
        for F in self.framesTotales:
            frame = F(self, container)
            self.frames[F] = frame
            frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')


        if(terminalVet.validarTokenDeActivacion() == False):
            self.show_frame(screenIngresoLlave)
        else:
            self.show_frame(screenPantallaInicial)

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

    def setIdNuevaMascota(self, idMascota):
        self.idNuevaMascota = idMascota
        
    def getIdNuevaMascota(self):
        return self.idNuevaMascota

    def setFlagEditar(self, flagValue):
        self.flagEditar = flagValue

    def getFlagEditar(self):
        return self.flagEditar

    def filtroNoValidChar(self, texto):
        regex = re.compile("'[@_!#$%^&*()<>?/\|}{~:]")
        if(regex.search(texto) == None):
            return True
        else: 
            return False
        
    def filtroNum(self, texto):
        try:
            textoInt = int(texto)
        except:
            return False
        else:
            return True

    def validarRut(self, rutTutor):

        if(len(rutTutor) >= 7 and len(rutTutor)<=15):
            rut = rutTutor
            rut = rut.upper()
            rut = rut.replace("-","")
            rut = rut.replace(".","")
            for i in rut:
                if(i != "k"):
                    try:
                        letra = int(i)
                    except:
                        return False
            aux = rut[:-1]
            dv = rut[-1:]

            revertido = map(int, reversed(str(aux)))
            factors = cycle(range(2,8))
            s = sum(d * f for d, f in zip(revertido,factors))
            res = (-s)%11

            if str(res) == dv:
                return True
            elif (dv=="K" and res==10):
                return True
            else:
                return False


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
        self.entradaKey = ctk.CTkEntry(self, width = 500, text_font=Font_tuple14, fg_color="#F0EFEB", placeholder_text="Ingrese llave de acceso", placeholder_text_color="grey", justify = "center", text_color='black')
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

class screenPantallaInicial(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 14)
        self.frameBotonesPrincipal = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
        self.frameBotonesPrincipal.pack(padx=30, pady=30)

        self.botonBuscarMascota = ctk.CTkButton(self.frameBotonesPrincipal, width=300, height=120, text="Buscar mascota\n(Ver datos, Crear/Editar Fichas)", text_font=Font_tuple, fg_color="#28587A", hover_color="#142C3D", command= lambda: parent.update_frame(parent.screenBuscarMascota, parent, container))
        self.botonBuscarMascota.pack(padx=20, pady=50)
        self.botonIngresarMascota = ctk.CTkButton(self.frameBotonesPrincipal, width=300, height=120, text="Ingresar mascota al sistema", text_font=Font_tuple, fg_color="#28587A", hover_color="#142C3D", command= lambda: parent.update_frame(parent.screenFormularioAgregarMascota, parent, container))
        self.botonIngresarMascota.pack(padx=20, pady=50)
        self.botonCalendario = ctk.CTkButton(self.frameBotonesPrincipal, width=300, height=120, text="Ver calendario", text_font=Font_tuple, fg_color="#28587A", hover_color="#142C3D", command= lambda: parent.update_frame(parent.screenCalendarioVacunacion, parent, container))
        self.botonCalendario.pack(padx=20, pady=50)
        #futuro boton que liste a las mascotas
        #Boton que permita manejar los insumos


class screenBuscarMascota(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 14)
        self.searchFrame = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
        self.searchFrame.grid(row=0, column=0, padx=20 , pady=20)

        self.frameMensajes = ctk.CTkFrame(self.searchFrame, corner_radius=10, fg_color="#C5DEDD")

        self.entradaBuscar = ctk.CTkEntry(self.searchFrame, width = 600, text_font=Font_tuple, border_width=0, placeholder_text="Ingrese Codigo Mascota", placeholder_text_color="grey", text_color="black", fg_color="#F0EFEB")
        self.entradaBuscar.grid(row=0, column=0, padx=10, pady=10)

        self.botonBuscar = ctk.CTkButton(self.searchFrame, width= 10, text="Buscar", text_font=Font_tuple, command= lambda: self.clickBuscar(parent, container), fg_color="#28587A")
        self.botonBuscar.grid(row=0, column=1, padx=10, pady=10)

        self.labelCodigoInvalido = ctk.CTkLabel(self.frameMensajes, text="Ingrese un código válido", text_font=Font_tuple, text_color='red')
        self.labelNoExiste =  ctk.CTkLabel(self.frameMensajes, justify='left', text= "Mascota no registrada en el sistema", text_font=Font_tuple, text_color='black', width=100)

        self.botonEntrar = ctk.CTkButton(self.searchFrame, width=8, text='Ver Datos Mascota', text_font=Font_tuple, fg_color="#28587A", command=lambda: parent.update_frame(parent.screenDatosTotalMascota, parent, container))
        self.botonEntrarAbstract = ctk.CTkButton(self.searchFrame, width=8, text='Ver Abstract', text_font=Font_tuple, fg_color="#28587A", command=lambda: parent.update_frame(parent.screenAbstractMedico, parent, container))
        self.botonCrearMascota = ctk.CTkButton(self.searchFrame, width=8, text='Registrar Mascota', text_font=Font_tuple, fg_color="#28587A", command=lambda: parent.update_frame(parent.screenFormularioAgregarMascota, parent, container))
        
        self.botonVolver = ctk.CTkButton(self, width=20, text="Volver a pantalla principal", text_font=Font_tuple, fg_color="#28587A", hover_color="#142C3D", command= lambda: parent.update_frame(parent.screenPantallaInicial, parent, container))
        self.botonVolver.grid(row=0, column=1, padx=20, pady=20)

        self.labelInfoBasica = ctk.CTkLabel(self.frameMensajes, justify='left', text_font=Font_tuple, text_color='black', width=100)
    
    def validarDatos(self, parent, container):
        flag = False
        codigoMascota = self.entradaBuscar.get()
        if(parent.filtroNum(codigoMascota) is not True) or (parent.filtroNoValidChar(codigoMascota) is not True) or (len(codigoMascota) == 0):
            flag = False
            self.labelCodigoInvalido.grid(row=0, column=0,padx=10, pady=10)

        if(flag):
            self.clickBuscar(parent, container)


    def clickBuscar(self, parent, container):
        codigoMascota = self.entradaBuscar.get()
        resultado = terminalVet.verificarMascotaEnSistema(codigoMascota)
        Font_tuple = ("Helvetica", 14)
        self.frameMensajes.grid(row=1, column=0, padx=10, pady=10)
        if(resultado[0] == "MalCodigo"):
            self.labelCodigoInvalido.grid(row=0, column=0,padx=10, pady=10)
        elif(resultado[0]=="MascotaLocal"):

            idMascota = resultado[1]
            #datosMascota = terminalVet.getDatosBasicosMascota(idMascota)

            mascotaLol = terminalVet.getMascota(idMascota)
            terminalVet.buscarMascotaLocal2(idMascota)

            parent.setMascotaApp(mascotaLol)
            
            mascotaMostrar:Mascota = parent.getMascotaApp()
            self.labelCodigoInvalido.grid_forget()
            self.botonEntrarAbstract.grid_forget()
            self.labelInfoBasica.grid_forget()
            self.labelNoExiste.grid_forget()
            self.botonCrearMascota.grid_forget()
            infoBasica = f'Codigo mascota:  {str(mascotaMostrar.getId())} , Nombre mascota:  {str(mascotaMostrar.getNombreMascota())} , Especie:   {str(mascotaMostrar.getEspecie())} \nRaza:   {str(mascotaMostrar.getRaza())}  , Dueño/a:   {str(mascotaMostrar.getNombreTutor())}'
            self.labelInfoBasica = ctk.CTkLabel(self.frameMensajes, justify='left', text=infoBasica, text_font=Font_tuple, text_color='black', width=100)
            self.labelInfoBasica.grid(row=1, column=0, padx=10, pady=30)
         
            self.botonEntrar.grid(row=1, column=1, padx=10, pady=10) 
        elif(resultado[0]=='MascotaRemota'):

            idMascota = resultado[1]
            datosMascota = terminalVet.getDatosBasicosMascota(idMascota)

            mascotaLol = terminalVet.agregarMascotaRemota(idMascota)

            terminalVet.buscarMascotaRemota2(idMascota)

            parent.setMascotaApp(mascotaLol)
            
            mascotaMostrar:Mascota = parent.getMascotaApp()
            self.labelCodigoInvalido.grid_forget()
            self.botonEntrar.grid_forget()
            self.labelInfoBasica.grid_forget()
            self.labelNoExiste.grid_forget()
            self.botonCrearMascota.grid_forget()

            infoBasica = f'Codigo mascota:  {str(mascotaMostrar.getId())} , Nombre mascota:  {str(mascotaMostrar.getNombreMascota())} , Especie:   {str(mascotaMostrar.getEspecie())} \nRaza:   {str(mascotaMostrar.getRaza())}  , Dueño/a:   {str(mascotaMostrar.getNombreTutor())}'
            self.labelInfoBasica = ctk.CTkLabel(self.frameMensajes, justify='left', text=infoBasica, text_font=Font_tuple, text_color='black', width=100)
            self.labelInfoBasica.grid(row=1, column=0, padx=10, pady=30)
            
            self.botonEntrarAbstract.grid(row=1, column=1, padx=10, pady=10)

        elif(resultado[0]=='MascotaNoExiste'):

            #'Mascota no registrada en el sistema'
            parent.setIdNuevaMascota(codigoMascota)
            self.labelCodigoInvalido.grid_forget()
            self.labelInfoBasica.grid_forget()
            self.botonEntrar.grid_forget()
            self.botonEntrarAbstract.grid_forget()
            
            self.labelNoExiste.grid(row=1, column=0, padx=10, pady=30)
            
            self.botonCrearMascota = ctk.CTkButton(self.searchFrame, width=8, text='Registrar Mascota', text_font=Font_tuple, fg_color="#28587A", command=lambda: parent.update_frame(parent.screenFormularioAgregarMascota, parent, container))
            self.botonCrearMascota.grid(row=1, column=1, padx=10, pady=10)


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
            fechaNacimiento = str(mascotaActual.getFechaDeNacimiento())


            listaDatosBasicos = [f'Nombre : {nombreMascota}', f'Especie: {especieMascota}', f'Raza: {razaMascota}', f'Color: {colorMascota}', f'RUT: {rutTutor}',
                                 f'Teléfono: {numTelefono}', f'Dirección :{direccion}', f'Fecha Nacimiento: {fechaNacimiento}']
            listaString = tk.StringVar(value=listaDatosBasicos)

            self.listDatosBasicos = tk.Listbox(
                self.frameListaboxDatos,
                listvariable=listaString,
                width=40,
                height=8,
                selectmode='browse',
                borderwidth=0,
                background="#EAF2F8",
                font=('Helvetica', '13'))
            self.listDatosBasicos.grid(row=0, column=0, padx=10, pady=8)

            i = 0
            alergiasTabla = mascotaActual.getAlergias()
            alergias = ''
            
            while(i <= (len(alergiasTabla)-1)):
                alergias = alergias + str(alergiasTabla[i]['nombre'])
                i += 1
            alergiasString = f'Alergias: {alergias}'
            alergiasMostrar = tk.StringVar(value=alergiasString)
            
            self.listaAlergias = tk.Listbox(
                self.frameListaboxDatos,
                listvariable=alergiasMostrar,
                width=40,
                height=7,
                selectmode='browse',
                borderwidth=0,
                background="#EAF2F8",
                font=('Helvetica', '13'))
            self.listaAlergias.grid(row = 1, column=0, padx=10, pady=10)

            operacionesTabla = mascotaActual.getRegistroDeOperaciones()
            operaciones = ''
            i = 0
            while(i <= (len(operacionesTabla)-1)):
                operaciones = operaciones + str(operacionesTabla[i]['operacion']) + '\n'#falta generar las operaciones
                i += 1
            operacionesString = f'Operaciones: {operaciones}'
            
            operacionesMostrar = tk.StringVar(value=operacionesString)
            self.listaOperaciones = tk.Listbox(
                self.frameListaboxDatos,
                listvariable=operacionesMostrar,
                width=40,
                height=7,
                selectmode='browse',
                borderwidth=0,
                background="#EAF2F8",
                font=('Helvetica', '13'))
            self.listaOperaciones.grid(row = 2, column=0, padx=10, pady=10)

            vacunasTabla = mascotaActual.getVacunasSuministradas()
            vacunas = ''
            i = 0
            while(i <= (len(vacunasTabla)-1)):
                vacunas = vacunas + str(vacunasTabla[i]['nomVacuna']) + '\n'
                i += 1
            vacunasString = f'Vacunas: {vacunas}'
            vacunasMostrar = tk.StringVar(value=vacunasString)

            self.listaVacunas = tk.Listbox(
                self.frameListaboxDatos,
                listvariable=vacunasMostrar,
                width=40,
                height=7,
                selectmode='browse',
                borderwidth=0,
                background="#EAF2F8",
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
            listaFechas.sort(reverse=True)
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
                borderwidth=0,
                background="#EAF2F8",
                font=('Helvetica', '13'))
            self.listFichasMedicas.grid(row = 0, column=0, padx=10, pady=10)

            self.buttonVerFicha = ctk.CTkButton(self.frameBotones, width= 175, height= 100,text='Ver Ficha', hover_color="#142C3D", text_font=Font_tuple,command=lambda: self.verSeleccionado(self.listFichasMedicas, parent, container, mascotaActual))
            self.buttonVerFicha.pack(padx=10, pady=20)

            self.buttonEditarFicha = ctk.CTkButton(self.frameBotones, width= 175, height= 100,text='Editar Ficha', hover_color="#142C3D", text_font=Font_tuple,command=lambda: self.verSeleccionadoEditar(self.listFichasMedicas, parent, container, mascotaActual))
            self.buttonEditarFicha.pack(padx=10, pady=20)

            self.buttonCrearFicha = ctk.CTkButton(self.frameBotones, width= 175, height= 100,text='Crear Ficha', hover_color="#142C3D", text_font=Font_tuple, command=lambda: parent.update_frame(parent.screenFormularioCrearFicha, parent, container))
            self.buttonCrearFicha.pack(padx=10, pady=20)

            self.botonVolverSDatosTotal = ctk.CTkButton(self.frameBotones, width= 175, height= 100,text='Volver', text_font=Font_tuple, command=lambda: parent.update_frame(parent.screenBuscarMascota, parent, container), hover_color="#142C3D")
            self.botonVolverSDatosTotal.pack(padx=10, pady=20)

            self.labelErrorFicha = ctk.CTkLabel(self, text="Seleccione una ficha")

    def verSeleccionado(self, lista, parent, container, mascotaActual):
        item = lista.curselection()
        auxTexto = lista.get(item)
        textoSplit = auxTexto.split('Ficha del : ')
        fechaSolo = textoSplit[1]
        
        mascotaActual.setActualFichaMedicaConsulta(fechaSolo, True)
        parent.update_frame(parent.screenFormularioVerFicha, parent, container)
    
    def verSeleccionadoEditar(self, lista, parent, container, mascotaActual):
        item = lista.curselection()
        auxTexto = lista.get(item)
        textoSplit = auxTexto.split('Ficha del : ')
        fechaSolo = textoSplit[1]
        
        mascotaActual.setActualFichaMedicaConsulta(fechaSolo, True)
        parent.update_frame(parent.screenFormularioEditarFicha, parent, container)
        
        
class screenFormularioVerFicha(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ('Helvetica', 12)
        Font_tuple16 = ('Helvetica', 18)
        #Agregar Labels--------------------------------------------------------------------------------------------------------------------------------
        mascotaActual:Mascota = parent.getMascotaApp()
        if(mascotaActual != None):
            
            idFicha = mascotaActual.getidFichaActual()
            terminalVet.completarFichaParcial(mascotaActual.getId(), idFicha)
            textoMascota = mascotaActual.getNombreMascota()
            self.labelTituloScreenSVerFicha = ctk.CTkLabel(self, text=f"Visualización de ficha, Mascota : {textoMascota}", text_font=Font_tuple16, text_color="black")
            self.labelTituloScreenSVerFicha.grid(row=0, column=0, padx=10, pady=10)

            self.frameForm = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameForm.grid(row=1, column=0, padx=20, pady=20)

            self.frameButtons = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameButtons.grid(row=2, column=0, padx=20, pady=20)

            self.labelSucursalSVerFicha = ctk.CTkLabel(self.frameForm, text="Sucursal Veterinaria", text_font=Font_tuple, text_color='black')
            self.labelSucursalSVerFicha.grid(row = 0, column = 0, padx=(20,5), pady=15)
            
            self.labelVetACargoSVerFicha = ctk.CTkLabel(self.frameForm, text="Veterinario a cargo", text_font=Font_tuple, text_color='black')
            self.labelVetACargoSVerFicha.grid(row = 1, column = 0, padx=(20,5), pady=15)
            
            self.labelFechaConsultaSVerFicha = ctk.CTkLabel(self.frameForm, text="Fecha Consulta", text_font=Font_tuple, text_color='black')
            self.labelFechaConsultaSVerFicha.grid(row = 2, column = 0, padx=(20,5), pady=15)
            
            self.labelTratamientosConsultaSVerFicha = ctk.CTkLabel(self.frameForm, text="Tratamientos Consulta", text_font=Font_tuple, text_color='black')
            self.labelTratamientosConsultaSVerFicha.grid(row = 3, column = 0, padx=(20,5), pady=15)
            
            self.labelMedicamentosConsultaSVerFicha = ctk.CTkLabel(self.frameForm, text="Medicamentos Consulta", text_font=Font_tuple, text_color='black')
            self.labelMedicamentosConsultaSVerFicha.grid(row = 4, column = 0, padx=(20,5), pady=15)
            
            self.labelCausaVisitaSVerFicha = ctk.CTkLabel(self.frameForm, text="Causa Visita", text_font=Font_tuple, text_color='black')
            self.labelCausaVisitaSVerFicha.grid(row = 5, column = 0, padx=(20,5), pady=15)
            
            self.labelVacSuministradasSVerFicha = ctk.CTkLabel(self.frameForm, text="Vacunas Suministradas", text_font=Font_tuple, text_color='black')
            self.labelVacSuministradasSVerFicha.grid(row = 0, column = 2, padx=(20,5), pady=15)
            
            self.labelFrecRespiratoriaSVerFicha = ctk.CTkLabel(self.frameForm, text="Frecuencia Respiratoria", text_font=Font_tuple, text_color='black')
            self.labelFrecRespiratoriaSVerFicha.grid(row = 1, column = 2, padx=(20,5), pady=15)
            
            self.labelFrecCardiacaSVerFicha = ctk.CTkLabel(self.frameForm, text="Frecuencia Cardiaca", text_font=Font_tuple, text_color='black')
            self.labelFrecCardiacaSVerFicha.grid(row = 2, column = 2, padx=(20,5), pady=15)

            self.labelPesoSVerFicha = ctk.CTkLabel(self.frameForm, text="Peso", text_font=Font_tuple, text_color='black')
            self.labelPesoSVerFicha.grid(row = 3, column = 2, padx=(20,5), pady=15)
            
            self.labelEdadSVerFicha = ctk.CTkLabel(self.frameForm, text="Edad", text_font=Font_tuple, text_color='black')
            self.labelEdadSVerFicha.grid(row = 4, column = 2, padx=(20,5), pady=15)

            self.labelTemperaturaSVerFicha = ctk.CTkLabel(self.frameForm, text="Temperatura", text_font=Font_tuple, text_color='black')
            self.labelTemperaturaSVerFicha.grid(row = 5, column = 2, padx=(20,5), pady=15)

            
            #Agregar Entrys------------------------------------------------------------------------------------------------------------------------------
            self.textVarSucursal = tk.StringVar()
            self.textVarVetACargo = tk.StringVar()
            self.textVarFecha = tk.StringVar()
            self.textVarFechaMod = tk.StringVar()
            self.textVarTratamiento = tk.StringVar()
            self.textVarMedicamento = tk.StringVar()
            self.textVarCausa = tk.StringVar()
            self.textVarVacunas = tk.StringVar()
            self.textVarFrecResp = tk.StringVar()
            self.textVarFrecCardio = tk.StringVar()
            self.textVarPeso = tk.StringVar()
            self.textVarEdad = tk.StringVar()
            self.textVarTemp = tk.StringVar()

            self.textVarSucursal.set(str(mascotaActual.getSucursalVeterinaria(idFicha)))
            self.entradaSucursalSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey', textvariable=self.textVarSucursal, state=DISABLED)
            self.entradaSucursalSVerFicha.grid(row = 0, column = 1, padx=20, pady=15)

            self.textVarVetACargo.set(str(mascotaActual.getVeterinarioACargo(idFicha)))
            self.entradaVetACargoSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey', textvariable=self.textVarVetACargo, state=DISABLED)
            self.entradaVetACargoSVerFicha.grid(row = 1, column = 1, padx=20, pady=15)
            
            self.textVarFecha.set(str(mascotaActual.getFechaConsulta(idFicha)))
            self.entradaFechaConsultaSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey', textvariable=self.textVarFecha, state=DISABLED)
            self.entradaFechaConsultaSVerFicha.grid(row = 2, column = 1, padx=20, pady=15)


            tratamientos = mascotaActual.getTratamiento(idFicha)
            tratamientosString = ''
            
            for i in range(len(tratamientos)):
                if(i == len(tratamientos)-1):
                    tratamientosString = tratamientosString + tratamientos[i]['nombreTratamiento'] + '.'
                else:
                    tratamientosString = tratamientosString + tratamientos[i]['nombreTratamiento'] + ','
            self.textVarTratamiento.set(str(tratamientosString))
            self.entradaTratamientosConsultaSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey', textvariable=self.textVarTratamiento, state=DISABLED)
            self.entradaTratamientosConsultaSVerFicha.grid(row = 3, column = 1, padx=20, pady=15)
            
            medicamentos = mascotaActual.getMedicamentosConsulta(idFicha)
            medicamentosString = ''
            
            for i in range(len(medicamentos)):
                if(i == len(medicamentos)-1):
                    medicamentosString = medicamentosString + medicamentos[i]['nomMedicamento'] + '.'
                else:
                    medicamentosString = medicamentosString + medicamentos[i]['nomMedicamento'] + ','
            self.textVarMedicamento.set(str(medicamentosString))
            self.entradaMedicamentosConsultaSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey', textvariable=self.textVarMedicamento, state=DISABLED)
            self.entradaMedicamentosConsultaSVerFicha.grid(row = 4, column = 1, padx=20, pady=15)

            #Trat
            causaVisita = mascotaActual.getTratamiento(idFicha)
            causaVisitaString = ''
            
            for i in range(len(tratamientos)):
                if(i == len(causaVisita)-1):
                    causaVisitaString = causaVisitaString + causaVisita[i]['causaVisita'] + '.'
                else:
                    causaVisitaString = causaVisitaString + causaVisita[i]['causaVisita'] + ','
            self.textVarCausa.set(str(causaVisitaString))
            self.entradaCausaVisitaSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey', textvariable=self.textVarCausa, state=DISABLED)
            self.entradaCausaVisitaSVerFicha.grid(row = 5, column = 1, padx=20, pady=15)

            vacunas = mascotaActual.getVacunasSuministradasConsulta(idFicha)
            vacunasString = ''
            
            for i in range(len(vacunas)):
                if(i == len(vacunas)-1):
                    vacunasString = vacunasString + vacunas[i]['nomVacuna'] + '.'
                else:
                    vacunasString = vacunasString + vacunas[i]['nomVacuna'] + ','

            self.textVarVacunas.set(str(vacunasString))
            self.entradaVacSuministradasSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey', textvariable=self.textVarVacunas, state=DISABLED)
            self.entradaVacSuministradasSVerFicha.grid(row = 0, column = 3, padx=20, pady=15)

            self.textVarFrecResp.set(str(mascotaActual.getFrecRespiratoria(idFicha)))
            self.entradaFrecRespiratoriaSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey', textvariable=self.textVarFrecResp, state=DISABLED)
            self.entradaFrecRespiratoriaSVerFicha.grid(row = 1, column = 3, padx=20, pady=15)

            self.textVarFrecCardio.set(str(mascotaActual.getFrecCardiaca(idFicha)))
            self.entradaFrecCardiacaSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey', textvariable=self.textVarFrecCardio, state=DISABLED)
            self.entradaFrecCardiacaSVerFicha.grid(row = 2, column = 3, padx=20, pady=15)

            self.textVarPeso.set(str(mascotaActual.getPeso(idFicha)))
            self.entradaPesoSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey', textvariable=self.textVarPeso, state=DISABLED)
            self.entradaPesoSVerFicha.grid(row = 3, column = 3, padx=20, pady=15)

            self.textVarEdad.set(str(mascotaActual.getEdad(idFicha)))
            self.entradaEdadSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey', textvariable=self.textVarEdad, state=DISABLED)
            self.entradaEdadSVerFicha.grid(row = 4, column = 3, padx=20, pady=15)

            self.textVarTemp.set(str(mascotaActual.getTemp(idFicha)))
            self.entradaTemperaturaSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey', textvariable=self.textVarTemp, state=DISABLED)
            self.entradaTemperaturaSVerFicha.grid(row = 5, column = 3, padx=20, pady=15)

            if(mascotaActual.getFechaModificacion(idFicha) is not None):
                self.textVarFechaMod.set(str(mascotaActual.getFechaModificacion(idFicha)))
                self.labelFechaModificacion = ctk.CTkLabel(self.frameForm, text="Fecha Ultima Modificación", text_font=Font_tuple, text_color='black')
                self.labelFechaModificacion.grid(row = 6, column = 0, padx=(20,5), pady=15)
                self.entradaFechaUltimaModSVerFicha = ctk.CTkEntry(self.frameForm, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey', textvariable=self.textVarFechaMod, state=DISABLED)
                self.entradaFechaUltimaModSVerFicha.grid(row = 6, column = 1, padx=20, pady=15)

            #Agregar Buttons
            self.botonVolverSVerFicha = ctk.CTkButton(self.frameButtons, width= 200, height= 80, text='Volver', text_font=Font_tuple, hover_color="#142C3D", command=lambda: self.volverSDTotalMascota(parent, container, mascotaActual, idFicha))
            self.botonVolverSVerFicha.grid(row=0, column=4, padx=15, pady=15)

            if (mascotaActual.getHospitalizacion(idFicha) == True):
                self.botonVerFichaHosp = ctk.CTkButton(self.frameButtons, width= 200, height= 80, text='Ver Ficha Hospitalizacion', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenFormularioFichaHospt, parent, container))
                self.botonVerFichaHosp.grid(row=0, column=1, padx=5, pady=15)
            
            if(mascotaActual.getSedacion(idFicha) == True):
                self.botonVerFichaSedacion = ctk.CTkButton(self.frameButtons, width= 200, height= 80, text='Ver Ficha Sedación', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenFormularioFichaSedacion, parent, container))
                self.botonVerFichaSedacion.grid(row=0, column=2, padx=5, pady=15)

            if(mascotaActual.getOperacion(idFicha) == True):
                self.botonVerFichaOperacion = ctk.CTkButton(self.frameButtons, width= 200, height= 80, text='Ver Ficha Operación', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenFormularioFichaAuthCirugia, parent, container))
                self.botonVerFichaOperacion.grid(row=0, column=3, padx=5, pady=15)

    def volverSDTotalMascota(self, parent, container, mascotaActual, idFicha):
        mascotaActual.quitarActualFichaMedicaConsulta(idFicha)
        parent.update_frame(parent.screenDatosTotalMascota, parent, container)


class screenFormularioEditarFicha(ctk.CTkFrame):

    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ('Helvetica', 12)
        Font_tuple16 = ('Helvetica', 16)

        #Agregar Labels--------------------------------------------------------------------------------------------------------------------------------
        mascotaActual:Mascota = parent.getMascotaApp()
        if(mascotaActual != None):
            
            idFicha = mascotaActual.getidFichaActual()
            terminalVet.completarFichaParcial(mascotaActual.getId(), idFicha)

            textoMascota = mascotaActual.getNombreMascota()
            self.labelTituloScreenSEditarFicha = ctk.CTkLabel(self, text=f"Edición de ficha, Mascota : {textoMascota}", text_font=Font_tuple16, text_color="black")
            self.labelTituloScreenSEditarFicha.grid(row=0, column=0, padx=10, pady=10)

            self.frameFormSEditarFicha = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameFormSEditarFicha.grid(row=1, column=0, padx=20, pady=20)

            self.frameButtonsSEditarFicha = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameButtonsSEditarFicha.grid(row=2, column=0, padx=20, pady=20)

            self.labelSucursalSEditarFicha = ctk.CTkLabel(self.frameFormSEditarFicha, text="Sucursal Veterinaria", text_font=Font_tuple, text_color='black')
            self.labelSucursalSEditarFicha.grid(row = 0, column = 0, padx=(20,5), pady=15)
            
            self.labelVetACargoSEditarFicha = ctk.CTkLabel(self.frameFormSEditarFicha, text="Veterinario a cargo", text_font=Font_tuple, text_color='black')
            self.labelVetACargoSEditarFicha.grid(row = 1, column = 0, padx=(20,5), pady=15)
            
            self.labelFechaConsultaSEditarFicha = ctk.CTkLabel(self.frameFormSEditarFicha, text="Fecha Modificación", text_font=Font_tuple, text_color='black')
            self.labelFechaConsultaSEditarFicha.grid(row = 2, column = 0, padx=(20,5), pady=15)
            
            self.labelTratamientosConsultaSEditarFicha = ctk.CTkLabel(self.frameFormSEditarFicha, text="Tratamientos Consulta", text_font=Font_tuple, text_color='black')
            self.labelTratamientosConsultaSEditarFicha.grid(row = 3, column = 0, padx=(20,5), pady=15)
            
            self.labelMedicamentosConsultaSEditarFicha = ctk.CTkLabel(self.frameFormSEditarFicha, text="Medicamentos Consulta", text_font=Font_tuple, text_color='black')
            self.labelMedicamentosConsultaSEditarFicha.grid(row = 4, column = 0, padx=(20,5), pady=15)
            
            self.labelCausaVisitaSEditarFicha = ctk.CTkLabel(self.frameFormSEditarFicha, text="Causa Visita", text_font=Font_tuple, text_color='black')
            self.labelCausaVisitaSEditarFicha.grid(row = 5, column = 0, padx=(20,5), pady=15)
            
            self.labelVacSuministradasSEditarFicha = ctk.CTkLabel(self.frameFormSEditarFicha, text="Vacunas Suministradas", text_font=Font_tuple, text_color='black')
            self.labelVacSuministradasSEditarFicha.grid(row = 0, column = 2, padx=(20,5), pady=15)
            
            self.labelFrecRespiratoriaSEditarFicha = ctk.CTkLabel(self.frameFormSEditarFicha, text="Frecuencia Respiratoria", text_font=Font_tuple, text_color='black')
            self.labelFrecRespiratoriaSEditarFicha.grid(row = 1, column = 2, padx=(20,5), pady=15)
            
            self.labelFrecCardiacaSEditarFicha = ctk.CTkLabel(self.frameFormSEditarFicha, text="Frecuencia Cardiaca", text_font=Font_tuple, text_color='black')
            self.labelFrecCardiacaSEditarFicha.grid(row = 2, column = 2, padx=(20,5), pady=15)

            self.labelPesoSEditarFicha = ctk.CTkLabel(self.frameFormSEditarFicha, text="Peso", text_font=Font_tuple, text_color='black')
            self.labelPesoSEditarFicha.grid(row = 3, column = 2, padx=(20,5), pady=15)
            
            self.labelEdadSEditarFicha = ctk.CTkLabel(self.frameFormSEditarFicha, text="Edad", text_font=Font_tuple, text_color='black')
            self.labelEdadSEditarFicha.grid(row = 4, column = 2, padx=(20,5), pady=15)

            self.labelTemperaturaSEditarFicha = ctk.CTkLabel(self.frameFormSEditarFicha, text="Temperatura", text_font=Font_tuple, text_color='black')
            self.labelTemperaturaSEditarFicha.grid(row = 5, column = 2, padx=(20,5), pady=15)

            self.labelMensajeEditadoGeneral = ctk.CTkLabel(self.frameButtonsSEditarFicha, text="Ficha Editada", text_font=Font_tuple, text_color='green')
            
            #Agregar Entrys------------------------------------------------------------------------------------------------------------------------------
            self.textVarSucursal = tk.StringVar()
            self.textVarVetACargo = tk.StringVar()
            self.textVarFecha = tk.StringVar()
            self.textVarTratamiento = tk.StringVar()
            self.textVarMedicamento = tk.StringVar()
            self.textVarCausa = tk.StringVar()
            self.textVarVacunas = tk.StringVar()
            self.textVarFrecResp = tk.StringVar()
            self.textVarFrecCardio = tk.StringVar()
            self.textVarPeso = tk.StringVar()
            self.textVarEdad = tk.StringVar()
            self.textVarTemp = tk.StringVar()

            self.textVarSucursal.set(str(mascotaActual.getSucursalVeterinaria(idFicha)))
            self.entradaSucursalSEditarFicha = ctk.CTkEntry(self.frameFormSEditarFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=self.textVarSucursal)
            self.entradaSucursalSEditarFicha.grid(row = 0, column = 1, padx=20, pady=15)

            self.textVarVetACargo.set(str(mascotaActual.getVeterinarioACargo(idFicha)))
            self.entradaVetACargoSEditarFicha = ctk.CTkEntry(self.frameFormSEditarFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=self.textVarVetACargo)
            self.entradaVetACargoSEditarFicha.grid(row = 1, column = 1, padx=20, pady=15)
            
            textFechaActual = tk.StringVar()
            hoy = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            textFechaActual.set(str(hoy))
            self.textVarFecha.set(str(mascotaActual.getFechaConsulta(idFicha)))
            self.entradaFechaConsultaSEditarFicha = ctk.CTkEntry(self.frameFormSEditarFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey', textvariable=textFechaActual, state = DISABLED)
            self.entradaFechaConsultaSEditarFicha.grid(row = 2, column = 1, padx=20, pady=15)


            tratamientos = mascotaActual.getTratamiento(idFicha)
            tratamientosString = ''
            
            for i in range(len(tratamientos)):
                if(i == len(tratamientos)-1):
                    tratamientosString = tratamientosString + tratamientos[i]['nombreTratamiento'] + '.'
                else:
                    tratamientosString = tratamientosString + tratamientos[i]['nombreTratamiento'] + ','
            self.textVarTratamiento.set(str(tratamientosString))
            self.entradaTratamientosConsultaSEditarFicha = ctk.CTkEntry(self.frameFormSEditarFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=self.textVarTratamiento)
            self.entradaTratamientosConsultaSEditarFicha.grid(row = 3, column = 1, padx=20, pady=15)
            
            medicamentos = mascotaActual.getMedicamentosConsulta(idFicha)
            medicamentosString = ''
            
            for i in range(len(medicamentos)):
                if(i == len(medicamentos)-1):
                    medicamentosString = medicamentosString + medicamentos[i]['nomMedicamento'] + '.'
                else:
                    medicamentosString = medicamentosString + medicamentos[i]['nomMedicamento'] + ','
            self.textVarMedicamento.set(str(medicamentosString))
            self.entradaMedicamentosConsultaSEdiEditarFicha = ctk.CTkEntry(self.frameFormSEditarFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', placeholder_text="Medicamento1; Medicamento2...", textvariable=self.textVarMedicamento)
            self.entradaMedicamentosConsultaSEdiEditarFicha.grid(row = 4, column = 1, padx=20, pady=15)

            #Trat
            causaVisita = mascotaActual.getTratamiento(idFicha)
            causaVisitaString = ''
            
            for i in range(len(tratamientos)):
                if(i == len(causaVisita)-1):
                    causaVisitaString = causaVisitaString + causaVisita[i]['causaVisita'] + '.'
                else:
                    causaVisitaString = causaVisitaString + causaVisita[i]['causaVisita'] + ','
            self.textVarCausa.set(str(causaVisitaString))
            self.entradaCausaVisitaSEditarFicha = ctk.CTkEntry(self.frameFormSEditarFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', textvariable=self.textVarCausa)
            self.entradaCausaVisitaSEditarFicha.grid(row = 5, column = 1, padx=20, pady=15)

            vacunas = mascotaActual.getVacunasSuministradasConsulta(idFicha)
            vacunasString = ''
            
            for i in range(len(vacunas)):
                if(i == len(vacunas)-1):
                    vacunasString = vacunasString + vacunas[i]['nomVacuna'] + '.'
                else:
                    vacunasString = vacunasString + vacunas[i]['nomVacuna'] + ','

            self.textVarVacunas.set(str(vacunasString))
            self.entradaVacSuministradasSEditarFicha = ctk.CTkEntry(self.frameFormSEditarFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', placeholder_text="Vacuna1; Vacuna2...", textvariable=self.textVarVacunas)
            self.entradaVacSuministradasSEditarFicha.grid(row = 0, column = 3, padx=20, pady=15)

            self.textVarFrecResp.set(str(mascotaActual.getFrecRespiratoria(idFicha)))
            self.entradaFrecRespiratoriaSEditarFicha = ctk.CTkEntry(self.frameFormSEditarFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', placeholder_text="En RPM", textvariable=self.textVarFrecResp)
            self.entradaFrecRespiratoriaSEditarFicha.grid(row = 1, column = 3, padx=20, pady=15)

            self.textVarFrecCardio.set(str(mascotaActual.getFrecCardiaca(idFicha)))
            self.entradaFrecCardiacaSEditarFicha = ctk.CTkEntry(self.frameFormSEditarFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', placeholder_text="En BPM", textvariable=self.textVarFrecCardio)
            self.entradaFrecCardiacaSEditarFicha.grid(row = 2, column = 3, padx=20, pady=15)

            self.textVarPeso.set(str(mascotaActual.getPeso(idFicha)))
            self.entradaPesoSEditarFicha = ctk.CTkEntry(self.frameFormSEditarFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', placeholder_text="En kg", textvariable=self.textVarPeso)
            self.entradaPesoSEditarFicha.grid(row = 3, column = 3, padx=20, pady=15)

            self.textVarEdad.set(str(mascotaActual.getEdad(idFicha)))
            self.entradaEdadSEditarFicha = ctk.CTkEntry(self.frameFormSEditarFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', placeholder_text="Ej: 2 años", textvariable=self.textVarEdad)
            self.entradaEdadSEditarFicha.grid(row = 4, column = 3, padx=20, pady=15)

            self.textVarTemp.set(str(mascotaActual.getTemp(idFicha)))
            self.entradaTemperaturaSEditarFicha = ctk.CTkEntry(self.frameFormSEditarFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', placeholder_text="Ej: 32.3", textvariable=self.textVarTemp)
            self.entradaTemperaturaSEditarFicha.grid(row = 5, column = 3, padx=20, pady=15)

            #Agregar Buttons
            self.botonEditarFichaGeneralSCrearFicha = ctk.CTkButton(self.frameButtonsSEditarFicha, width=250, height=80, text='Editar Ficha Actual', text_font=Font_tuple, hover_color="#142C3D", command=lambda: self.clickEditarFicha(idFicha, self.entradaSucursalSEditarFicha.get(), 
            self.entradaVetACargoSEditarFicha.get(), self.entradaFechaConsultaSEditarFicha.get(), mascotaActual.getOperacion(idFicha), self.entradaFrecRespiratoriaSEditarFicha.get(),
            self.entradaFrecCardiacaSEditarFicha.get(), self.entradaPesoSEditarFicha.get(), self.entradaEdadSEditarFicha.get(), mascotaActual.getHospitalizacion(idFicha), mascotaActual.getSedacion(idFicha),  self.entradaTemperaturaSEditarFicha.get(), mascotaActual.getId(),
            self.entradaTratamientosConsultaSEditarFicha.get(), self.entradaCausaVisitaSEditarFicha.get() ,self.entradaMedicamentosConsultaSEdiEditarFicha.get(), self.entradaVacSuministradasSEditarFicha.get(), terminalVet, mascotaActual))
            
            self.botonEditarFichaGeneralSCrearFicha.grid(row=0, column=0, padx=15, pady=15)

            flagHosp = False
            flagOperacion = False

            if (mascotaActual.getHospitalizacion(idFicha) == True):
                flagHosp = True
                self.botonEditarFichaHosp = ctk.CTkButton(self.frameButtonsSEditarFicha, width= 250, height= 80, text='Editar Ficha Hospitalizacion', text_font=Font_tuple, hover_color="#142C3D", command=lambda: self.clickEditarHosp(parent, container, flagHosp)) #hay que agregar cauda de la visita a la base de datos
                self.botonEditarFichaHosp.grid(row=0, column=1, padx=5, pady=15)
            else:
                self.botonAgregarFichaHosp = ctk.CTkButton(self.frameButtonsSEditarFicha, width= 250, height= 80, text='Agregar Ficha Hospitalizacion', text_font=Font_tuple, hover_color="#142C3D", command=lambda: self.clickEditarHosp(parent, container, flagHosp)) #hay que agregar cauda de la visita a la base de datos
                self.botonAgregarFichaHosp.grid(row=0, column=1, padx=5, pady=15)

            if(mascotaActual.getSedacion(idFicha) == False):
                self.botonAgregarFichaSedacion = ctk.CTkButton(self.frameButtonsSEditarFicha, width= 250, height= 80, text='Agregar Ficha Sedación', text_font=Font_tuple, hover_color="#142C3D", command=lambda: self.clickAgregarSedacion(parent, container))
                self.botonAgregarFichaSedacion.grid(row=0, column=2, padx=5, pady=15)

            if(mascotaActual.getOperacion(idFicha) == True):
                flagOperacion = True
                self.botonEditarFichaOperacion = ctk.CTkButton(self.frameButtonsSEditarFicha, width= 250, height= 80, text='Editar Ficha Operación', text_font=Font_tuple, hover_color="#142C3D", command=lambda: self.clickEditarOperacion(parent, container, flagOperacion))
                self.botonEditarFichaOperacion.grid(row=0, column=3, padx=5, pady=15)
            else:
                self.botonAgregarFichaOperacion = ctk.CTkButton(self.frameButtonsSEditarFicha, width= 250, height= 80, text='Agregar Ficha Operación', text_font=Font_tuple, hover_color="#142C3D", command=lambda: self.clickEditarOperacion(parent, container, flagOperacion))
                self.botonAgregarFichaOperacion.grid(row=0, column=3, padx=5, pady=15)

            self.botonVolverSEditarFicha = ctk.CTkButton(self.frameButtonsSEditarFicha, width= 200, height= 80, text='Volver', text_font=Font_tuple, hover_color="#142C3D", command=lambda: self.volverSDTotalMascota(parent, container, mascotaActual, idFicha))
            self.botonVolverSEditarFicha.grid(row=0, column=4, padx=15, pady=15)
            
    def clickEditarHosp(self, parent, container, flag):
        if(flag is False):
            parent.setFlagEditar(True)
            parent.update_frame(parent.screenFormularioCrearFichaHospt, parent, container)
        else:
            parent.update_frame(parent.screenFormularioEditarFichaHospt, parent, container)

    def clickEditarOperacion(self, parent, container, flag):
        if(flag is False):
            parent.setFlagEditar(True)
            parent.update_frame(parent.screenFormularioCrearFichaAuthCirugia, parent, container)
        else:
            parent.update_frame(parent.screenFormularioEditarFichaAuthCirugia, parent, container)

    def clickAgregarSedacion(self, parent, container):
        parent.setFlagEditar(True)
        parent.update_frame(parent.screenFormularioCrearFichaSedacion, parent, container)

    def clickEditarFicha(self, idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, idMascota, tratamientos, causaVisita, medicamentos, vacunas, terminalVet, mascotaActual):
        
        hoy = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        terminalVet.editarFichaMedica(idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, idMascota, tratamientos, causaVisita, medicamentos, vacunas, hoy)
        #self.botonEditarFichaGeneralSCrearFicha.configure(state=DISABLED)
        self.labelMensajeEditadoGeneral.grid(row=1, column=2, pady=15)
        mascotaActual.setActualFichaMedicaConsulta(str(fechaConsulta), True)
        
    def volverSDTotalMascota(self, parent, container, mascotaActual, idFicha):
        mascotaActual.quitarActualFichaMedicaConsulta(idFicha)
        parent.update_frame(parent.screenDatosTotalMascota, parent, container)
    

class screenFormularioCrearFicha(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ('Helvetica', 12)
        Font_tuple10 = ('Helvetica', 10)
        Font_tuple16 = ('Helvetica', 16)
        mascotaActual:Mascota = parent.getMascotaApp()
        if(mascotaActual != None):

     
            #Agregar Labels--------------------------------------------------------------------------------------------------------------------------------
            textoMascota = mascotaActual.getNombreMascota()
            self.labelTituloScreenSCrearFicha = ctk.CTkLabel(self, text=f"Creación de ficha, Mascota : {textoMascota}", text_font=Font_tuple16, text_color="black")
            self.labelTituloScreenSCrearFicha.grid(row=0, column=0, padx=10, pady=10)

            self.frameFormSCrearFicha = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameFormSCrearFicha.grid(row=1, column=0, padx=20, pady=20)

            self.frameButtonsSCrearFicha = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameButtonsSCrearFicha.grid(row=2, column=0, padx=20, pady=20)

            # self.frameButtonsVolver = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            # self.frameButtonsVolver.grid(row=1, column=2, padx=(20,5), pady=20)

            self.labelSucursalSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Sucursal Veterinaria", text_font=Font_tuple, text_color='black')
            self.labelSucursalSCrearFicha.grid(row = 0, column = 0, padx=(20,5), pady=15)
            
            self.labelVetACargoSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Veterinario a cargo", text_font=Font_tuple, text_color='black')
            self.labelVetACargoSCrearFicha.grid(row = 1, column = 0, padx=(20,5), pady=15)
            
            self.labelFechaConsultaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Fecha Consulta", text_font=Font_tuple, text_color='black')
            self.labelFechaConsultaSCrearFicha.grid(row = 2, column = 0, padx=(20,5), pady=15)
            
            self.labelTratamientosConsultaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Tratamientos Consulta", text_font=Font_tuple, text_color='black')
            self.labelTratamientosConsultaSCrearFicha.grid(row = 3, column = 0, padx=(20,5), pady=15)
            
            self.labelMedicamentosConsultaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Medicamentos Consulta", text_font=Font_tuple, text_color='black')
            self.labelMedicamentosConsultaSCrearFicha.grid(row = 4, column = 0, padx=(20,5), pady=15)
            
            self.labelCausaVisitaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Causa Visita", text_font=Font_tuple, text_color='black')
            self.labelCausaVisitaSCrearFicha.grid(row = 5, column = 0, padx=(20,5), pady=15)
            
            self.labelVacSuministradasSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Vacunas Suministradas", text_font=Font_tuple, text_color='black')
            self.labelVacSuministradasSCrearFicha.grid(row = 0, column = 2, padx=(20,5), pady=15)
            
            self.labelFrecRespiratoriaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Frecuencia Respiratoria", text_font=Font_tuple, text_color='black')
            self.labelFrecRespiratoriaSCrearFicha.grid(row = 1, column = 2, padx=(20,5), pady=15)

            self.labelFrecCardiacaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Frecuencia Cardiaca", text_font=Font_tuple, text_color='black')
            self.labelFrecCardiacaSCrearFicha.grid(row = 2, column = 2, padx=(20,5), pady=15)
            
            self.labelPesoSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Peso", text_font=Font_tuple, text_color='black')
            self.labelPesoSCrearFicha.grid(row = 3, column = 2, padx=(20,5), pady=15)
            
            self.labelEdadSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Edad", text_font=Font_tuple, text_color='black')
            self.labelEdadSCrearFicha.grid(row = 4, column = 2, padx=(20,5), pady=15)

            self.labelTemperaturaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Temperatura", text_font=Font_tuple, text_color='black')
            self.labelTemperaturaSCrearFicha.grid(row = 5, column = 2, padx=(20,5), pady=(15,35))

            self.labelMensajeAgregarSCrearFicha = ctk.CTkLabel(self.frameButtonsSCrearFicha, text="Ficha Agregada", text_font=Font_tuple, text_color="green")
            
            #Agregar Entrys------------------------------------------------------------------------------------------------------------------------------

            self.entradaSucursalSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black')
            self.entradaSucursalSCrearFicha.grid(row = 0, column = 1, padx=20, pady=15)

            self.entradaVetACargoSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black')
            self.entradaVetACargoSCrearFicha.grid(row = 1, column = 1, padx=20, pady=15)

            #scamos la fehca y hora actual

            textFechaActual = tk.StringVar()
            hoy = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            textFechaActual.set(str(hoy))
            
            self.entradaFechaConsultaSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='grey', text=textFechaActual, state=DISABLED)
            self.entradaFechaConsultaSCrearFicha.grid(row = 2, column = 1, padx=20, pady=15)

            self.entradaTratamientosConsultaSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black')
            self.entradaTratamientosConsultaSCrearFicha.grid(row = 3, column = 1, padx=20, pady=15)

            self.entradaMedicamentosConsultaSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", placeholder_text="Medicamento1; Medicamento2...", text_color='black')
            self.entradaMedicamentosConsultaSCrearFicha.grid(row = 4, column = 1, padx=20, pady=15)

            self.entradaCausaVisitaSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black')
            self.entradaCausaVisitaSCrearFicha.grid(row = 5, column = 1, padx=20, pady=15)

            self.entradaVacSuministradasSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", placeholder_text="Vacuna1; Vacuna2...", text_color='black')
            self.entradaVacSuministradasSCrearFicha.grid(row = 0, column = 3, padx=20, pady=15)

            self.entradaFrecRespiratoriaSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", placeholder_text="En RPM", text_color='black')
            self.entradaFrecRespiratoriaSCrearFicha.grid(row = 1, column = 3, padx=20, pady=15)

            self.entradaFrecCardiacaSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", placeholder_text="En BPM",text_color='black')
            self.entradaFrecCardiacaSCrearFicha.grid(row = 2, column = 3, padx=20, pady=15)

            self.entradaPesoSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", placeholder_text="En kg", text_color='black')
            self.entradaPesoSCrearFicha.grid(row = 3, column = 3, padx=20, pady=15)

            self.entradaEdadSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", placeholder_text="Ej: 2 años", text_color='black')
            self.entradaEdadSCrearFicha.grid(row = 4, column = 3, padx=20, pady=15)

            self.entradaTemperaturaSCrearFicha = ctk.CTkEntry(self.frameFormSCrearFicha, width = 400, text_font=Font_tuple, fg_color="#F0EFEB", text_color='black', placeholder_text="Ej: 32.3", )
            self.entradaTemperaturaSCrearFicha.grid(row = 5, column = 3, padx=20, pady=(15,35))

            #Agregar Buttons
            self.botonVolverSCrearFicha = ctk.CTkButton(self.frameButtonsSCrearFicha, width= 200, height= 80, text='Volver', text_font=Font_tuple, hover_color="#142C3D", command=lambda: self.clickVolver(parent, container, mascotaActual, self.entradaFechaConsultaSCrearFicha.get()))
            self.botonVolverSCrearFicha.grid(row=0, column=4, padx=15, pady=15)

            self.botonAgregarFichaGeneralSCrearFicha = ctk.CTkButton(self.frameButtonsSCrearFicha, width=250, height=80, text='Agregar Ficha General', text_font=Font_tuple, hover_color="#142C3D", command=lambda: self.validarDatosFicha(parent, self.entradaSucursalSCrearFicha.get(), 
            self.entradaVetACargoSCrearFicha.get(), self.entradaFechaConsultaSCrearFicha.get(), 0, self.entradaFrecRespiratoriaSCrearFicha.get(),
            self.entradaFrecCardiacaSCrearFicha.get(), self.entradaPesoSCrearFicha.get(), self.entradaEdadSCrearFicha.get(), 0, 0,  self.entradaTemperaturaSCrearFicha.get(), mascotaActual.getId(),
            self.entradaTratamientosConsultaSCrearFicha.get(), self.entradaCausaVisitaSCrearFicha.get() ,self.entradaMedicamentosConsultaSCrearFicha.get(), self.entradaVacSuministradasSCrearFicha.get(), terminalVet, mascotaActual))
            
            self.botonAgregarFichaGeneralSCrearFicha.grid(row=0, column=0, padx=15, pady=15)

            self.botonAgregarFichaHosp = ctk.CTkButton(self.frameButtonsSCrearFicha, width= 250, height= 80, text='Agregar Ficha Hospitalizacion', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenFormularioCrearFichaHospt, parent, container), state=DISABLED) #hay que agregar cauda de la visita a la base de datos
            self.botonAgregarFichaHosp.grid(row=0, column=1, padx=5, pady=15)
            
            self.botonAgregarFichaSedacion = ctk.CTkButton(self.frameButtonsSCrearFicha, width= 250, height= 80, text='Agregar Ficha Sedación', text_font=Font_tuple, hover_color="#142C3D", state=DISABLED, command=lambda: parent.update_frame(parent.screenFormularioCrearFichaSedacion, parent, container))
            self.botonAgregarFichaSedacion.grid(row=0, column=2, padx=5, pady=15)
            
            self.botonAgregarFichaOperacion = ctk.CTkButton(self.frameButtonsSCrearFicha, width= 250, height= 80, text='Agregar Ficha Operación', text_font=Font_tuple, hover_color="#142C3D", state=DISABLED, command=lambda: parent.update_frame(parent.screenFormularioCrearFichaAuthCirugia, parent, container))
            self.botonAgregarFichaOperacion.grid(row=0, column=3, padx=5, pady=15)

            self.labelErrorSucursalVetSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Ingrese sucursal válida (solo letras)", text_font=Font_tuple10, text_color='#c1121f')
            self.labelErrorTratamientosSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Ingrese tratamientos válidos (solo letras y ;)", text_font=Font_tuple10, text_color='#c1121f')
            self.labelErrorMedicamentosSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Ingrese medicamentos válidos (solo letras y ;)", text_font=Font_tuple10, text_color='#c1121f')
            self.labelErrorCausaVisitaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Ingrese causa de la visia válida (solo letras)", text_font=Font_tuple10, text_color='#c1121f')
            self.labelErrorVacunasSumSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Ingrese vacunas válidas (solo letras y ;)", text_font=Font_tuple10, text_color='#c1121f')
            self.labelErrorVetACargoSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Ingrese nombre válido (solo letras)", text_font=Font_tuple10, text_color='#c1121f')
            self.labelErrorFrecRespSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Ingrese frecuencia respitatoria válida (solo numeros)", text_font=Font_tuple10, text_color='#c1121f')
            self.labelErrorFrecCardSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Ingrese frecuencia cardiaca válida (solo numeros)", text_font=Font_tuple10, text_color='#c1121f')
            self.labelErrorPesoSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Ingrese peso válido (solo numeros)", text_font=Font_tuple10, text_color='#c1121f')
            self.labelErrorEdadSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Ingrese edad válida (solo numeros)", text_font=Font_tuple10, text_color='#c1121f')
            self.labelErrorTemperaturaSCrearFicha = ctk.CTkLabel(self.frameFormSCrearFicha, text="Ingrese temperatura válida (solo numeros)", text_font=Font_tuple10, text_color='#c1121f')
        

    def validarDatosFicha(self, parent, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, idMascota, tratamientos, causaVisita, medicamentos, vacunas, terminalVet, mascotaActual):
        flag = True

        if(parent.filtroNoValidChar(sucursalVeterinaria) is not True or parent.filtroNum(sucursalVeterinaria) is not False or len(sucursalVeterinaria) == 0):
            flag = False
            self.labelErrorSucursalVetSCrearFicha.place(x="230", y="44")
        else:
            self.labelErrorSucursalVetSCrearFicha.place_forget()

        if(parent.filtroNoValidChar(veterinarioACargo) is not True or parent.filtroNum(veterinarioACargo) is not False or len(veterinarioACargo) == 0):
            flag = False
            self.labelErrorVetACargoSCrearFicha.place(x="230", y="102")
        else:
            self.labelErrorVetACargoSCrearFicha.place_forget()
        
        if(parent.filtroNoValidChar(tratamientos) is not True or parent.filtroNum(tratamientos) is not False or len(tratamientos) == 0):
            flag = False
            self.labelErrorTratamientosSCrearFicha.place(x="230", y="218")
        else:
            self.labelErrorTratamientosSCrearFicha.place_forget()

        if(parent.filtroNoValidChar(medicamentos) is not True or parent.filtroNum(medicamentos) is not False or len(medicamentos) == 0):
            flag = False
            self.labelErrorMedicamentosSCrearFicha.place(x="230", y="276")
        else:
            self.labelErrorMedicamentosSCrearFicha.place_forget()

        if(parent.filtroNoValidChar(causaVisita) is not True or parent.filtroNum(causaVisita) is not False or len(causaVisita) == 0):
            flag = False
            self.labelErrorCausaVisitaSCrearFicha.place(x="230", y="334")
        else:
            self.labelErrorCausaVisitaSCrearFicha.place_forget()
        
        if(parent.filtroNoValidChar(vacunas) is not True or parent.filtroNum(vacunas) is not False or len(vacunas) == 0):
            flag = False
            self.labelErrorVacunasSumSCrearFicha.place(x="230", y="391")
        else:
            self.labelErrorVacunasSumSCrearFicha.place_forget()

        if(parent.filtroNoValidChar(frecRespiratoria) is not True or parent.filtroNum(frecRespiratoria) is not True or len(frecRespiratoria) == 0):
            flag = False
            self.labelErrorFrecRespSCrearFicha.place(x="230", y="449")
        else:
            self.labelErrorFrecRespSCrearFicha.place_forget()

        if(parent.filtroNoValidChar(frecCardiaca) is not True or parent.filtroNum(frecCardiaca) is not True or len(frecCardiaca) == 0):
            flag = False
            self.labelErrorFrecCardSCrearFicha.place(x="230", y="507")
        else:
            self.labelErrorFrecCardSCrearFicha.place_forget() 

        if(parent.filtroNoValidChar(peso) is not True is not True or len(peso) == 0):
            flag = False
            self.labelErrorPesoSCrearFicha.place(x="230", y="565")
        else:
            self.labelErrorPesoSCrearFicha.place_forget()

        if(parent.filtroNoValidChar(edad) is not True is not True or len(edad) == 0):
            flag = False
            self.labelErrorEdadSCrearFicha.place(x="230", y="624")
        else:
            self.labelErrorEdadSCrearFicha.place_forget()

        if(parent.filtroNoValidChar(temp) is not True is not True or len(temp) == 0):
            flag = False
            self.labelErrorTemperaturaSCrearFicha.place(x="230", y="682")
        else:
            self.labelErrorTemperaturaSCrearFicha.place_forget() 
        
        if(flag is True):
            self.clickAgregarFicha(sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, idMascota, tratamientos, causaVisita, medicamentos, vacunas, terminalVet, mascotaActual)

    def clickAgregarFicha(self, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, idMascota, tratamientos, causaVisita, medicamentos, vacunas, terminalVet, mascotaActual):
        terminalVet.agregarFichaMedica(sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, idMascota, tratamientos, causaVisita, medicamentos, vacunas)
        self.botonAgregarFichaGeneralSCrearFicha.configure(state=DISABLED)

        self.botonAgregarFichaOperacion.configure(state=NORMAL)
        self.botonAgregarFichaSedacion.configure(state=NORMAL)
        self.botonAgregarFichaHosp.configure(state=NORMAL)
        self.labelMensajeAgregarSCrearFicha.grid(row=1, column=2)

        mascotaActual.setActualFichaMedicaConsulta(str(fechaConsulta), True)
        
    def clickVolver(self, parent, container, mascotaActual, fechaConsulta):

        mascotaActual.setActualFichaMedicaConsulta(fechaConsulta, False)
        parent.update_frame(parent.screenDatosTotalMascota, parent, container)
        
        
class screenFormularioAgregarMascota(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 12)
        Font_tuple14 = ("Helvetica", 14)
        Font_tuple16 = ("Helvetica", 16)

        self.labelTituloScreenSAgregarFicha = ctk.CTkLabel(self, text="Agregando mascota", text_font=Font_tuple16, text_color="black")
        self.labelTituloScreenSAgregarFicha.grid(row=0, column=0, padx=10, pady=10)

        self.frameFormSAgregarMascota = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
        self.frameFormSAgregarMascota.grid(row=1, column=0, padx=20, pady=20)

        self.frameButtonsSAgregarMascota = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
        self.frameButtonsSAgregarMascota.grid(row=2, column=0, padx=20, pady=20)

        self.labelNombreMascotaSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Nombre Mascota", text_font=Font_tuple, text_color="black")
        self.labelNombreMascotaSAgregarMascota.grid(row=0, column=0, padx=(20,5), pady=15)

        self.labelEspecieSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Especie ", text_font=Font_tuple, text_color="black")
        self.labelEspecieSAgregarMascota.grid(row=1, column=0, padx=(20,5), pady=15)

        self.labelColorSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Color", text_font=Font_tuple, text_color="black")
        self.labelColorSAgregarMascota.grid(row=2, column=0, padx=(20,5), pady=15)

        self.labelRazaSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Raza", text_font=Font_tuple, text_color="black")
        self.labelRazaSAgregarMascota.grid(row=3, column=0, padx=(20,5), pady=15)

        self.labelNombreTutorSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Nombre Tutor", text_font=Font_tuple, text_color="black")
        self.labelNombreTutorSAgregarMascota.grid(row=4, column=0, padx=(20,5), pady=15)
        
        self.labelRutTutorSAgregarMascota =ctk.CTkLabel(self.frameFormSAgregarMascota, text="Rut Tutor", text_font=Font_tuple, text_color="black")
        self.labelRutTutorSAgregarMascota.grid(row=0, column=2, padx=(20,5), pady=15)

        self.labelNumeroTelefonoSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Número de Teléfono",text_font=Font_tuple, text_color="black")
        self.labelNumeroTelefonoSAgregarMascota.grid(row=1, column=2, padx=(20,5), pady=15)

        self.labelDireccionTutorSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Dirección Tutor", text_font=Font_tuple, text_color="black")
        self.labelDireccionTutorSAgregarMascota.grid(row=2, column=2, padx=(20,5), pady=15)

        self.labelAlergiasSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Alergias", text_font=Font_tuple, text_color="black")
        self.labelAlergiasSAgregarMascota.grid(row=3, column=2, padx=(20,5), pady=15)

        self.labelFechaNacSAgregarMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Fecha de nacimiento", text_font=Font_tuple, text_color="black")
        self.labelFechaNacSAgregarMascota.grid(row=4, column=2, padx=(20,5), pady=15)

        self.labelMensajeAgregarMascota = ctk.CTkLabel(self.frameButtonsSAgregarMascota, text="Mascota Agregada", text_font=Font_tuple, text_color="green")


        #Agregar Entrys
    
        self.entradaNombreMascotaSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB")
        self.entradaNombreMascotaSAgregarMascota.grid(row=0, column=1, padx=20, pady=15)

        self.entradaEspecieSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB")
        self.entradaEspecieSAgregarMascota.grid(row=1, column=1, padx=20, pady=15)

        self.entradaColorSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB")
        self.entradaColorSAgregarMascota.grid(row=2, column=1, padx=20, pady=15)

        self.entradaRazaSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB")
        self.entradaRazaSAgregarMascota.grid(row=3, column=1, padx=20, pady=15)
        
        self.entradaNombreTutorSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB")
        self.entradaNombreTutorSAgregarMascota.grid(row=4, column=1, padx=20, pady=15)
        
        self.entradaRutTutorSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, placeholder_text="9123456-k", text_color="black", fg_color="#F0EFEB")
        self.entradaRutTutorSAgregarMascota.grid(row=0, column=3, padx=20, pady=15)
        
        self.entradaNumeroTelefonoSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, placeholder_text="56911112222",text_color="black", fg_color="#F0EFEB")
        self.entradaNumeroTelefonoSAgregarMascota.grid(row=1, column=3, padx=20, pady=15)

        self.entradaDireccionTutorSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB")
        self.entradaDireccionTutorSAgregarMascota.grid(row=2, column=3, padx=20, pady=15)

        self.entradaAlergiasSAgregarMascota = ctk.CTkEntry(self.frameFormSAgregarMascota, width = 400, text_font=Font_tuple, placeholder_text="Alergia1; Alergia2...",text_color="black", fg_color="#F0EFEB")
        self.entradaAlergiasSAgregarMascota.grid(row=3, column=3, padx=20, pady=15)

        self.entradaFechaNacSAgregarMascota = DateEntry(self.frameFormSAgregarMascota, width = 20)
        self.entradaFechaNacSAgregarMascota.grid(row=4, column=3, padx=20, pady=15)
        
        self.labelErrorNombreMascota = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Ingrese nombre válido (Solo letras)", text_font=Font_tuple, text_color="#c1121f")
        self.labelErrorEspecie = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Ingrese espeice válida (Solo letras)", text_font=Font_tuple, text_color="#c1121f")
        self.labelErrorColor = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Ingrese color válido (Solo letras)", text_font=Font_tuple, text_color="#c1121f")
        self.labelErrorRaza = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Ingrese raza válida (Solo letras)", text_font=Font_tuple, text_color="#c1121f")
        self.labelErrorNombreTutor = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Ingrese nombre tutor válido (Solo letras)", text_font=Font_tuple, text_color="#c1121f")
        self.labelErrorRutTutor = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Ingrese rut válido", text_font=Font_tuple, text_color="#c1121f")
        self.labelErrorNumeroTelefono = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Ingrese número válido (Solo números)", text_font=Font_tuple, text_color="#c1121f")
        self.labelErrorDireccion = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Ingrese dirección válida (Solo letras y números)", text_font=Font_tuple, text_color="#c1121f")
        self.labelErrorAlergias = ctk.CTkLabel(self.frameFormSAgregarMascota, text="Ingrese alergias válidas (Solo letras y ;)", text_font=Font_tuple, text_color="#c1121f")

        #Agregar buttons
        self.botonIrScreenInicialSCrearFicha = ctk.CTkButton(self.frameButtonsSAgregarMascota, width= 200, height= 120,text='Ir a pantalla inicial', text_font= Font_tuple14, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenPantallaInicial, parent, container))
        self.botonIrScreenInicialSCrearFicha.grid(row=0, column=0, padx=25, pady=15)

        self.botonIrScreenBuscarSCrearFicha = ctk.CTkButton(self.frameButtonsSAgregarMascota, width= 200, height= 120,text='Ir a pantalla para buscar mascota', text_font= Font_tuple14, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenBuscarMascota, parent, container))
        self.botonIrScreenBuscarSCrearFicha.grid(row=0, column=1, padx=15, pady=15)
        
        self.botonAgregarMascota = ctk.CTkButton(self.frameButtonsSAgregarMascota, width= 200, height= 120,text='Agregar Mascota', text_font= Font_tuple14, hover_color="#142C3D", command=lambda: self.validarDatos(parent,
            self.entradaNombreMascotaSAgregarMascota.get(), self.entradaEspecieSAgregarMascota.get(), self.entradaColorSAgregarMascota.get(), self.entradaRazaSAgregarMascota.get(), self.entradaNombreTutorSAgregarMascota.get(),
            self.entradaRutTutorSAgregarMascota.get(), self.entradaNumeroTelefonoSAgregarMascota.get(), self.entradaDireccionTutorSAgregarMascota.get(), self.entradaAlergiasSAgregarMascota.get(), self.entradaFechaNacSAgregarMascota.get()))
        self.botonAgregarMascota.grid(row=0, column=2, padx=25, pady=15)

        self.buttonCrearFicha = ctk.CTkButton(self.frameButtonsSAgregarMascota, width= 175, height= 100,text='Crear Ficha', hover_color="#142C3D", text_font=Font_tuple, command=lambda: parent.update_frame(parent.screenFormularioCrearFicha, parent, container))
    
    def validarDatos(self, parent, nombreMascota, especie, color, raza, nombreTutor, rutTutor, numTel, direccion, alergias, fechaNac):
        
        flag = True

        if((parent.filtroNoValidChar(nombreMascota) is not True) or (parent.filtroNum(nombreMascota) is not False) or (len(nombreMascota) < 3)):
            flag = False
            self.labelErrorNombreMascota.place(x="215", y="54")
        else: 
            self.labelErrorNombreMascota.place_forget()

        if((parent.filtroNoValidChar(especie) is not True) or (parent.filtroNum(especie) is not False) or (len(especie) == 0)):
            flag = False
            self.labelErrorEspecie.place(x="215", y="122")
        else: 
            self.labelErrorEspecie.place_forget()

        if((parent.filtroNoValidChar(color) is not True) or (parent.filtroNum(color) is not False) or (len(color) == 0)):
            flag = False
            self.labelErrorColor.place(x="215", y="190")
        else: 
            self.labelErrorColor.place_forget()

        if((parent.filtroNoValidChar(raza) is not True) or (parent.filtroNum(raza) is not False) or (len(raza) == 0)):
            flag = False
            self.labelErrorRaza.place(x="215", y="258")
        else: 
            self.labelErrorRaza.place_forget()

        if((parent.filtroNoValidChar(nombreTutor) is not True) or (parent.filtroNum(nombreTutor) is not False) or (len(nombreTutor) < 3)):
            flag = False
            self.labelErrorNombreTutor.place(x="215", y="326")
        else: 
            self.labelErrorNombreTutor.place_forget()

        if(parent.validarRut(rutTutor) is not True):
            flag = False
            self.labelErrorRutTutor.place(x="205", y="395")
        else:
            print("Valid")
            self.labelErrorRutTutor.place_forget()

        if((parent.filtroNum(numTel) is not True) or (parent.filtroNoValidChar(numTel) is not True) or (len(numTel) < 9)):
            flag = False
            self.labelErrorNumeroTelefono.place(x="215", y="463")
        else: 
            self.labelErrorNumeroTelefono.place_forget()

        if((parent.filtroNoValidChar(direccion) is not True) or (len(direccion) == 0)):
            flag = False
            self.labelErrorDireccion.place(x="215", y="529")
        else: 
            self.labelErrorDireccion.place_forget()

        if((parent.filtroNoValidChar(alergias) is not True) or (parent.filtroNum(alergias) is not False) or (len(alergias) == 0)):
            flag = False
            self.labelErrorAlergias.place(x="215", y="596")
        else: 
            self.labelErrorAlergias.place_forget()

        if(flag):
            self.clickAgregarMascota(parent, nombreMascota, especie, color, raza, nombreTutor, rutTutor, numTel, alergias, direccion, fechaNac)



    def clickAgregarMascota(self, parent, nombreMascota, especie, color, raza, nombreTutor, rutTutor, numTel, alergias, direccion, fechaNacimiento):

        idNuevaMascota = parent.getIdNuevaMascota()
        tablaMedica = TablaMedica(uuid.uuid4())
        terminalVet.agregarMascota(idNuevaMascota, nombreMascota, especie, color, raza, nombreTutor, rutTutor, numTel, direccion, alergias, tablaMedica, fechaNacimiento)
        self.labelMensajeAgregarMascota.pack()
        self.botonAgregarMascota.configure(state="disabled")
        #self.buttonCrearFicha.pack(padx=10, pady=20)

class screenFormularioFichaAuthCirugia(ctk.CTkFrame): #Ta weno ya
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 12)
        Font_tuple16 = ("Helvetica", 16)
        mascotaActual:Mascota = parent.getMascotaApp()
        if(mascotaActual is not None):
            
            idFicha = mascotaActual.getidFichaActual()
            textoMascota = mascotaActual.getNombreMascota()
            self.labelTituloScreenSFichaAuthCirugia = ctk.CTkLabel(self, text=f"Visualización de ficha autorización a cirugia, Mascota : {textoMascota}", text_font=Font_tuple16, text_color="black")
            self.labelTituloScreenSFichaAuthCirugia.grid(row=0, column=0, padx=10, pady=10)

            self.frameFormSFichaAuthCirugia = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameFormSFichaAuthCirugia.grid(row=1, column=0, padx=20, pady=10)
    
            self.frameButtonsSFichaAuthCirugia = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameButtonsSFichaAuthCirugia.grid(row=2, column=0, padx=20, pady=10)
    
            self.frameText = ctk.CTkFrame(self.frameFormSFichaAuthCirugia, corner_radius=0, fg_color="#4e5257")
            self.frameText.grid(row=6, column=1, padx=20, pady=10)
    
            self.labelNombrePacienteSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Nombre Paciente", text_font=Font_tuple, text_color="black")
            self.labelNombrePacienteSFichaAuthCirugia.grid(row=0, column=0, padx=(20,5), pady=15)
    
            self.labelPesoSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Peso", text_font=Font_tuple, text_color="black")
            self.labelPesoSFichaAuthCirugia.grid(row=1, column=0, padx=(20,5), pady=15)
    
            self.labelEspecieSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Especie", text_font=Font_tuple, text_color="black")
            self.labelEspecieSFichaAuthCirugia.grid(row=2, column=0, padx=(20,5), pady=15)
    
            self.labelEdadSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Edad", text_font=Font_tuple, text_color="black")
            self.labelEdadSFichaAuthCirugia.grid(row=3, column=0, padx=(20,5), pady=15)
            
            self.labelRazaSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Raza", text_font=Font_tuple, text_color="black")
            self.labelRazaSFichaAuthCirugia.grid(row=4, column=0, padx=(20,5), pady=15)
            
            self.labelColorSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Color", text_font=Font_tuple, text_color="black")
            self.labelColorSFichaAuthCirugia.grid(row=5, column=0, padx=(20,5), pady=15)
            
            self.labelDiagnosticoSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Diagnóstico", text_font=Font_tuple, text_color="black")
            self.labelDiagnosticoSFichaAuthCirugia.grid(row=6, column=0, padx=(20,5), pady=15)
            
            self.labelCirugiaARealizarSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Cirugía a Realizar", text_font=Font_tuple, text_color="black")
            self.labelCirugiaARealizarSFichaAuthCirugia.grid(row=0, column=2, padx=(20,5), pady=15)
            
            self.labelNombreDelTutorSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Nombre del Tutor", text_font=Font_tuple, text_color="black")
            self.labelNombreDelTutorSFichaAuthCirugia.grid(row=1, column=2, padx=(20,5), pady=15)
    
            self.labelRutTutorSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Rut Tutor", text_font=Font_tuple, text_color="black")
            self.labelRutTutorSFichaAuthCirugia.grid(row=2, column=2, padx=(20,5), pady=15)
            
            self.labelNumeroTelefonoSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Número de Teléfono", text_font=Font_tuple, text_color="black")
            self.labelNumeroTelefonoSFichaAuthCirugia.grid(row=3, column=2, padx=(20,5), pady=15)
    
            self.labelDireccionSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Dirección", text_font=Font_tuple, text_color="black")
            self.labelDireccionSFichaAuthCirugia.grid(row=4, column=2, padx=(20,5), pady=15)
    
            self.labelAuthTutorSFichaAuthCirugia = ctk.CTkLabel(self.frameFormSFichaAuthCirugia, text="Autorizacion tutor", text_font=Font_tuple, text_color="black")
            self.labelAuthTutorSFichaAuthCirugia.grid(row=5, column=2, padx=(20,5), pady=15)

    
            #Agregar Entrys
            self.textVarNombrePaciente = tk.StringVar()
            self.textVarPeso = tk.StringVar()
            self.textVarEspecie = tk.StringVar()
            self.textVarEdad = tk.StringVar()
            self.textVarRaza = tk.StringVar()
            self.textVarColor = tk.StringVar()
            self.textVarCirugia = tk.StringVar()
            self.textVarNombreTutor = tk.StringVar()
            self.textVarRut = tk.StringVar()
            self.textVarTelefono = tk.StringVar()
            self.textVarDireccion = tk.StringVar()
            
            self.textVarNombrePaciente.set(mascotaActual.getNombreMascota())
            self.entradaNombrePacienteSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarNombrePaciente,  state=DISABLED)
            self.entradaNombrePacienteSFichaAuthCirugia.grid(row=0, column=1, padx=20, pady=15)

            self.textVarPeso.set(mascotaActual.getPeso(idFicha))
            self.entradaPesoSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarPeso,  state=DISABLED)
            self.entradaPesoSFichaAuthCirugia.grid(row=1, column=1, padx=20, pady=15)

            self.textVarEspecie.set(mascotaActual.getEspecie())
            self.entradaEspecieSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarEspecie,  state=DISABLED)
            self.entradaEspecieSFichaAuthCirugia.grid(row=2, column=1, padx=20, pady=15)

            self.textVarEdad.set(mascotaActual.getEdad(idFicha))
            self.entradaEdadConsultaSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarEdad,  state=DISABLED)
            self.entradaEdadConsultaSFichaAuthCirugia.grid(row=3, column=1, padx=20, pady=15)
            
            self.textVarRaza.set(mascotaActual.getRaza())
            self.entradaRazaSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarRaza,  state=DISABLED)
            self.entradaRazaSFichaAuthCirugia.grid(row=4, column=1, padx=20, pady=15)

            self.textVarColor.set(mascotaActual.getColorMascota())
            self.entradaColorSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarColor,  state=DISABLED)
            self.entradaColorSFichaAuthCirugia.grid(row=5, column=1, padx=20, pady=15)

            operacion = mascotaActual.getOperacionFicha(idFicha)

            self.entradaDiagnosticoSFichaAuthCirugia = tk.Text(self.frameText, width = 44, height= 3, background="#F0EFEB", font=("Helvetica", 12), state=NORMAL)
            self.entradaDiagnosticoSFichaAuthCirugia.delete(1.0, END)
            self.entradaDiagnosticoSFichaAuthCirugia.grid(row=0, column=0, padx=2, pady=2)
            self.entradaDiagnosticoSFichaAuthCirugia.insert(END, operacion['diagnostico'])
            self.entradaDiagnosticoSFichaAuthCirugia.configure(state="disabled")


            self.textVarCirugia.set(operacion['cirugiaARealizar'])
            self.entradaCirugiaARealizarSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarCirugia,  state=DISABLED)
            self.entradaCirugiaARealizarSFichaAuthCirugia.grid(row=0, column=3, padx=20, pady=15)

            self.textVarNombreTutor.set(mascotaActual.getNombreTutor())
            self.entradaNombreTutorSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarNombreTutor,  state=DISABLED)
            self.entradaNombreTutorSFichaAuthCirugia.grid(row=1, column=3, padx=20, pady=15)

            self.textVarRut.set(mascotaActual.getRutTutor())
            self.entradaRutSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarRut,  state=DISABLED)
            self.entradaRutSFichaAuthCirugia.grid(row=2, column=3, padx=20, pady=15)

            self.textVarTelefono.set(mascotaActual.getNumeroTelefono())
            self.entradaNumTelefonoSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarTelefono,  state=DISABLED)
            self.entradaNumTelefonoSFichaAuthCirugia.grid(row=3, column=3, padx=20, pady=15)

            self.textVarDireccion.set(mascotaActual.getDireccion())
            self.entradaDireccionSFichaAuthCirugia = ctk.CTkEntry(self.frameFormSFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarDireccion,  state=DISABLED)
            self.entradaDireccionSFichaAuthCirugia.grid(row=4, column=3, padx=20, pady=15)

            var = tk.IntVar()
            var.set(1)

            if(operacion['autTutor'] == True):
                self.entradaAuthTutorSFichaAuthCirugia = ctk.CTkCheckBox(self.frameFormSFichaAuthCirugia, fg_color="#0D1D29", border_width=2, border_color="grey", variable=var, onvalue=1, state=DISABLED, text="")
            else:
                self.entradaAuthTutorSFichaAuthCirugia = ctk.CTkCheckBox(self.frameFormSFichaAuthCirugia, fg_color="#0D1D29", border_width=2, border_color="grey", variable=var, offvalue=0, state=DISABLED, text="")
            self.entradaAuthTutorSFichaAuthCirugia.grid(row=5, column=3, padx=20, pady=15)
    
            #Agregar botones
            self.botonVolverSFichaAuthCirugia = ctk.CTkButton(self.frameButtonsSFichaAuthCirugia, width= 250, height= 80, text='Volver', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenFormularioVerFicha, parent, container))
            self.botonVolverSFichaAuthCirugia.pack(padx= 10, pady = 40)


class screenFormularioEditarFichaAuthCirugia(ctk.CTkFrame): #Ta weno ya
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 12)
        Font_tuple16 = ("Helvetica", 16)

        mascotaActual:Mascota = parent.getMascotaApp()
        if(mascotaActual is not None):
            
            idFicha = mascotaActual.getidFichaActual()
            textoMascota = mascotaActual.getNombreMascota()
            self.labelTituloScreenSEditarFichaAuthCirugia = ctk.CTkLabel(self, text=f"Edición de ficha autorización cirugía, Mascota : {textoMascota}", text_font=Font_tuple16, text_color="black")
            self.labelTituloScreenSEditarFichaAuthCirugia.grid(row=0, column=0, padx=10, pady=10)

            self.frameFormSEditarFichaAuthCirugia = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameFormSEditarFichaAuthCirugia.grid(row=1, column=0, padx=20, pady=10)
    
            self.frameButtonsSEditarFichaAuthCirugia = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameButtonsSEditarFichaAuthCirugia.grid(row=2, column=0, padx=20, pady=10)
    
            self.frameText = ctk.CTkFrame(self.frameFormSEditarFichaAuthCirugia, corner_radius=0, fg_color="#4e5257")
            self.frameText.grid(row=6, column=1, padx=25, pady=10)
    
            self.labelNombrePacienteSEditarFichaAuthCirugia = ctk.CTkLabel(self.frameFormSEditarFichaAuthCirugia, text="Nombre Paciente", text_font=Font_tuple, text_color="black")
            self.labelNombrePacienteSEditarFichaAuthCirugia.grid(row=0, column=0, padx=(20,5), pady=15)
    
            self.labelPesoSEditarFichaAuthCirugia = ctk.CTkLabel(self.frameFormSEditarFichaAuthCirugia, text="Peso", text_font=Font_tuple, text_color="black")
            self.labelPesoSEditarFichaAuthCirugia.grid(row=1, column=0, padx=(20,5), pady=15)
    
            self.labelEspecieSEditarFichaAuthCirugia = ctk.CTkLabel(self.frameFormSEditarFichaAuthCirugia, text="Especie", text_font=Font_tuple, text_color="black")
            self.labelEspecieSEditarFichaAuthCirugia.grid(row=2, column=0, padx=(20,5), pady=15)
    
            self.labelEdadSEditarFichaAuthCirugia = ctk.CTkLabel(self.frameFormSEditarFichaAuthCirugia, text="Edad", text_font=Font_tuple, text_color="black")
            self.labelEdadSEditarFichaAuthCirugia.grid(row=3, column=0, padx=(20,5), pady=15)
            
            self.labelRazaSEditarFichaAuthCirugia = ctk.CTkLabel(self.frameFormSEditarFichaAuthCirugia, text="Raza", text_font=Font_tuple, text_color="black")
            self.labelRazaSEditarFichaAuthCirugia.grid(row=4, column=0, padx=(20,5), pady=15)
            
            self.labelColorSEditarFichaAuthCirugia = ctk.CTkLabel(self.frameFormSEditarFichaAuthCirugia, text="Color", text_font=Font_tuple, text_color="black")
            self.labelColorSEditarFichaAuthCirugia.grid(row=5, column=0, padx=(20,5), pady=15)
            
            self.labelDiagnosticoSEditarFichaAuthCirugia = ctk.CTkLabel(self.frameFormSEditarFichaAuthCirugia, text="Diagnóstico", text_font=Font_tuple, text_color="black")
            self.labelDiagnosticoSEditarFichaAuthCirugia.grid(row=6, column=0, padx=(20,5), pady=15)
            
            self.labelCirugiaARealizarSEditarFichaAuthCirugia = ctk.CTkLabel(self.frameFormSEditarFichaAuthCirugia, text="Cirugía a Realizar", text_font=Font_tuple, text_color="black")
            self.labelCirugiaARealizarSEditarFichaAuthCirugia.grid(row=0, column=2, padx=(20,5), pady=15)
            
            self.labelNombreDelTutorSEditarFichaAuthCirugia = ctk.CTkLabel(self.frameFormSEditarFichaAuthCirugia, text="Nombre del Tutor", text_font=Font_tuple, text_color="black")
            self.labelNombreDelTutorSEditarFichaAuthCirugia.grid(row=1, column=2, padx=(20,5), pady=15)
    
            self.labelRutTutorSEditarFichaAuthCirugia = ctk.CTkLabel(self.frameFormSEditarFichaAuthCirugia, text="Rut Tutor", text_font=Font_tuple, text_color="black")
            self.labelRutTutorSEditarFichaAuthCirugia.grid(row=2, column=2, padx=(20,5), pady=15)
            
            self.labelNumeroTelefonoSEditarFichaAuthCirugia = ctk.CTkLabel(self.frameFormSEditarFichaAuthCirugia, text="Número de Teléfono", text_font=Font_tuple, text_color="black")
            self.labelNumeroTelefonoSEditarFichaAuthCirugia.grid(row=3, padx=(20,5), pady=15)
    
            self.labelDireccionSEditarFichaAuthCirugia = ctk.CTkLabel(self.frameFormSEditarFichaAuthCirugia, text="Dirección", text_font=Font_tuple, text_color="black")
            self.labelDireccionSEditarFichaAuthCirugia.grid(row=4, padx=(20,5), pady=15)
    
            self.labelAuthTutorSEditarFichaAuthCirugia = ctk.CTkLabel(self.frameFormSEditarFichaAuthCirugia, text="Autorizacion tutor", text_font=Font_tuple, text_color="black")
            self.labelAuthTutorSEditarFichaAuthCirugia.grid(row=5, padx=(20,5), pady=15)

            self.labelMensajeEditadoFichaAuthCirugia = ctk.CTkLabel(self.frameButtonsSEditarFichaAuthCirugia, text="Ficha Editada", text_font=Font_tuple, text_color="green")

            #Agregar Entrys
            self.textVarNombrePaciente = tk.StringVar()
            self.textVarPeso = tk.StringVar()
            self.textVarEspecie = tk.StringVar()
            self.textVarEdad = tk.StringVar()
            self.textVarRaza = tk.StringVar()
            self.textVarColor = tk.StringVar()
            self.textVarCirugia = tk.StringVar()
            self.textVarDiagnostico = tk.StringVar()
            self.textVarNombreTutor = tk.StringVar()
            self.textVarRut = tk.StringVar()
            self.textVarTelefono = tk.StringVar()
            self.textVarDireccion = tk.StringVar()
            
            self.textVarNombrePaciente.set(mascotaActual.getNombreMascota())
            self.entradaNombrePacienteSEditarFichaAuthCirugia = ctk.CTkEntry(self.frameFormSEditarFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarNombrePaciente,  state=DISABLED)
            self.entradaNombrePacienteSEditarFichaAuthCirugia.grid(row=0, column=1, padx=25, pady=15)

            self.textVarPeso.set(mascotaActual.getPeso(idFicha))
            self.entradaPesoSEditarFichaAuthCirugia = ctk.CTkEntry(self.frameFormSEditarFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarPeso,  state=DISABLED)
            self.entradaPesoSEditarFichaAuthCirugia.grid(row=1, column=1, padx=25, pady=15)

            self.textVarEspecie.set(mascotaActual.getEspecie())
            self.entradaEspecieSEditarFichaAuthCirugia = ctk.CTkEntry(self.frameFormSEditarFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarEspecie,  state=DISABLED)
            self.entradaEspecieSEditarFichaAuthCirugia.grid(row=2, column=1, padx=25, pady=15)

            self.textVarEdad.set(mascotaActual.getEdad(idFicha))
            self.entradaEdadConsultaSEditarFichaAuthCirugia = ctk.CTkEntry(self.frameFormSEditarFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarEdad,  state=DISABLED)
            self.entradaEdadConsultaSEditarFichaAuthCirugia.grid(row=3, column=1, padx=25, pady=15)
            
            self.textVarRaza.set(mascotaActual.getRaza())
            self.entradaRazaSEditarFichaAuthCirugia = ctk.CTkEntry(self.frameFormSEditarFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarRaza,  state=DISABLED)
            self.entradaRazaSEditarFichaAuthCirugia.grid(row=4, column=1, padx=25, pady=15)

            self.textVarColor.set(mascotaActual.getColorMascota())
            self.entradaColorSEditarFichaAuthCirugia = ctk.CTkEntry(self.frameFormSEditarFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarColor,  state=DISABLED)
            self.entradaColorSEditarFichaAuthCirugia.grid(row=5, column=1, padx=25, pady=15)

            operacion = mascotaActual.getOperacionFicha(idFicha)

            self.entradaDiagnosticoSEditarFichaAuthCirugia = tk.Text(self.frameText, width = 44, height= 3, background="#F0EFEB", font=("Helvetica", 12), borderwidth=0)
            self.entradaDiagnosticoSEditarFichaAuthCirugia.delete(1.0, END)
            self.entradaDiagnosticoSEditarFichaAuthCirugia.grid(row=0, column=0, padx=2, pady=2)
            self.entradaDiagnosticoSEditarFichaAuthCirugia.insert(END, operacion['diagnostico'])
            self.entradaDiagnosticoSEditarFichaAuthCirugia.grid(row=0, column=0, padx=2, pady=2)
  

            self.textVarCirugia.set(operacion['cirugiaARealizar'])
            self.entradaCirugiaARealizarSEditarFichaAuthCirugia = ctk.CTkEntry(self.frameFormSEditarFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB", text=self.textVarCirugia)
            self.entradaCirugiaARealizarSEditarFichaAuthCirugia.grid(row=0, column=3, padx=25, pady=15)

            self.textVarNombreTutor.set(mascotaActual.getNombreTutor())
            self.entradaNombreTutorSEditarFichaAuthCirugia = ctk.CTkEntry(self.frameFormSEditarFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarNombreTutor,  state=DISABLED)
            self.entradaNombreTutorSEditarFichaAuthCirugia.grid(row=1, column=3, padx=25, pady=15)

            self.textVarRut.set(mascotaActual.getRutTutor())
            self.entradaRutSEditarFichaAuthCirugia = ctk.CTkEntry(self.frameFormSEditarFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarRut,  state=DISABLED)
            self.entradaRutSEditarFichaAuthCirugia.grid(row=2, column=3, padx=25, pady=15)

            self.textVarTelefono.set(mascotaActual.getNumeroTelefono())
            self.entradaNumTelefonoSEditarFichaAuthCirugia = ctk.CTkEntry(self.frameFormSEditarFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarTelefono,  state=DISABLED)
            self.entradaNumTelefonoSEditarFichaAuthCirugia.grid(row=3, column=3, padx=25, pady=15)

            self.textVarDireccion.set(mascotaActual.getDireccion())
            self.entradaDireccionSEditarFichaAuthCirugia = ctk.CTkEntry(self.frameFormSEditarFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", text=self.textVarDireccion,  state=DISABLED)
            self.entradaDireccionSEditarFichaAuthCirugia.grid(row=4, column=3, padx=25, pady=15)

            var = tk.IntVar()
            var.set(1)

            if(operacion['autTutor'] == True):
                self.entradaAuthTutorSFichaAuthCirugia = ctk.CTkCheckBox(self.frameFormSEditarFichaAuthCirugia, fg_color="#0D1D29", border_width=2, border_color="black", variable=var, onvalue=1, text="", state=DISABLED)
            else:
                self.entradaAuthTutorSFichaAuthCirugia = ctk.CTkCheckBox(self.frameFormSEditarFichaAuthCirugia, fg_color="#0D1D29", border_width=2, border_color="black", variable=var, offvalue=0, state=DISABLED, text="")
            self.entradaAuthTutorSFichaAuthCirugia.grid(row=5, column=3, padx=25, pady=15)

            self.labelErrorDiagnosticoSEditarFichaAuthCirugia = ctk.CTkLabel(self.frameFormSEditarFichaAuthCirugia, text="Ingrese diagnostico en formato correcto (Solo letras)", text_font=Font_tuple, text_color="#c1121f")
            self.labelErrorCirugiaSEditarFichaAuthCirugia = ctk.CTkLabel(self.frameFormSEditarFichaAuthCirugia, text="Ingrese cirugia en formato correcto (Solo letras)", text_font=Font_tuple, text_color="#c1121f")

            #Agregar botones
            self.botonEditarSFichaAuthCirugia = ctk.CTkButton(self.frameButtonsSEditarFichaAuthCirugia, width= 250, height= 80, text='Editar Ficha', text_font=Font_tuple, hover_color="#142C3D", command=lambda: self.validarDatos(parent, mascotaActual, idFicha))
            self.botonEditarSFichaAuthCirugia.grid(row=0, column=0, padx= 10, pady = 40)
            self.botonVolverSFichaAuthCirugia = ctk.CTkButton(self.frameButtonsSEditarFichaAuthCirugia, width= 250, height= 80, text='Volver', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenFormularioEditarFicha, parent, container))
            self.botonVolverSFichaAuthCirugia.grid(row=0, column=1, padx= 10, pady = 40)

    def validarDatos(self, parent, mascotaActual, idFicha):
        
        flag = True
        diagnostico = self.entradaDiagnosticoSEditarFichaAuthCirugia.get("1.0",END)

        cirugia = self.entradaCirugiaARealizarSEditarFichaAuthCirugia.get()

        if(parent.filtroNoValidChar(diagnostico) is not True or (parent.filtroNum(diagnostico) is not False) or (len(diagnostico) < 6)):
            flag = False
            self.labelErrorDiagnosticoSEditarFichaAuthCirugia.place(x="210", y="367")
        else:
            self.labelErrorDiagnosticoSEditarFichaAuthCirugia.place_forget()

        if((parent.filtroNoValidChar(cirugia) is not True) or (parent.filtroNum(cirugia) is not False) or (len(cirugia) < 3)):
            flag = False
            self.labelErrorCirugiaSEditarFichaAuthCirugia.place(x="210", y="428")
        else:
            self.labelErrorCirugiaSEditarFichaAuthCirugia.place_forget()
        
        if(flag is True):
            self.editarFichaCirugia(mascotaActual, idFicha)

    def editarFichaCirugia(self, mascotaActual, idFicha):
        hoy = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        diagnostico = self.entradaDiagnosticoSEditarFichaAuthCirugia.get("1.0",END)
        cirugia = self.entradaCirugiaARealizarSEditarFichaAuthCirugia.get()
        check = self.entradaAuthTutorSFichaAuthCirugia.get()

        terminalVet.editarFichaOperacion(mascotaActual.getId(), idFicha, diagnostico, cirugia, hoy)
        self.labelMensajeEditadoFichaAuthCirugia.grid(row=0, column=0, padx=10, pady=10)
        #self.botonEditarSFichaAuthCirugia.configure(state=DISABLED)


class screenFormularioCrearFichaAuthCirugia(ctk.CTkFrame): 
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 12)
        Font_tuple16 = ("Helvetica", 16)
        
        
        mascotaActual:Mascota = parent.getMascotaApp()
        if(mascotaActual is not None):
            
            idFicha = mascotaActual.getidFichaActual()
            textoMascota = mascotaActual.getNombreMascota()
            self.labelTituloScreenSEditarFichaAuthCirugia = ctk.CTkLabel(self, text=f"Creación de ficha autorización cirugía, Mascota : {textoMascota}", text_font=Font_tuple16, text_color="black")
            self.labelTituloScreenSEditarFichaAuthCirugia.grid(row=0, column=0, padx=10, pady=10)

            self.frameFormSCrearFichaAuthCirugia = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameFormSCrearFichaAuthCirugia.grid(row=1, column=0, padx=20, pady=20)

            self.frameButtonsSCrearFichaAuthCirugia = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameButtonsSCrearFichaAuthCirugia.grid(row=2, column=0, padx=20, pady=20)

            self.frameText = ctk.CTkFrame(self.frameFormSCrearFichaAuthCirugia, corner_radius=0, fg_color="#4e5257")
            self.frameText.grid(row=6, column=1, padx=25, pady=15)

            self.labelNombrePacienteSCrearFichaAuthCirugia = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Nombre Paciente", text_font=Font_tuple, text_color="black")
            self.labelNombrePacienteSCrearFichaAuthCirugia.grid(row=0, column=0, padx=(20,5), pady=15)

            self.labelPesoSCrearFichaAuthCirugia = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Peso", text_font=Font_tuple, text_color="black")
            self.labelPesoSCrearFichaAuthCirugia.grid(row=1, column=0, padx=(20,5), pady=15)

            self.labelEspecieSCrearFichaAuthCirugia = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Especie", text_font=Font_tuple, text_color="black")
            self.labelEspecieSCrearFichaAuthCirugia.grid(row=2, column=0, padx=(20,5), pady=15)

            self.labelEdadSCrearFichaAuthCirugia = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Edad", text_font=Font_tuple, text_color="black")
            self.labelEdadSCrearFichaAuthCirugia.grid(row=3, column=0, padx=(20,5), pady=15)
            
            self.labelRazaSCrearFichaAuthCirugia = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Raza", text_font=Font_tuple, text_color="black")
            self.labelRazaSCrearFichaAuthCirugia.grid(row=4, column=0, padx=(20,5), pady=15)
            
            self.labelColorSCrearFichaAuthCirugia = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Color", text_font=Font_tuple, text_color="black")
            self.labelColorSCrearFichaAuthCirugia.grid(row=5, column=0, padx=(20,5), pady=15)
            
            self.labelDiagnosticoSCrearFichaAuthCirugia = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Diagnóstico", text_font=Font_tuple, text_color="black")
            self.labelDiagnosticoSCrearFichaAuthCirugia.grid(row=6, column=0, padx=(20,5), pady=15)
            
            self.labelCirugiaARealizarSCrearFichaAuthCirugia = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Cirugía a Realizar", text_font=Font_tuple, text_color="black")
            self.labelCirugiaARealizarSCrearFichaAuthCirugia.grid(row=0, column=2, padx=(20,5), pady=15)
            
            self.labelNombreDelTutorSCrearFichaAuthCirugia = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Nombre del Tutor", text_font=Font_tuple, text_color="black")
            self.labelNombreDelTutorSCrearFichaAuthCirugia.grid(row=1, column=2, padx=(20,5), pady=15)

            self.labelRutTutorSCrearFichaAuthCirugia = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Rut Tutor", text_font=Font_tuple, text_color="black")
            self.labelRutTutorSCrearFichaAuthCirugia.grid(row=2, column=2, padx=(20,5), pady=15)
            
            self.labelNumeroTelefonoSCrearFichaAuthCirugia = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Número de Teléfono", text_font=Font_tuple, text_color="black")
            self.labelNumeroTelefonoSCrearFichaAuthCirugia.grid(row=3, column=2, padx=(20,5), pady=15)

            self.labelDireccionSCrearFichaAuthCirugia = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Dirección", text_font=Font_tuple, text_color="black")
            self.labelDireccionSCrearFichaAuthCirugia.grid(row=4, column=2, padx=(20,5), pady=15)

            self.labelAuthTutorSCrearFichaAuthCirugia = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Autorizacion tutor", text_font=Font_tuple, text_color="black")
            self.labelAuthTutorSCrearFichaAuthCirugia.grid(row=5, column=2, padx=(20,5), pady=15)

            self.labelErrorCamposSCrearFichaAuthCirugia = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Error en el formato", text_font=Font_tuple, text_color="black")
            self.labelMensajeAgregadoSCrearFichaAuthCirugia = ctk.CTkLabel(self.frameButtonsSCrearFichaAuthCirugia, text="Ficha Agregada", text_font=Font_tuple, text_color="green")

            #Agregar Entrys
            self.textVarNombrePaciente = tk.StringVar()
            self.textVarEspecie = tk.StringVar()
            self.textVarNombreTutor = tk.StringVar()
            self.textVarRaza = tk.StringVar()
            self.textVarTelefono = tk.StringVar()
            self.textVarEdad = tk.StringVar()
            self.textVarPeso = tk.StringVar()
            self.textVarColor = tk.StringVar()
            self.textVarRut = tk.StringVar()
            self.textVarDireccion = tk.StringVar()
                
            self.textVarNombrePaciente.set(mascotaActual.getNombreMascota())
            self.entradaNombrePacienteSCrearFichaAuthCirugia = ctk.CTkEntry(self.frameFormSCrearFichaAuthCirugia, text = self.textVarNombrePaciente , width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaNombrePacienteSCrearFichaAuthCirugia.grid(row=0, column=1, padx=25, pady=15)

            self.textVarPeso.set(mascotaActual.getPeso(idFicha))
            self.entradaPesoSCrearFichaAuthCirugia = ctk.CTkEntry(self.frameFormSCrearFichaAuthCirugia,text = self.textVarPeso, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaPesoSCrearFichaAuthCirugia.grid(row=1, column=1, padx=25, pady=15)

            self.textVarEspecie.set(mascotaActual.getEspecie())
            self.entradaEspecieSCrearFichaAuthCirugia = ctk.CTkEntry(self.frameFormSCrearFichaAuthCirugia,text = self.textVarEspecie , width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaEspecieSCrearFichaAuthCirugia.grid(row=2, column=1, padx=25, pady=15)

            self.textVarEdad.set(mascotaActual.getEdad(idFicha))
            self.entradaEdadConsultaSCrearFichaAuthCirugia = ctk.CTkEntry(self.frameFormSCrearFichaAuthCirugia,text = self.textVarEdad,  width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaEdadConsultaSCrearFichaAuthCirugia.grid(row=3, column=1, padx=25, pady=15)
            
            self.textVarRaza.set(mascotaActual.getRaza())
            self.entradaRazaSCrearFichaAuthCirugia = ctk.CTkEntry(self.frameFormSCrearFichaAuthCirugia,text = self.textVarRaza,  width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaRazaSCrearFichaAuthCirugia.grid(row=4, column=1, padx=25, pady=15)

            self.textVarColor.set(mascotaActual.getColorMascota())
            self.entradaColorSCrearFichaAuthCirugia = ctk.CTkEntry(self.frameFormSCrearFichaAuthCirugia,text = self.textVarColor, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaColorSCrearFichaAuthCirugia.grid(row=5, column=1, padx=20, pady=15)

            self.entradaDiagnosticoSFichaAuthCirugia = tk.Text(self.frameText, width = 44, height= 3, background="#F0EFEB", font=("Helvetica", 12))
            self.entradaDiagnosticoSFichaAuthCirugia.grid(row=0, column=0, padx=2, pady=2)

            self.entradaCirugiaARealizarSCrearFichaAuthCirugia = ctk.CTkEntry(self.frameFormSCrearFichaAuthCirugia, width = 400, text_font=Font_tuple, text_color="black", fg_color="#F0EFEB")
            self.entradaCirugiaARealizarSCrearFichaAuthCirugia.grid(row=0, column=3, padx=25, pady=15)

            self.textVarNombreTutor.set(mascotaActual.getNombreTutor())
            self.entradaNombreTutorSCrearFichaAuthCirugia = ctk.CTkEntry(self.frameFormSCrearFichaAuthCirugia,text = self.textVarNombreTutor, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaNombreTutorSCrearFichaAuthCirugia.grid(row=1, column=3, padx=25, pady=15)

            self.textVarRut.set(mascotaActual.getRutTutor())
            self.entradaRutSCrearFichaAuthCirugia = ctk.CTkEntry(self.frameFormSCrearFichaAuthCirugia,text = self.textVarRut, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaRutSCrearFichaAuthCirugia.grid(row=2, column=3, padx=25, pady=15)

            self.textVarTelefono.set(mascotaActual.getNumeroTelefono())
            self.entradaNumTelefonoSCrearFichaAuthCirugia = ctk.CTkEntry(self.frameFormSCrearFichaAuthCirugia,text = self.textVarTelefono, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaNumTelefonoSCrearFichaAuthCirugia.grid(row=3, column=3, padx=25, pady=15)

            self.textVarDireccion.set(mascotaActual.getDireccion())
            self.entradaDireccionSCrearFichaAuthCirugia = ctk.CTkEntry(self.frameFormSCrearFichaAuthCirugia,text = self.textVarDireccion, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaDireccionSCrearFichaAuthCirugia.grid(row=4, column=3, padx=25, pady=15)

            self.entradaAuthTutorSCrearFichaAuthCirugia = ctk.CTkCheckBox(self.frameFormSCrearFichaAuthCirugia, text="", fg_color="#0D1D29", border_width=2, border_color="grey")
            self.entradaAuthTutorSCrearFichaAuthCirugia.grid(row=5, column=3, padx=25, pady=15)

            self.labelErrorDiagnostico = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Ingrese diagnostico en formato correcto (Solo letras)", text_font=Font_tuple, text_color="red")
            self.labelErrorCirugia = ctk.CTkLabel(self.frameFormSCrearFichaAuthCirugia, text="Ingrese cirugia en formato correcto (Solo letras)", text_font=Font_tuple, text_color="red")


            #Agregar botones
            flagEditar = parent.getFlagEditar()
            if(flagEditar is True):
                self.botonVolverSCrearFichaAuthCirugia = ctk.CTkButton(self.frameButtonsSCrearFichaAuthCirugia, width= 250, height= 80, text='Volver', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenFormularioEditarFicha, parent, container))
                self.botonVolverSCrearFichaAuthCirugia.grid(row=0, column=0, padx= 15, pady = 20)
            else:
                self.botonVolverSCrearFichaAuthCirugia = ctk.CTkButton(self.frameButtonsSCrearFichaAuthCirugia, width= 250, height= 80, text='Volver', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.show_frame(parent.screenFormularioCrearFicha))
                self.botonVolverSCrearFichaAuthCirugia.grid(row=0, column=0, padx= 15, pady = 20)

            self.botonAgregarFichaSCrearFichaAuthCirugia = ctk.CTkButton(self.frameButtonsSCrearFichaAuthCirugia, width= 250, height= 80, text='Agregar Ficha Operación', text_font=Font_tuple, hover_color="#142C3D", command=lambda: self.validarDatos(parent, mascotaActual))
            self.botonAgregarFichaSCrearFichaAuthCirugia.grid(row=0, column=1, padx= 15, pady = 20)
    
    def validarDatos(self, parent, mascotaActual):
        
        flag = True
        diagnostico = self.entradaDiagnosticoSFichaAuthCirugia.get("1.0",END)

        cirugia = self.entradaCirugiaARealizarSCrearFichaAuthCirugia.get()

        if(parent.filtroNoValidChar(diagnostico) is not True or (parent.filtroNum(diagnostico) is not False) or (len(diagnostico) < 6)):
            flag = False
            self.labelErrorDiagnostico.place(x="210", y="367")
        else:
            self.labelErrorDiagnostico.place_forget()

        if((parent.filtroNoValidChar(cirugia) is not True) or (parent.filtroNum(cirugia) is not False) or (len(cirugia) < 3)):
            flag = False
            self.labelErrorCirugia.place(x="210", y="428")
        else:
            self.labelErrorCirugia.place_forget()
        
        if(flag is True):
            self.agregarFichaCirugia(mascotaActual, parent)

    def agregarFichaCirugia(self, mascotaActual, parent):
        idFichahOp = uuid.uuid4()
        diagnostico = self.entradaDiagnosticoSFichaAuthCirugia.get("1.0",END)
        cirugia = self.entradaCirugiaARealizarSCrearFichaAuthCirugia.get()
        check = self.entradaAuthTutorSCrearFichaAuthCirugia.get()
        self.operacionFicha = { #al ser una ficha se guarda directamente en el tributo relerente al diccionario
            'id':idFichahOp,
            'diagnostico':diagnostico,
            'cirugiaARealizar':cirugia,
            'autTutor': check
        }
        parent.setFlagEditar(False) #indica que en este caso no se esta agregando en una ficha nueva, se esta gregando en una ficha de edicion
        terminalVet.agregarFichaOperacion(mascotaActual.getId(), self.operacionFicha)
        self.botonAgregarFichaSCrearFichaAuthCirugia.configure(state=DISABLED)
        self.labelMensajeAgregadoSCrearFichaAuthCirugia.grid(row=1, column=0, padx=10, pady=10)
        

class screenFormularioFichaHospt(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 12)
        Font_tuple16 = ("Helvetica", 16)
        mascotaActual:Mascota = parent.getMascotaApp()
        if(mascotaActual is not None):

            idFicha = mascotaActual.getidFichaActual()
            textoMascota = mascotaActual.getNombreMascota()
            self.labelTituloScreenSVerFichaHosp = ctk.CTkLabel(self, text=f"Visualización de ficha hospitalización, Mascota : {textoMascota}", text_font=Font_tuple16, text_color="black")
            self.labelTituloScreenSVerFichaHosp.grid(row=0, column=0, padx=10, pady=10)
            self.frameFormSVerFichaHosp = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameFormSVerFichaHosp.grid(row=1, column=0, padx=20, pady=10)

            self.frameButtonsSVerFichaHosp = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameButtonsSVerFichaHosp.grid(row=1, column=1, padx=20, pady=10)

            self.frameText1 = ctk.CTkFrame(self.frameFormSVerFichaHosp, corner_radius=0, fg_color="#4e5257")
            self.frameText1.grid(row=6, column=1, padx=20, pady=10)

            #Agregar Labels
            self.labelNombreMascotaSVerFichaHosp = ctk.CTkLabel(self.frameFormSVerFichaHosp, text="Nombre Mascota", text_font=Font_tuple, text_color="black")
            self.labelNombreMascotaSVerFichaHosp.grid(row=0, column=0, padx=20, pady=10)

            self.labelPesoSVerFichaHosp = ctk.CTkLabel(self.frameFormSVerFichaHosp, text="Peso", text_font=Font_tuple, text_color="black")
            self.labelPesoSVerFichaHosp.grid(row=1, column=0, padx=20, pady=10)

            self.labelEspecieSVerFichaHosp = ctk.CTkLabel(self.frameFormSVerFichaHosp, text="Especie ", text_font=Font_tuple, text_color="black")
            self.labelEspecieSVerFichaHosp.grid(row=2, column=0, padx=20, pady=10)

            self.labelEdadSVerFichaHosp = ctk.CTkLabel(self.frameFormSVerFichaHosp, text="Edad", text_font=Font_tuple, text_color="black")
            self.labelEdadSVerFichaHosp.grid(row=3, column=0, padx=20, pady=10)

            self.labelRazaSVerFichaHosp = ctk.CTkLabel(self.frameFormSVerFichaHosp, text="Raza", text_font=Font_tuple, text_color="black")
            self.labelRazaSVerFichaHosp.grid(row=4, column=0, padx=20, pady=10)

            self.labelColorSVerFichaHosp = ctk.CTkLabel(self.frameFormSVerFichaHosp, text="Color", text_font=Font_tuple, text_color="black")
            self.labelColorSVerFichaHosp.grid(row=5, column=0, padx=20, pady=10)

            self.labelMotivoHospSVerFichaHosp = ctk.CTkLabel(self.frameFormSVerFichaHosp, text="Motivo de Hospitalización", text_font=Font_tuple, text_color="black")
            self.labelMotivoHospSVerFichaHosp.grid(row=6, column=0, padx=20, pady=10) 

            self.labelMensajeAgregarSVerFichaHosp = ctk.CTkLabel(self.frameButtonsSVerFichaHosp, text="Ficha Agregada", text_font=Font_tuple, text_color="green")


            #Agregar Entrys
            self.textVarNombrePaciente = tk.StringVar()
            self.textVarPeso = tk.StringVar()
            self.textVarEspecie = tk.StringVar()
            self.textVarEdad = tk.StringVar()
            self.textVarRaza = tk.StringVar()
            self.textVarColor = tk.StringVar()

            self.textVarNombrePaciente.set(mascotaActual.getNombreMascota())
            self.entradaNombrePacienteSVerFichaHosp = ctk.CTkEntry(self.frameFormSVerFichaHosp, width = 400, text=self.textVarNombrePaciente, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaNombrePacienteSVerFichaHosp.grid(row=0, column=1, padx=20, pady=10)

            self.textVarPeso.set(mascotaActual.getPeso(idFicha))
            self.entradaPesoSVerFichaHosp = ctk.CTkEntry(self.frameFormSVerFichaHosp, width = 400, text=self.textVarPeso, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaPesoSVerFichaHosp.grid(row=1, column=1, padx=20, pady=10)

            self.textVarEspecie.set(mascotaActual.getEspecie())
            self.entradaEspecieSVerFichaHosp = ctk.CTkEntry(self.frameFormSVerFichaHosp, width = 400, text=self.textVarEspecie, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaEspecieSVerFichaHosp.grid(row=2, column=1, padx=20, pady=10)

            self.textVarEdad.set(mascotaActual.getEdad(idFicha))
            self.entradaEdadSVerFichaHosp = ctk.CTkEntry(self.frameFormSVerFichaHosp, width = 400, text=self.textVarEdad, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaEdadSVerFichaHosp.grid(row=3, column=1, padx=20, pady=10)


            self.textVarRaza.set(mascotaActual.getRaza())
            self.entradaRazaSVerFichaHosp = ctk.CTkEntry(self.frameFormSVerFichaHosp, width = 400, text=self.textVarRaza, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaRazaSVerFichaHosp.grid(row=4, column=1, padx=20, pady=10)


            self.textVarColor.set(mascotaActual.getColorMascota())
            self.entradaColorSVerFichaHosp = ctk.CTkEntry(self.frameFormSVerFichaHosp, width = 400, text=self.textVarColor, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaColorSVerFichaHosp.grid(row=5, column=1, padx=20, pady=10)

            if(mascotaActual.getHospitalizacion(idFicha) == True):
                motivoHosp = mascotaActual.getHospitalizacionFicha(idFicha)

                self.entradaMotivoHospSVerFichaHosp = tk.Text(self.frameText1, width = 40, height=6, font=("Helvetica", "12"), background="#F0EFEB")
                self.entradaMotivoHospSVerFichaHosp.delete(1.0, END)
                self.entradaMotivoHospSVerFichaHosp.grid(row=0, column=0, padx=2, pady=2)
                self.entradaMotivoHospSVerFichaHosp.insert(END, motivoHosp["motivo"])
                self.entradaMotivoHospSVerFichaHosp.configure(state="disabled")


            #Agregar buttons
            self.botonVolverSVerFichaHosp = ctk.CTkButton(self.frameButtonsSVerFichaHosp, width=200, height=120, text='Volver', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenFormularioVerFicha, parent, container))
            self.botonVolverSVerFichaHosp.pack(padx= 10, pady = 40)


class screenFormularioCrearFichaHospt(ctk.CTkFrame): #Hospitalización
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 12)
        Font_tuple10 = ("Helvetica", 10)
        Font_tuple16 = ("Helvetica", 16)

        mascotaActual:Mascota = parent.getMascotaApp()
        if(mascotaActual is not None):
            
            idFicha = mascotaActual.getidFichaActual()
            textoMascota = mascotaActual.getNombreMascota()
            self.labelTituloScreenSCrearFichaHosp = ctk.CTkLabel(self, text=f"Creación de ficha hospitalización, Mascota : {textoMascota}", text_font=Font_tuple16, text_color="black")
            self.labelTituloScreenSCrearFichaHosp.grid(row=0, column=0, padx=10, pady=10)

            self.frameFormSCrearFichaHosp = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameFormSCrearFichaHosp.grid(row=1, column=0, padx=20, pady=10)

            self.frameButtonsSCrearFichaHosp = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameButtonsSCrearFichaHosp.grid(row=1, column=1, padx=20, pady=10)

            self.frameText1 = ctk.CTkFrame(self.frameFormSCrearFichaHosp, corner_radius=0, fg_color="#4e5257")
            self.frameText1.grid(row=6, column=1, padx=20, pady=10)

            #Agregar Labels
            self.labelNombreMascotaSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Nombre Mascota", text_font=Font_tuple, text_color="black")
            self.labelNombreMascotaSCrearFichaHosp.grid(row=0, column=0, padx=20, pady=15)

            self.labelEspecieSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Especie ", text_font=Font_tuple, text_color="black")
            self.labelEspecieSCrearFichaHosp.grid(row=1, column=0, padx=20, pady=15)

            self.labelPesoSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Peso", text_font=Font_tuple, text_color="black")
            self.labelPesoSCrearFichaHosp.grid(row=2, column=0, padx=20, pady=15)

            self.labelEdadSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Edad", text_font=Font_tuple, text_color="black")
            self.labelEdadSCrearFichaHosp.grid(row=3, column=0, padx=20, pady=15)

            self.labelRazaSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Raza", text_font=Font_tuple, text_color="black")
            self.labelRazaSCrearFichaHosp.grid(row=4, column=0, padx=20, pady=15)

            self.labelColorSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Color", text_font=Font_tuple, text_color="black")
            self.labelColorSCrearFichaHosp.grid(row=5, column=0, padx=20, pady=15)

            self.labelMotivoHospSCrearFichaHosp = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Motivo de Hospitalización", text_font=Font_tuple, text_color="black")
            self.labelMotivoHospSCrearFichaHosp.grid(row=6, column=0, padx=20, pady=15)

            self.labelMensajeAgregadoSCrearFichaHosp = ctk.CTkLabel(self.frameButtonsSCrearFichaHosp, text="Ficha agregada", text_font=Font_tuple, text_color="green")

            #Agregar Entrys

            self.textVarNombrePaciente = tk.StringVar()
            self.textVarPeso = tk.StringVar()
            self.textVarEspecie = tk.StringVar()
            self.textVarEdad = tk.StringVar()
            self.textVarRaza = tk.StringVar()
            self.textVarColor = tk.StringVar()

            self.textVarNombrePaciente.set(mascotaActual.getNombreMascota())
            self.entradaNombrePacienteSCrearFichaHosp = ctk.CTkEntry(self.frameFormSCrearFichaHosp, text=self.textVarNombrePaciente , width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaNombrePacienteSCrearFichaHosp.grid(row=0, column=1, padx=20, pady=15)

            self.textVarEspecie.set(mascotaActual.getEspecie())
            self.entradaEspecieSCrearFichaHosp = ctk.CTkEntry(self.frameFormSCrearFichaHosp,text=self.textVarEspecie, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaEspecieSCrearFichaHosp.grid(row=2, column=1, padx=20, pady=15)

            self.textVarPeso.set(mascotaActual.getPeso(idFicha))
            self.entradaPesoSCrearFichaHosp = ctk.CTkEntry(self.frameFormSCrearFichaHosp,text=self.textVarPeso,  width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaPesoSCrearFichaHosp.grid(row=1, column=1, padx=20, pady=15)

            self.textVarEdad.set(mascotaActual.getEdad(idFicha))
            self.entradaEdadSCrearFichaHosp = ctk.CTkEntry(self.frameFormSCrearFichaHosp,text=self.textVarEdad, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaEdadSCrearFichaHosp.grid(row=3, column=1, padx=20, pady=15)

            self.textVarRaza.set(mascotaActual.getRaza())
            self.entradaRazaSCrearFichaHosp = ctk.CTkEntry(self.frameFormSCrearFichaHosp,text=self.textVarRaza, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaRazaSCrearFichaHosp.grid(row=4, column=1, padx=20, pady=15)

            self.textVarColor.set(mascotaActual.getColorMascota())
            self.entradaColorSCrearFichaHosp = ctk.CTkEntry(self.frameFormSCrearFichaHosp,text=self.textVarColor, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaColorSCrearFichaHosp.grid(row=5, column=1, padx=20, pady=15)

            self.entradaMotivoHospSCrearFichaHosp = tk.Text(self.frameText1, width = 40, height=6, font=("Helvetica", "12"), background="#F0EFEB")
            self.entradaMotivoHospSCrearFichaHosp.grid(row=0, column=0, padx=2, pady=2)
            
            self.labelErrorMotivo = ctk.CTkLabel(self.frameFormSCrearFichaHosp, text="Ingrese motivo en formato correcto (Solo letras)", text_font=Font_tuple, text_color="#c1121f")

            #Agregar buttons
            flagEditar = parent.getFlagEditar()
            if(flagEditar is True):
                self.botonVolverSCrearFichaHosp = ctk.CTkButton(self.frameButtonsSCrearFichaHosp, width=200, height=120, text='Volver', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenFormularioEditarFicha, parent, container))
                self.botonVolverSCrearFichaHosp.pack(padx= 10, pady = 40)
            else:
                self.botonVolverSCrearFichaHosp = ctk.CTkButton(self.frameButtonsSCrearFichaHosp, width=200, height=120, text='Volver', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.show_frame(parent.screenFormularioCrearFicha))
                self.botonVolverSCrearFichaHosp.pack(padx= 10, pady = 40)
            
            self.botonAgregarFichaHosp = ctk.CTkButton(self.frameButtonsSCrearFichaHosp, width=250, height=120, text='Agregar Ficha \nHospitalización', text_font=Font_tuple, hover_color="#142C3D", command=lambda: self.validarDatos(parent, mascotaActual))
            self.botonAgregarFichaHosp.pack(padx= 10, pady = 40)

    def validarDatos(self, parent, mascotaActual):
        
        flag = True
        motivo = self.entradaMotivoHospSCrearFichaHosp.get("1.0", END)

        if(parent.filtroNoValidChar(motivo) is not True or (parent.filtroNum(motivo) is not False) or (len(motivo) < 6)):
            flag = False
            self.labelErrorMotivo.place(x="270", y="481")
        else:
            self.labelErrorMotivo.place_forget()

        if(flag is True):
            self.agregarFichaHosp(mascotaActual, parent)


    def agregarFichaHosp(self, mascotaActual, parent):
        motivo = self.entradaMotivoHospSCrearFichaHosp.get("1.0", END)
        idFichahHosp = uuid.uuid4()
        hospDicc = {
            'id':idFichahHosp,
            'motivo':motivo
        }
        parent.setFlagEditar(False)
        terminalVet.agregarFichaHospitalizacion(mascotaActual.getId(), hospDicc)
        self.botonAgregarFichaHosp.configure(state=DISABLED)
        self.labelMensajeAgregadoSCrearFichaHosp.pack()


class screenFormularioEditarFichaHospt(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 12)
        Font_tuple16 = ("Helvetica", 16)
        mascotaActual:Mascota = parent.getMascotaApp()
        if(mascotaActual is not None):

            idFicha = mascotaActual.getidFichaActual()
            textoMascota = mascotaActual.getNombreMascota()
            self.labelTituloScreenSEditarFichaHosp = ctk.CTkLabel(self, text=f"Edición de ficha hospitalización, Mascota : {textoMascota}", text_font=Font_tuple16, text_color="black")
            self.labelTituloScreenSEditarFichaHosp.grid(row=0, column=0, padx=10, pady=10)
            self.frameFormSEditarFichaHosp = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameFormSEditarFichaHosp.grid(row=1, column=0, padx=20, pady=10)

            self.frameButtonsSEditarFichaHosp = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameButtonsSEditarFichaHosp.grid(row=1, column=1, padx=20, pady=10)

            self.frameText1 = ctk.CTkFrame(self.frameFormSEditarFichaHosp, corner_radius=0, fg_color="#4e5257")
            self.frameText1.grid(row=6, column=1, padx=20, pady=(17,30))

            #Agregar Labels
            self.labelNombreMascotaSEditarFichaHosp = ctk.CTkLabel(self.frameFormSEditarFichaHosp, text="Nombre Mascota", text_font=Font_tuple, text_color="black")
            self.labelNombreMascotaSEditarFichaHosp.grid(row=0, column=0, padx=20, pady=15)

            self.labelPesoSEditarFichaHosp = ctk.CTkLabel(self.frameFormSEditarFichaHosp, text="Peso", text_font=Font_tuple, text_color="black")
            self.labelPesoSEditarFichaHosp.grid(row=1, column=0, padx=20, pady=15)

            self.labelEspecieSEditarFichaHosp = ctk.CTkLabel(self.frameFormSEditarFichaHosp, text="Especie ", text_font=Font_tuple, text_color="black")
            self.labelEspecieSEditarFichaHosp.grid(row=2, column=0, padx=20, pady=15)

            self.labelEdadSEditarFichaHosp = ctk.CTkLabel(self.frameFormSEditarFichaHosp, text="Edad", text_font=Font_tuple, text_color="black")
            self.labelEdadSEditarFichaHosp.grid(row=3, column=0, padx=20, pady=15)

            self.labelRazaSEditarFichaHosp = ctk.CTkLabel(self.frameFormSEditarFichaHosp, text="Raza", text_font=Font_tuple, text_color="black")
            self.labelRazaSEditarFichaHosp.grid(row=4, column=0, padx=20, pady=15)

            self.labelColorSEditarFichaHosp = ctk.CTkLabel(self.frameFormSEditarFichaHosp, text="Color", text_font=Font_tuple, text_color="black")
            self.labelColorSEditarFichaHosp.grid(row=5, column=0, padx=20, pady=15)

            self.labelMotivoHospSEditarFichaHosp = ctk.CTkLabel(self.frameFormSEditarFichaHosp, text="Motivo de Hospitalización", text_font=Font_tuple, text_color="black")
            self.labelMotivoHospSEditarFichaHosp.grid(row=6, column=0, padx=20, pady=15)

            self.labelMensajeAgregarSEditarFichaHosp = ctk.CTkLabel(self.frameButtonsSEditarFichaHosp, text="Ficha Agregada", text_font=Font_tuple, text_color="green")


            #Agregar Entrys
            self.textVarNombrePaciente = tk.StringVar()
            self.textVarPeso = tk.StringVar()
            self.textVarEspecie = tk.StringVar()
            self.textVarEdad = tk.StringVar()
            self.textVarRaza = tk.StringVar()
            self.textVarColor = tk.StringVar()

            self.textVarNombrePaciente.set(mascotaActual.getNombreMascota())
            self.entradaNombrePacienteSEditarFichaHosp = ctk.CTkEntry(self.frameFormSEditarFichaHosp, width = 400, text=self.textVarNombrePaciente, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaNombrePacienteSEditarFichaHosp.grid(row=0, column=1, padx=20, pady=15)

            self.textVarPeso.set(mascotaActual.getPeso(idFicha))
            self.entradaPesoSEditarFichaHosp = ctk.CTkEntry(self.frameFormSEditarFichaHosp, width = 400, text=self.textVarPeso, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaPesoSEditarFichaHosp.grid(row=1, column=1, padx=20, pady=15)

            self.textVarEspecie.set(mascotaActual.getEspecie())
            self.entradaEspecieSEditarFichaHosp = ctk.CTkEntry(self.frameFormSEditarFichaHosp, width = 400, text=self.textVarEspecie, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaEspecieSEditarFichaHosp.grid(row=2, column=1, padx=20, pady=15)

            self.textVarEdad.set(mascotaActual.getEdad(idFicha))
            self.entradaEdadSEditarFichaHosp = ctk.CTkEntry(self.frameFormSEditarFichaHosp, width = 400, text=self.textVarEdad, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaEdadSEditarFichaHosp.grid(row=3, column=1, padx=20, pady=15)


            self.textVarRaza.set(mascotaActual.getRaza())
            self.entradaRazaSEditarFichaHosp = ctk.CTkEntry(self.frameFormSEditarFichaHosp, width = 400, text=self.textVarRaza, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaRazaSEditarFichaHosp.grid(row=4, column=1, padx=20, pady=15)


            self.textVarColor.set(mascotaActual.getColorMascota())
            self.entradaColorSEditarFichaHosp = ctk.CTkEntry(self.frameFormSEditarFichaHosp, width = 400, text=self.textVarColor, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaColorSEditarFichaHosp.grid(row=5, column=1, padx=20, pady=15)

            if(mascotaActual.getHospitalizacion(idFicha) == True):
                motivoHosp = mascotaActual.getHospitalizacionFicha(idFicha)

                self.entradaMotivoHospSEditarFichaHosp = tk.Text(self.frameText1, width = 40, height=6, font=("Helvetica", "12"), background="#F0EFEB", borderwidth=0)
                self.entradaMotivoHospSEditarFichaHosp.delete(1.0, END)
                self.entradaMotivoHospSEditarFichaHosp.grid(row=0, column=0, padx=2, pady=2)
                self.entradaMotivoHospSEditarFichaHosp.insert(END, motivoHosp["motivo"])

            self.labelErrorMotivo = ctk.CTkLabel(self.frameFormSEditarFichaHosp, text="Ingrese motivo en formato correcto (Solo letras)", text_font=Font_tuple, text_color="#c1121f")
            #Agregar buttons
            self.botonEditarSRditarFichaHosp = ctk.CTkButton(self.frameButtonsSEditarFichaHosp, width=200, height=120, text='Editar ficha', text_font=Font_tuple, hover_color="#142C3D", command=lambda: self.validarDatos(parent, mascotaActual, idFicha))
            self.botonEditarSRditarFichaHosp.pack(padx= 10, pady = 40)
            
            self.botonVolverSEditarFichaHosp = ctk.CTkButton(self.frameButtonsSEditarFichaHosp, width=200, height=120, text='Volver', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenFormularioEditarFicha, parent, container))
            self.botonVolverSEditarFichaHosp.pack(padx= 10, pady = 40)

    def validarDatos(self, parent, mascotaActual, idFicha):
        
        flag = True
        motivo = self.entradaMotivoHospSEditarFichaHosp.get("1.0", END)

        if(parent.filtroNoValidChar(motivo) is not True or (parent.filtroNum(motivo) is not False) or (len(motivo) < 6)):
            flag = False
            self.labelErrorMotivo.place(x="270", y="481")
        else:
           self.labelErrorMotivo.place_forget()

        if(flag is True):
            self.editarFichaHosp(parent, mascotaActual, idFicha)


    def editarFichaHosp(self, parent, mascotaActual, idFicha):
        # motivo = self.entradaDiagnosticoSEditarFichaHosp.get("1.0", END)
        motivo = self.entradaMotivoHospSEditarFichaHosp.get("1.0", END)
        hoy = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.labelMensajeAgregarSEditarFichaHosp.pack()
        #self.botonEditarSRditarFichaHosp.configure(state=DISABLED)
        terminalVet.editarFichaHospitalizacion(mascotaActual.getId(), idFicha, motivo, hoy)

        # terminalVet.editarFichaHospitalizacion(mascotaActual.getId(), hospDicc)
        # self.labelMensajeAgregadoSCrearFichaHosp.pack()



class screenFormularioFichaSedacion(ctk.CTkFrame): #Muestra datos cambiados
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 12)
        Font_tuple10 = ("Helvetica", 10)
        Font_tuple16 = ("Helvetica", 16)
        mascotaActual:Mascota = parent.getMascotaApp()
        if(mascotaActual is not None):

            idFicha = mascotaActual.getidFichaActual()
            textoMascota = mascotaActual.getNombreMascota()
            self.labelTituloScreenSVerFichaSedacion = ctk.CTkLabel(self, text=f"Visualización de ficha sedación, Mascota : {textoMascota}", text_font=Font_tuple16, text_color="black")
            self.labelTituloScreenSVerFichaSedacion.grid(row=0, column=0, padx=10, pady=10)
            self.frameFormSVerFichaSedacion = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameFormSVerFichaSedacion.grid(row=1, column=0, padx=20, pady=10)

            self.frameButtonsSVerFichaSedacion = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameButtonsSVerFichaSedacion.grid(row=1, column=1, padx=20, pady=10)

            self.labelNombrePacienteSVerFichaSedacion = ctk.CTkLabel( self.frameFormSVerFichaSedacion, text="Nombre Paciente", text_font=Font_tuple, text_color="black")
            self.labelNombrePacienteSVerFichaSedacion.grid(row=0, column=0, padx=20, pady=10)

            self.labelEspecieSVerFichaSedacion = ctk.CTkLabel( self.frameFormSVerFichaSedacion, text="Especie", text_font=Font_tuple, text_color="black")
            self.labelEspecieSVerFichaSedacion.grid(row=1, column=0, padx=20, pady=10)

            self.labelRazaSVerFichaSedacion = ctk.CTkLabel( self.frameFormSVerFichaSedacion, text="Raza", text_font=Font_tuple, text_color="black")
            self.labelRazaSVerFichaSedacion.grid(row=2, column=0, padx=20, pady=10)
            
            self.labelNombreTutorSVerFichaSedacion = ctk.CTkLabel( self.frameFormSVerFichaSedacion, text="Nombre tutor", text_font=Font_tuple, text_color="black")
            self.labelNombreTutorSVerFichaSedacion.grid(row=3, column=0, padx=20, pady=10)

            self.labelRutTutorSVerFichaSedacion = ctk.CTkLabel( self.frameFormSVerFichaSedacion, text="Rut", text_font=Font_tuple, text_color="black")
            self.labelRutTutorSVerFichaSedacion.grid(row=4, column=0, padx=20, pady=10)
            
            self.labelNumeroTelefonoSVerFichaSedacion = ctk.CTkLabel( self.frameFormSVerFichaSedacion, text="Número de Teléfono", text_font=Font_tuple, text_color="black")
            self.labelNumeroTelefonoSVerFichaSedacion.grid(row=5, column=0, padx=20, pady=10)

            self.labelDireccionSVerFichaSedacion = ctk.CTkLabel( self.frameFormSVerFichaSedacion, text="Dirección", text_font=Font_tuple, text_color="black")
            self.labelDireccionSVerFichaSedacion.grid(row=6, column=0, padx=20, pady=10)

            self.labelauthTutorSVerFichaSedacion = ctk.CTkLabel( self.frameFormSVerFichaSedacion, text="Autorización Tutor", text_font=Font_tuple, text_color="black")
            self.labelauthTutorSVerFichaSedacion.grid(row=7, column=0, padx=20, pady=10)

            #Agregar Entrys
            self.textVarNombrePaciente = tk.StringVar()
            self.textVarEspecie = tk.StringVar()
            self.textVarRaza = tk.StringVar()
            self.textVarNombreTutor = tk.StringVar()
            self.textVarRut = tk.StringVar()
            self.textVarTelefono = tk.StringVar()
            self.textVarDireccion = tk.StringVar()

            self.textVarNombrePaciente.set(mascotaActual.getNombreMascota())
            self.entradaNombrePacienteSVerFichaSedacion = ctk.CTkEntry( self.frameFormSVerFichaSedacion, width = 400, text=self.textVarNombrePaciente, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaNombrePacienteSVerFichaSedacion.grid(row=0, column=1, padx=20, pady=10)

            self.textVarEspecie.set(mascotaActual.getEspecie())
            self.entradaEspecieSVerFichaSedacion = ctk.CTkEntry( self.frameFormSVerFichaSedacion, width = 400, text=self.textVarEspecie, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaEspecieSVerFichaSedacion.grid(row=1, column=1, padx=20, pady=10)

            self.textVarRaza.set(mascotaActual.getRaza())
            self.entradaRazaSVerFichaSedacion = ctk.CTkEntry( self.frameFormSVerFichaSedacion, width = 400, text=self.textVarRaza, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaRazaSVerFichaSedacion.grid(row=2, column=1, padx=20, pady=10)

            self.textVarNombreTutor.set(mascotaActual.getNombreTutor())
            self.entradaNombreTutorSVerFichaSedacion = ctk.CTkEntry( self.frameFormSVerFichaSedacion, width = 400, text=self.textVarNombreTutor, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaNombreTutorSVerFichaSedacion.grid(row=3, column=1, padx=20, pady=10)

            self.textVarRut.set(mascotaActual.getRutTutor())
            self.entradaRutTutorSVerFichaSedacion = ctk.CTkEntry( self.frameFormSVerFichaSedacion, width = 400, text=self.textVarRut, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaRutTutorSVerFichaSedacion.grid(row=4, column=1, padx=20, pady=10)

            self.textVarTelefono.set(mascotaActual.getNumeroTelefono())
            self.entradaNumTelefonoSVerFichaSedacion = ctk.CTkEntry( self.frameFormSVerFichaSedacion, width = 400, text=self.textVarTelefono, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaNumTelefonoSVerFichaSedacion.grid(row=5, column=1, padx=20, pady=10)

            self.textVarDireccion.set(mascotaActual.getDireccion())
            self.entradaDireccionSVerFichaSedacion = ctk.CTkEntry( self.frameFormSVerFichaSedacion, width = 400, text=self.textVarDireccion, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaDireccionSVerFichaSedacion.grid(row=6, column=1, padx=20, pady=10)
            
            var = tk.IntVar()
            var.set(1)

            if(mascotaActual.getSedacion(idFicha)):
                sedacion = mascotaActual.getSedacioFicha(idFicha)

                if(sedacion["autorizacion"] == True):
                    self.entradaAuthTutorSVerFichaSedacion = ctk.CTkCheckBox(self.frameFormSVerFichaSedacion, text="", variable=var, onvalue=1, fg_color="#0D1D29", border_width=2, border_color="grey", state=DISABLED)
                else:
                    self.entradaAuthTutorSVerFichaSedacion = ctk.CTkCheckBox(self.frameFormSVerFichaSedacion, text="", variable=var, onvalue=0, fg_color="#0D1D29", border_width=2, border_color="grey", state=DISABLED)
                self.entradaAuthTutorSVerFichaSedacion.grid(row=7, column=1, padx=20, pady=10)

            #Agregar buttons
            self.botonVolverSVerFichaSedacion = ctk.CTkButton(self.frameButtonsSVerFichaSedacion, width= 200, height= 120,text='Volver', text_font=Font_tuple10, hover_color="#142C3D", command=lambda: parent.show_frame(parent.screenFormularioVerFicha))
            self.botonVolverSVerFichaSedacion.pack(padx= 10, pady = 40)
            

class screenFormularioCrearFichaSedacion(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple = ("Helvetica", 12)
        Font_tuple10 = ("Helvetica", 10)
        Font_tuple16 = ("Helvetica", 16)
        
        mascotaActual:Mascota = parent.getMascotaApp()
        if(mascotaActual is not None):
            
            idFicha = mascotaActual.getidFichaActual()
            textoMascota = mascotaActual.getNombreMascota()
            self.labelTituloScreenSCrearFichaSedacion = ctk.CTkLabel(self, text=f"Creación de ficha sedación, Mascota : {textoMascota}", text_font=Font_tuple16, text_color="black")
            self.labelTituloScreenSCrearFichaSedacion.grid(row=0, column=0, padx=10, pady=10)

            self.frameFormSCrearFichaSedacion = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameFormSCrearFichaSedacion.grid(row=1, column=0, padx=20, pady=10)
                
            self.frameButtonsSCrearFichaSedacion = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameButtonsSCrearFichaSedacion.grid(row=1, column=1, padx=20, pady=10)

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
            
            self.labelMensajeAgregarSCrearFichaSedacion = ctk.CTkLabel(self.frameButtonsSCrearFichaSedacion, text="Ficha Agregada", text_font=Font_tuple, text_color="green")

            #Agregar Entrys
            self.textVarNombrePaciente = tk.StringVar()
            self.textVarRut = tk.StringVar()
            self.textVarEspecie = tk.StringVar()
            self.textVarNombreTutor = tk.StringVar()
            self.textVarRaza = tk.StringVar()
            self.textVarTelefono = tk.StringVar()
            self.textVarDireccion = tk.StringVar()            

            self.textVarNombrePaciente.set(mascotaActual.getNombreMascota())
            self.entradaNombrePacienteSCrearFichaSedacion = ctk.CTkEntry( self.frameFormSCrearFichaSedacion, text = self.textVarNombrePaciente, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaNombrePacienteSCrearFichaSedacion.grid(row=0, column=1, padx=20, pady=10)

            self.textVarEspecie.set(mascotaActual.getEspecie())#####
            self.entradaEspecieSCrearFichaSedacion = ctk.CTkEntry( self.frameFormSCrearFichaSedacion, text = self.textVarEspecie, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaEspecieSCrearFichaSedacion.grid(row=1, column=1, padx=20, pady=10)

            self.textVarNombreTutor.set(mascotaActual.getNombreTutor())
            self.entradaNombreTutorSCrearFichaSedacion = ctk.CTkEntry( self.frameFormSCrearFichaSedacion, text = self.textVarNombreTutor, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaNombreTutorSCrearFichaSedacion.grid(row=2, column=1, padx=20, pady=10)

            self.textVarRut.set(mascotaActual.getRutTutor())
            self.entradaRutTutorSCrearFichaSedacion = ctk.CTkEntry( self.frameFormSCrearFichaSedacion, text = self.textVarRut, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaRutTutorSCrearFichaSedacion.grid(row=3, column=1, padx=20, pady=10)

            self.textVarRaza.set(mascotaActual.getRaza())
            self.entradaRazaSCrearFichaSedacion = ctk.CTkEntry( self.frameFormSCrearFichaSedacion, text = self.textVarRaza, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaRazaSCrearFichaSedacion.grid(row=4, column=1, padx=20, pady=10)

            self.textVarTelefono.set(mascotaActual.getNumeroTelefono())
            self.entradaNumTelefonoSCrearFichaSedacion = ctk.CTkEntry( self.frameFormSCrearFichaSedacion, text = self.textVarTelefono, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaNumTelefonoSCrearFichaSedacion.grid(row=5, column=1, padx=20, pady=10)

            self.textVarDireccion.set(mascotaActual.getDireccion())
            self.entradaDireccionSCrearFichaSedacion = ctk.CTkEntry( self.frameFormSCrearFichaSedacion, text = self.textVarDireccion, width = 400, text_font=Font_tuple, text_color="grey", fg_color="#F0EFEB", state=DISABLED)
            self.entradaDireccionSCrearFichaSedacion.grid(row=6, column=1, padx=20, pady=10)
            
            self.entradaAuthTutorSCrearFichaSedacion = ctk.CTkCheckBox(self.frameFormSCrearFichaSedacion, text="", fg_color="#0D1D29", border_width=2, border_color="grey")
            self.entradaAuthTutorSCrearFichaSedacion.grid(row=7, column=1, padx=20, pady=10)

            #Agregar buttons
            flagEditar = parent.getFlagEditar()
            if(flagEditar is True):
                self.botonVolverSCrearFichaSedacion = ctk.CTkButton(self.frameButtonsSCrearFichaSedacion, width= 200, height= 120,text='Volver', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.update_frame(parent.screenFormularioEditarFicha, parent, container))
                self.botonVolverSCrearFichaSedacion.pack(padx= 10, pady = 40)
            else:
                self.botonVolverSCrearFichaSedacion = ctk.CTkButton(self.frameButtonsSCrearFichaSedacion, width= 200, height= 120,text='Volver', text_font=Font_tuple, hover_color="#142C3D", command=lambda: parent.show_frame(parent.screenFormularioCrearFicha))
                self.botonVolverSCrearFichaSedacion.pack(padx= 10, pady = 40)
            
            self.botonAgregarFichaSedacion = ctk.CTkButton(self.frameButtonsSCrearFichaSedacion, width= 200, height= 120,text='Agregar Ficha Hospitalización', text_font=Font_tuple, hover_color="#142C3D", command=lambda:self.agregarFichaSed(mascotaActual,self.entradaAuthTutorSCrearFichaSedacion.get(), parent))
            self.botonAgregarFichaSedacion.pack(padx= 10, pady = 40)
        
    def agregarFichaSed(self, mascota, check, parent):
        idFichahSedacion = uuid.uuid4()
        sedacionDicc = {
            'id':idFichahSedacion,
            'autorizacion':check
        }
        terminalVet.agregarFichaSedacion(mascota.getId(), sedacionDicc)
        parent.setFlagEditar(False)
        self.botonAgregarFichaSedacion.configure(state=DISABLED)
        self.labelMensajeAgregarSCrearFichaSedacion.pack()
    
class screenCalendarioVacunacion(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")
        Font_tuple20 = ("Helvetica", 20)
        Font_tuple14 = ("Helvetica", 16)
        Font_tuple12 = ("Helvetica", 12)

        if(terminalVet.getIdCalendario() is not None):

            self.frameBotonesCalendario = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameBotonesCalendario.grid(row=0, column=0, padx=20, pady=20)

            self.frameIngresoDeDatos = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameIngresoDeDatos.grid(row=0, column=1, padx=20, pady=20)

            self.labelTitle = ctk.CTkLabel(self.frameBotonesCalendario, text="Calendario de vacunación MyPetRecord", text_font=Font_tuple20, text_color='black')
            self.labelTitle.grid(row=0, column=0, padx=(50,50), pady=10)

            self.labelSubTitle = ctk.CTkLabel(self.frameIngresoDeDatos, text="Nombre Veterinaria", text_font=Font_tuple20, text_color='black')
            self.labelSubTitle.grid(row=0, column=0, padx=(50,50), pady=10)

            self.calendario = Calendar(self.frameBotonesCalendario, selectmode='day',date_pattern='dd/mm/yyyy',  year=today.year, month=today.month, day=today.day)
            self.calendario.grid(row=3, column=0, padx=(50,50), pady=10)
        
            self.indicarFechasEnCalendarioPostCargaBaseDeDatos(parent)

            self.ingresarCita = ctk.CTkButton(self.frameIngresoDeDatos, width=20, text='Ingresar cita', command=lambda: self.ingresarCitaFuncion())
            self.ingresarCita.grid(row=4, column=0, padx=10 , pady=10)

            self.botonEditar = ctk.CTkButton(self.frameIngresoDeDatos, width= 20, text='Editar cita', command=lambda: self.editarHorario(parent), hover_color="#142C3D")
            self.botonEditar.grid(row=5, column=0, padx=10 , pady=10)

            self.botonEliminar = ctk.CTkButton(self.frameIngresoDeDatos, width= 20, text='Eliminar cita', command=lambda: self.eliminarCita(parent), hover_color="#142C3D")
            self.botonEliminar.grid(row=6, column=0, padx=10 , pady=10)

            self.botonConfirmarEditar = ctk.CTkButton(self.frameIngresoDeDatos, width= 20, text='Confirmar edicion de cita', command=lambda: self.clickConfirmarEdicion(parent), hover_color="#142C3D")
            self.botonConfirmarEditar.grid(row=10, column=0, padx=10 , pady=10)

            self.elementoAEditar = None
            self.datosAntesDeEdicion = None

            self.verCitas= ctk.CTkButton(self.frameBotonesCalendario, width=20, text='Revisar Horarios Reservados', command=lambda: self.mostarFechas(parent))
            self.verCitas.grid(row=6, column=0, padx=10 , pady=10)

            self.botonVolverBuscar = ctk.CTkButton(self.frameBotonesCalendario, width= 20, text='Volver', command=lambda: parent.update_frame(parent.screenBuscarMascota, parent, container), hover_color="#142C3D")
            self.botonVolverBuscar.grid(row=9, column=0, padx=10 , pady=10)

            self.labelErrorFicha = ctk.CTkLabel(self, text="Seleccione una ficha")
            
            #componentes botones
            self.horaInicialLabel = ctk.CTkLabel(self.frameIngresoDeDatos, text='Hora Incial:', text_color="black", text_font=Font_tuple14)
            self.horaInicialLabel.grid(row=2, column=0, padx=10, pady=10)

            self.horaInicialValor = tk.DoubleVar(value=0)
            self.horaInicial = Spinbox(self.frameIngresoDeDatos, from_= 0, to = 24,width=5, state = 'readonly', textvariable=self.horaInicialValor)  
            self.horaInicial.grid(row=2, column=1, padx=10 , pady=10)

            self.minutosInicialLabel = ctk.CTkLabel(self.frameIngresoDeDatos, text='Minutos Incial:', text_color="black", text_font=Font_tuple14)
            self.minutosInicialLabel.grid(row=3, column=0, padx=10, pady=10)

            self.minutosInicialValor = tk.DoubleVar(value=0)
            self.minutosInicial = Spinbox(self.frameIngresoDeDatos, from_= 0, to = 60,width=5, state = 'readonly', textvariable=self.minutosInicialValor, increment=30)  
            self.minutosInicial.grid(row=3, column=1, padx=10 , pady=10)
#------------------------------------------------------------horas y minutos finales
            self.horaLabel = ctk.CTkLabel(self.frameIngresoDeDatos, text='Hora Final:', text_color="black", text_font=Font_tuple14)
            self.horaLabel.grid(row=4, column=0, padx=10, pady=10)

            self.horaValor = tk.DoubleVar(value=0)
            self.hora = Spinbox(self.frameIngresoDeDatos, from_= 0, to = 24,width=5, state = 'readonly', textvariable=self.horaValor)  
            self.hora.grid(row=4, column=1, padx=10 , pady=10)

            self.minutosLabel = ctk.CTkLabel(self.frameIngresoDeDatos, text='Minutos Final:', text_color="black", text_font=Font_tuple14)
            self.minutosLabel.grid(row=5, column=0, padx=10, pady=10)

            self.minutosValor = tk.DoubleVar(value=0)
            self.minutos = Spinbox(self.frameIngresoDeDatos, from_= 0, to = 60,width=5, state = 'readonly', textvariable=self.minutosValor, increment=30)  
            self.minutos.grid(row=5, column=1, padx=10 , pady=10)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            self.rutLabel = ctk.CTkLabel(self.frameIngresoDeDatos, text='Rut :', text_color="black", text_font=Font_tuple14)
            self.rutLabel.grid(row=6, column=0, padx=10 , pady=10)

            self.listaRuts = terminalVet.getRutsMascota()
            self.listaNumeros = terminalVet.getNumeroTelefonoMascota()

            print(self.listaRuts)

            self.entradaRut = AutocompleteCombobox(self.frameIngresoDeDatos, completevalues = self.listaRuts)
            self.entradaRut.grid(row=6, column=1, padx=10 , pady=10)

            self.numeroDeTelefonoLabel = ctk.CTkLabel(self.frameIngresoDeDatos, text='Telefono :', text_color="black", text_font=Font_tuple14)
            self.numeroDeTelefonoLabel.grid(row=8, column=0, padx=10 , pady=10)

            self.numeroDeTelefono = AutocompleteCombobox(self.frameIngresoDeDatos, completevalues = self.listaNumeros)
            self.numeroDeTelefono.grid(row=8, column=1, padx=10 , pady=10)

            self.confirmarCita = ctk.CTkButton(self.frameIngresoDeDatos, width=20, text='Confirmar cita', command=lambda: self.clickConfirmarFecha(parent))
            self.confirmarCita.grid(row=10, column=0, padx=10 , pady=10)
#-------------------------------------------------------------------------------------------------------------------------------------------------------

            self.lista = tk.Listbox(self.frameIngresoDeDatos, width=70, height=7, selectmode='browse', font=('Helvetica', '13')) #creanis la lista pra mostrar nuestros datos
            self.lista.grid(row=0, column=0, padx=10, pady=10)

            #self.lista.bind('<Double-1>', identificarSeleccion())

            self.horaInicialArray = []
            self.minutoInicialArray = []
            self.horaFinalArray = []
            self.minutoFinalArray = []

            self.ocularElementosDeLLenado() #ocultamos los elemtos de llenado
            #horas cita
            
            #self.IndicadorDeHora = ctk
            #self.botonConf = ctk.CTkButton(self, width=10, text='Confirmar', command=lambda: self.clickConfirmar(parent))
            #self.botonConf.pack(padx=10, pady=30)
            #self.labelErrorIngreso = ctk.CTkLabel(self, text="Llave no existente", text_font=Font_tuple12, text_color='red')

#mensajes de error 
            self.labelErrorRutTutor = ctk.CTkLabel(self.frameIngresoDeDatos, text="Ingrese rut válido", text_font=Font_tuple12, text_color="#c1121f")
            self.labelErrorNumeroTelefono = ctk.CTkLabel(self.frameIngresoDeDatos, text="Ingrese número válido (Solo números)", text_font=Font_tuple12, text_color="#c1121f")
            self.labelErrorSeleccion = ctk.CTkLabel(self.frameIngresoDeDatos, text="Seleccione un horario válido", text_font=Font_tuple12, text_color="#c1121f")
            self.labelErrorHorario = ctk.CTkLabel(self.frameIngresoDeDatos, text="Seleccione una horas y minutos validos, margen de 30 minutos", text_font=Font_tuple12, text_color="#c1121f")
            self.labelErrorSeleccionEdicion = ctk.CTkLabel(self.frameIngresoDeDatos, text="Seleccione un horario previamente reservado para edición", text_font=Font_tuple12, text_color="#c1121f")
            self.labelErrorSeleccionEliminacion = ctk.CTkLabel(self.frameIngresoDeDatos, text="Seleccione un horario previamente reservado para eliminación", text_font=Font_tuple12, text_color="#c1121f")
                
    def ocularElementosDeLLenado(self):
        self.hora.grid_remove()
        self.horaLabel.grid_remove()
        self.horaInicial.grid_remove()
        self.horaInicialLabel.grid_remove()
        self.minutos.grid_remove()
        self.minutosLabel.grid_remove()
        self.minutosInicial.grid_remove()
        self.minutosInicialLabel.grid_remove()
        self.entradaRut.grid_remove()
        self.rutLabel.grid_remove()
        self.numeroDeTelefono.grid_remove()
        self.numeroDeTelefonoLabel.grid_remove()
        self.lista.grid_remove()
        self.ingresarCita.grid_remove()
        self.confirmarCita.grid_remove()
        self.botonEditar.grid_remove()
        self.botonConfirmarEditar.grid_remove()
        self.botonEliminar.grid_remove()
    
    def mostarElementosDeLlenado(self):
        self.horaInicial.grid()
        self.horaInicialLabel.grid()
        self.minutosInicial.grid()
        self.minutosInicialLabel.grid()
        self.hora.grid()
        self.horaLabel.grid()
        self.minutos.grid()
        self.minutosLabel.grid()
        self.entradaRut.grid()
        self.rutLabel.grid()
        self.numeroDeTelefono.grid()
        self.numeroDeTelefonoLabel.grid()
        self.confirmarCita.grid()

        #quitamos elementos no necesarios
        self.lista.grid_remove()
        self.botonEditar.grid_remove()
        self.botonConfirmarEditar.grid_remove()
        self.ingresarCita.grid_remove()

        self.labelErrorSeleccionEliminacion.grid_remove()
        self.labelErrorSeleccionEdicion.grid_remove()

               #ocultamos mensajes de error
        self.labelErrorNumeroTelefono.grid_remove()
        self.labelErrorRutTutor.grid_remove()
        pass
    
    def mostarElementosDeEditar(self):
        self.horaInicial.grid()
        self.horaInicialLabel.grid()
        self.minutosInicial.grid()
        self.minutosInicialLabel.grid()
        self.hora.grid()
        self.horaLabel.grid()
        self.minutos.grid()
        self.minutosLabel.grid()
        self.entradaRut.grid()
        self.rutLabel.grid()
        self.numeroDeTelefono.grid()
        self.numeroDeTelefonoLabel.grid()
        self.confirmarCita.grid()
       
        self.lista.grid_remove()
        self.botonEditar.grid_remove()
        self.ingresarCita.grid_remove()
        self.confirmarCita.grid_remove()
        self.botonEliminar.grid_remove()
        self.botonConfirmarEditar.grid()
    
    def ocultarElementosDeEditar(self):
        self.hora.grid_remove()
        self.horaLabel.grid_remove()
        self.horaInicial.grid_remove()
        self.horaInicialLabel.grid_remove()
        self.minutos.grid_remove()
        self.minutosLabel.grid_remove()
        self.minutosInicial.grid_remove()
        self.minutosInicialLabel.grid_remove()
        self.entradaRut.grid_remove()
        self.rutLabel.grid_remove()
        self.numeroDeTelefono.grid_remove()
        self.numeroDeTelefonoLabel.grid_remove()
        self.lista.grid_remove()
        self.ingresarCita.grid_remove()
        self.confirmarCita.grid_remove()
        self.botonEditar.grid_remove()
        self.botonConfirmarEditar.grid_remove()
        
    def ocultarLlenadoParaMostarListaDeFechas(self):
        self.hora.grid_remove()
        self.horaLabel.grid_remove()
        self.horaInicial.grid_remove()
        self.horaInicialLabel.grid_remove()
        self.minutos.grid_remove()
        self.minutosLabel.grid_remove()
        self.minutosInicial.grid_remove()
        self.minutosInicialLabel.grid_remove()
        self.entradaRut.grid_remove()
        self.rutLabel.grid_remove()
        self.numeroDeTelefono.grid_remove()
        self.numeroDeTelefonoLabel.grid_remove()
        self.confirmarCita.grid_remove()

        #mostrar estos elementos
        self.lista.grid()
        self.botonEditar.grid()
        self.ingresarCita.grid()
        self.botonEliminar.grid()
    
    def quitarMensajesDeErrorBotones(self):
        self.labelErrorSeleccionEliminacion.grid_remove()
        self.labelErrorSeleccionEdicion.grid_remove()
        self.labelErrorSeleccion.grid_remove()
    
    def validarDatos(self, parent, rutTutor, numTel):
        
        flag = True

        if(parent.validarRut(rutTutor) is not True):
            flag = False
            self.labelErrorRutTutor.grid(row=7, column=1, padx=10 , pady=10)
        else:
            print("Valid")
            self.labelErrorRutTutor.grid_forget()

        if((parent.filtroNum(numTel) is not True) or (parent.filtroNoValidChar(numTel) is not True) or (len(numTel) < 9)):
            flag = False
            self.labelErrorNumeroTelefono.grid(row=9, column=1, padx=10 , pady=10)
        else: 
            self.labelErrorNumeroTelefono.grid_forget()

        
        return flag
        
    
    def ingresarCitaFuncion(self):
        for a in self.lista.curselection():
            self.elementoAEditar = self.lista.get(a)
            break

        if(self.elementoAEditar is None):
            self.labelErrorSeleccion.grid(row=7, column=0, padx=10 , pady=10)
        else:
            #
            print("2593 :"+ str(self.horaFinalArray[a]))
            fechaSeleccionada = self.calendario.get_date()

            if(terminalVet.verificarFechaEnHorario(fechaSeleccionada, self.horaInicialArray[a] ,self.horaFinalArray[a]) == False):

                self.quitarMensajesDeErrorBotones()

                indicadorDeCitas = []
                self.mostarElementosDeLlenado()
                indicadorDeCitas = self.obtenerSeccionHorariaSeleccionada() #otenemos los datos de las listas

                self.horaInicialValor.set(indicadorDeCitas[0]) #seteamos los valores en los campos 
                self.minutosInicialValor.set(indicadorDeCitas[1])
                self.horaValor.set(indicadorDeCitas[2])
                self.minutosValor.set(indicadorDeCitas[3])
            else:
                self.labelErrorSeleccion.grid(row=7, column=0, padx=10 , pady=10)
        
    def obtenerSeccionHorariaSeleccionada(self):
        indicadoresDeCitas = []
        for i in self.lista.curselection():
            print("2494 : "+str(self.horaInicialArray[i]))
            indicadoresDeCitas.append(self.horaInicialArray[i])
            indicadoresDeCitas.append(self.minutoInicialArray[i])
            indicadoresDeCitas.append(self.horaFinalArray[i])
            indicadoresDeCitas.append(self.minutoFinalArray[i])
            break
        return  indicadoresDeCitas
        
    def clickConfirmarFecha(self, parent):

        fechaSeleccionada = self.calendario.get_date()
        

        #obtenermos la hora y minutos
        horaInicialSeleccionada = self.horaInicial.get()
        minutosInicialSeleccionados = self.minutosInicial.get()

        horaFinalSeleccionada = self.hora.get()
        minutosFinalSeleccionada = self.minutos.get()

        rutIngresado = self.entradaRut.get()
        numeroIngresado = self.numeroDeTelefono.get()

        if(self.validarDatos(parent, rutIngresado, numeroIngresado) == True):
            self.indicarFechasEnCalendario(parent, fechaSeleccionada) #marcamod en color verde la fecha seleccionada
            if (terminalVet.verificarFechaCalendario(fechaSeleccionada) == False):
                id  = str(uuid.uuid4())
                fechas = {'fecha': fechaSeleccionada, 'ruts':[], 'numeros':[], 'horasInicio':[], 'minutosInicio':[], 'horasFin':[], 'minutosFin':[] , 'id': []}
                fechas["ruts"].append(rutIngresado)
                fechas["numeros"].append(numeroIngresado)
                fechas["horasInicio"].append(horaInicialSeleccionada)
                fechas["minutosInicio"].append(minutosInicialSeleccionados)
                fechas["horasFin"].append(horaFinalSeleccionada)
                fechas["minutosFin"].append(minutosFinalSeleccionada)
                fechas["id"].append(id)
                terminalVet.agregarFechasCalendario(fechas)
            else:
                terminalVet.agregarDatosAFechasCalendario(fechaSeleccionada, rutIngresado, numeroIngresado, horaInicialSeleccionada, minutosInicialSeleccionados, horaFinalSeleccionada, minutosFinalSeleccionada)
        
            self.ocularElementosDeLLenado()

    def indicarFechasEnCalendario(self, parent, fechaSeleccionada):

        fecha = fechaSeleccionada.split('/') #la transformamos a string para poder ocuparla y marcar la casilla

        fechaSeleccionada2 = datetime.date(int(fecha[2]), int(fecha[1]), int(fecha[0])) #marcamos la casilla
        self.calendario.calevent_create(fechaSeleccionada2, "", tags="vacuna") #el vento nos permite mostrar la casilla
        self.calendario.tag_config("vacuna", background="green")
    
    def indicarFechasEnCalendarioPostCargaBaseDeDatos(self, parent):

        fechas = terminalVet.getFechasCalendario()
        for i in range(len(fechas)):
            fechaSeleccionada = fechas[i]["fecha"].split('/') #la transformamos a string para poder ocuparla y marcar la casilla

            fechaAIndicar = datetime.date(int(fechaSeleccionada[2]), int(fechaSeleccionada[1]), int(fechaSeleccionada[0])) #marcamos la casilla
            self.calendario
            self.calendario.calevent_create(fechaAIndicar, "", tags="vacuna") #el vento nos permite mostrar la casilla
            self.calendario.tag_config("vacuna", background="green")

    def mostarFechas(self, parent):
        fechaSeleccionada = self.calendario.get_date() #obtenemos la fecha seleccionada
        fechaObtenida = terminalVet.getFechaCalendario(fechaSeleccionada) #obtenemos los datos de la fecha seleccionada

        #primero generamos un listado con todas los bloques horarios
        self.lista.delete(0,'end')
        hora = 0
        minuto = 0
        hora2 = 0
        minuto2 = 30
        for i in range(48): #iteramos por el maximo largo
            if i % 2 == 0:
                hora2 = hora+1
                datos = 'Hora de atención : '+str(hora)+':'+str(minuto2)+"-"+str(hora2)+':'+str(minuto)
                self.horaInicialArray.append(hora)
                self.horaFinalArray.append(hora2)
                self.minutoInicialArray.append(minuto2)
                self.minutoFinalArray.append(minuto)
                hora = hora + 1
                minuto = 0
            else:
                self.horaInicialArray.append(hora)
                self.horaFinalArray.append(hora)
                self.minutoInicialArray.append(minuto)
                self.minutoFinalArray.append(minuto2)
                datos = 'Hora de atención : '+str(hora)+':'+str(minuto)+'-'+str(hora)+':'+str(minuto2)

            self.lista.insert(END, datos)

        #verificar si ya se tienen horas reservadas 
        if (fechaObtenida is not False):
            cantidadDeElementos = len(fechaObtenida["ruts"])

            for j in range(cantidadDeElementos):
                for i in range(len(self.horaInicialArray)): #iteramos por el maximo largo
                        if(fechaObtenida["horasInicio"][j] == str(self.horaInicialArray[i]) and fechaObtenida["minutosInicio"][j] == str(self.minutoInicialArray[i])): #identificamos la hora de 
                            datos = 'Hora de atención : '+str(self.horaInicialArray[i])+':'+str(self.minutoInicialArray[i])+'-'+str(self.horaFinalArray[i])+':'+str(self.minutoFinalArray[i])+" Rut : "+str(fechaObtenida["ruts"][j])+" numero : "+str(fechaObtenida["numeros"][j])
                            self.lista.delete(i) #en al linea anterior lar horas permaneceran igual, sin embargo datos como rut y numeros son sacados de la clase calendario
                            self.lista.insert(i, datos)
                            break
    
        self.ocultarLlenadoParaMostarListaDeFechas()

        #self.lista.delete(0,'end')
        #for i in range(len(fechaObtenida["ruts"])): #iteramos por el maximo largo
         #   datos = 'rut :'+str(fechaObtenida["ruts"][i])+' numero de telefono: '+str(fechaObtenida["numeros"][i])+' Hora de atención: '+str(fechaObtenida["horas"][i])+':'+str(fechaObtenida["minutos"][i]+"hrs")
            
          #  self.lista.insert(END, datos)
        
        #self.ocultarLlenadoParaMostar()
    

    def editarHorario(self, parent):
        self.labelErrorSeleccionEliminacion.grid_remove()
        self.labelErrorSeleccionEdicion.grid_remove()
        indicadorDeSeleccion = False
        for a in self.lista.curselection():
            self.elementoAEditar = self.lista.get(a)

            if(self.elementoAEditar != None): #verificamos que haya seleccionado un fecha
                fechaSeleccionada = self.calendario.get_date()
                datosFecha = terminalVet.getFechaCalendario(fechaSeleccionada)

                if(datosFecha != False):#verificamos que haya una cita en el horario seleccionado
                    self.quitarMensajesDeErrorBotones()
                    cantidadDeElementos = len(datosFecha["ruts"])
                    
                    for j in range(cantidadDeElementos):
                        if((datosFecha["horasInicio"][j] == str(self.horaInicialArray[a])) and (datosFecha["minutosInicio"][j] == str(self.minutoInicialArray[a])) and datosFecha["ruts"][j] is not None): #identificamos la hora de 

                            print("2724 : "+str(datosFecha["horasInicio"][j])+"-"+str(self.minutoInicialArray[a]))

                            self.horaInicialValor.set(datosFecha["horasInicio"][j])
                            self.minutosInicialValor.set(datosFecha["minutosInicio"][j])

                            self.horaValor.set(datosFecha["horasFin"][j])
                            self.minutosValor.set(datosFecha["minutosFin"][j])

                            horasInciales = [datosFecha["horasInicio"][j], datosFecha["minutosInicio"][j], datosFecha["horasFin"][j], datosFecha["minutosFin"][j]]

                            if(str(datosFecha["ruts"][j]) is not None):
                                self.entradaRut.delete(0, 'end')
                                self.entradaRut.insert(0, str(datosFecha["ruts"][j]))
                                self.numeroDeTelefono.delete(0, 'end')
                                self.numeroDeTelefono.insert(0, str(datosFecha["numeros"][j]))
                                self.mostarElementosDeEditar()
                                self.elementoAEditar = datosFecha
                                self.datosAntesDeEdicion = horasInciales
                                indicadorDeSeleccion = True
                            
                            break
                else:
                    self.labelErrorSeleccionEdicion.grid(row=7, column=0, padx=10 , pady=10)
                    break
        
        if(indicadorDeSeleccion == False): #verificamos que haya seleccionado una cita valida para edicion
            self.labelErrorSeleccion.grid(row=7, column=0, padx=10 , pady=10)
        else:
            self.labelErrorSeleccion.grid_remove()
                #cargamos los datos a editar en los entry
    
    def validarHoraSeleccionadaValida(self, horaInicialSeleccionada, minutosInicialSeleccionados, horaFinalSeleccionada, minutosFinalSeleccionada):

        horaInicial = int(horaInicialSeleccionada)*100
        minutosInicial = int(minutosInicialSeleccionados)
        horaFinal = int(horaFinalSeleccionada)*100
        minutosFinal = int(minutosFinalSeleccionada)

        print(horaInicial)
        print(minutosInicial)
        print(horaFinal)
        print(minutosFinal)

        horarioInicial = horaInicial+minutosInicial
        horarioFinal = horaFinal+minutosFinal
        print(horarioInicial)
        print(horarioFinal)

        if(horarioFinal-horarioInicial == 30):
            return True
        
        return False


    def clickConfirmarEdicion(self, parent):

        fechaSeleccionada = self.calendario.get_date()
                            
                    #obtenermos la hora y minutos
        horaInicialSeleccionada = self.horaInicial.get()
        minutosInicialSeleccionados = self.minutosInicial.get()

        horaFinalSeleccionada = self.hora.get()
        minutosFinalSeleccionada = self.minutos.get()

        rutIngresado = self.entradaRut.get()
        numeroIngresado = self.numeroDeTelefono.get()

        if(self.validarDatos(parent, rutIngresado, numeroIngresado) == True and self.validarHoraSeleccionadaValida(horaInicialSeleccionada, minutosInicialSeleccionados, horaFinalSeleccionada, minutosFinalSeleccionada) == True):
        
            datosFecha = self.elementoAEditar
            for j in range(len(datosFecha["ruts"])):
                if(datosFecha["horasInicio"][j] == str(self.datosAntesDeEdicion[0])): #identificamos la hora dentro del diccionario

                    self.ocultarElementosDeEditar()
                    self.labelErrorHorario.grid_remove()
                    terminalVet.editarDatosDeFecha(fechaSeleccionada, rutIngresado, numeroIngresado, horaInicialSeleccionada, minutosInicialSeleccionados, horaFinalSeleccionada, minutosFinalSeleccionada, j)
        else:
            self.labelErrorHorario.grid(row=12, column=0, padx=10 , pady=10)

    def eliminarCita(self, parent):
        self.labelErrorSeleccionEliminacion.grid_remove()
        self.labelErrorSeleccionEdicion.grid_remove()
        indicadorDeSeleccion = False
        for i in self.lista.curselection():
            self.elementoAEditar = self.lista.get(i)

            if(self.elementoAEditar != None): #verificamos que haya seleccionado un fecha
                fechaSeleccionada = self.calendario.get_date()
                datosFecha = terminalVet.getFechaCalendario(fechaSeleccionada)
                
                if(datosFecha != False):#verificamos que haya una cita en el horario seleccionado
                    self.quitarMensajesDeErrorBotones()
                    cantidadDeElementos = len(datosFecha["ruts"])
                    for j in range(cantidadDeElementos):
                        if(datosFecha["horasInicio"][j] == str(self.horaInicialArray[i])): #identificamos la hora seleccionada para de esta manera eliminar los datos
                            datos = 'Hora de atención : '+str(self.horaInicialArray[i])+':'+str(self.minutoInicialArray[i])+'-'+str(self.horaFinalArray[i])+':'+str(self.minutoFinalArray[i])
                            self.lista.delete(i) #en al linea anterior lar horas permaneceran igual, sin embargo datos como rut y numeros son sacados de la clase calendario
                            self.lista.insert(i, datos)
                            indicadorDeSeleccion = True
                            terminalVet.eliminarDatosDeFecha(fechaSeleccionada, j)
                            break
                else:
                    self.labelErrorSeleccionEliminacion.grid(row=7, column=0, padx=10 , pady=10)
                    break

            break

        if(indicadorDeSeleccion == False): #verificamos que haya seleccionado una cita valida para edicion
            self.labelErrorSeleccion.grid(row=7, column=0, padx=10 , pady=10)
        else:
            self.labelErrorSeleccion.grid_remove()
       
            
            #indicadoresDeCitas.append(self.horaInicialArray[i])
            #indicadoresDeCitas.append(self.minutoInicialArray[i])
            #indicadoresDeCitas.append(self.horaFinalArray[i])
            #indicadoresDeCitas.append(self.minutoFinalArray[i])

        return  #indicadoresDeCitas
              
                   
    
        


#----------------------------------------------------------------------------           ------------------------------              ------------------------------                  
class screenAbstractMedico(ctk.CTkFrame):
    def __init__(self, parent, container):
        super().__init__(container, fg_color="#C5DEDD")

        mascotaActual:Mascota = parent.getMascotaApp()
        if(mascotaActual is not None):
            
            textodatosDueno = f'Nombre Dueño: {mascotaActual.getNombreTutor()}\nTelefono: {mascotaActual.getNumeroTelefono()}\nDireccion: {mascotaActual.getDireccion()}'
            textoinfoBasicaMascota = f'Nombre Mascota: {mascotaActual.getNombreMascota()}\nRaza: {mascotaActual.getRaza()}'
            textoVacunasAlergias = self.setCadenaVacunasAlergias(mascotaActual)
            textoOperaciones = self.setCadenaOperaciones(mascotaActual)


            idsFichas = mascotaActual.getIdsFichas()
            medicamentos = []
            i = 0
            while(i <= (len(idsFichas)-1)):
                print("tukiiiiiiiiiiiiiii")
                terminalVet.completarFichaParcialMascotasExternas(mascotaActual.getId(), idsFichas[i]) #completamos cada ficha parcial para extraer los datos para el resumen veterinario 
                i += 1

            textoMedicamentos = self.setCadenaMedicamentos(mascotaActual)

            #-----------FRAME DATOS DUENO--------------------------------------
            self.titleDatosDueno = ctk.CTkLabel(self, text="Datos del dueño", text_color="Black", text_font=("Helvetica", "13"), fg_color="#AC99DE")
            
            self.titleDatosDueno.place(x=20, y=18)
            
            self.frameDatosDueno = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameDatosDueno.grid(row=0, column=0, padx=20, pady=(50,20))

            self.textDatosDuenoSAbstract = tk.Text(self.frameDatosDueno, width = 36, height= 5, background="#F0EFEB", font=("Helvetica", 13), state=NORMAL)
            self.textDatosDuenoSAbstract.pack(padx=20, pady=20)

            self.textDatosDuenoSAbstract.delete(1.0, END)
            self.textDatosDuenoSAbstract.pack(padx=20, pady=20)
            self.textDatosDuenoSAbstract.insert(END, textodatosDueno)
            self.textDatosDuenoSAbstract.configure(state="disabled", background="#99C1DE", border=0)
            #-----------FRAME DATOS DUENO--------------------------------------

            #-----------FRAME INFO BASICA--------------------------------------
            self.titleInfoBasica = ctk.CTkLabel(self, text="Datos básicos mascota", text_color="Black", text_font=("Helvetica", "13"), padx=8, bg_color="#AC99DE")
            self.titleInfoBasica.place(x=20, y=220)

            self.frameInfoBasica = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameInfoBasica.grid(row=1,column=0,padx=20, pady=45)

            self.textInfoBasicaMascota = tk.Text(self.frameInfoBasica, width = 36, height= 5, background="#F0EFEB", font=("Helvetica", 13), state=NORMAL)
            self.textInfoBasicaMascota.pack(padx=20, pady=20)

            self.textInfoBasicaMascota.delete(1.0, END)
            self.textInfoBasicaMascota.pack(padx=20, pady=20)
            self.textInfoBasicaMascota.insert(END, textoinfoBasicaMascota)
            self.textInfoBasicaMascota.configure(state="disabled", background="#99C1DE", border=0)
            #-----------FRAME INFO BASICA--------------------------------------

            #-----------FRAME VACUNAS--------------------------------------
            self.titleVacunasAlergias = ctk.CTkLabel(self, text="Vacunas y alergias mascota", text_color="Black", text_font=("Helvetica", "13"), padx=8, bg_color="#AC99DE")
            self.titleVacunasAlergias.place(x=20, y=422)

            self.frameVacunas = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameVacunas.grid(row=2,column=0,padx=20, pady=20)

            self.textVacunasAlergiasMascota = tk.Text(self.frameVacunas, width = 36, height= 5, background="#F0EFEB", font=("Helvetica", 13), state=NORMAL)
            self.textVacunasAlergiasMascota.pack(padx=20, pady=20)

            self.textVacunasAlergiasMascota.delete(1.0, END)
            self.textVacunasAlergiasMascota.pack(padx=20, pady=20)
            self.textVacunasAlergiasMascota.insert(END, textoVacunasAlergias)
            self.textVacunasAlergiasMascota.configure(state="disabled", background="#99C1DE", border=0, wrap=WORD)
            #-----------FRAME VACUNAS--------------------------------------

            #-----------FRAME OPERACIONES--------------------------------------
            self.titleOperaciones = ctk.CTkLabel(self, text="Operaciones mascota", text_color="Black", text_font=("Helvetica", "13"), padx=8, bg_color="#AC99DE")
            self.titleOperaciones.place(x=428, y=18)

            self.frameOperaciones = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameOperaciones.grid(row=0,column=1,padx=20, pady=(50,20))

            self.textOperaciones = tk.Text(self.frameOperaciones, width = 36, height= 5, background="#F0EFEB", font=("Helvetica", 13), state=NORMAL)
            self.textOperaciones.pack(padx=20, pady=20)
            
            self.textOperaciones.delete(1.0, END)
            self.textOperaciones.pack(padx=20, pady=20)
            self.textOperaciones.insert(END, textoOperaciones)
            self.textOperaciones.configure(state="disabled", background="#99C1DE", border=0, wrap=WORD)
            #-----------FRAME OPERACIONES--------------------------------------

            #-----------FRAME MEDICAMENTOS--------------------------------------
            self.titleMedicamentos = ctk.CTkLabel(self, text="Medicamentos mascota", text_color="Black", text_font=("Helvetica", "13"), padx=8, bg_color="#AC99DE")
            self.titleMedicamentos.place(x=428, y=220)

            self.frameMedicamentos = ctk.CTkFrame(self, corner_radius=10, fg_color="#99C1DE")
            self.frameMedicamentos.grid(row=1,column=1,padx=20, pady=45)

            self.textMedicamentos = tk.Text(self.frameMedicamentos, width = 36, height= 5, background="#F0EFEB", font=("Helvetica", 13), state=NORMAL)
            self.textMedicamentos.pack(padx=20, pady=20)

            self.textMedicamentos.delete(1.0, END)
            self.textMedicamentos.pack(padx=20, pady=20)
            self.textMedicamentos.insert(END, textoMedicamentos)
            self.textMedicamentos.configure(state="disabled", background="#99C1DE", border=0, wrap=WORD)
            #-----------FRAME MEDICAMENTOS--------------------------------------

            self.botonIrAMenuGeneral = ctk.CTkButton(self, width= 150, height= 100,text='Ir a Menu General', text_font=("Helvetica", "13"), command=lambda: self.insetarMascotaEnVeterinariaActual(parent, mascotaActual, container))
            self.botonIrAMenuGeneral.grid(row=0, column=2, padx=20, pady=20)

            self.botonVolverSAbstract = ctk.CTkButton(self, width= 150, height= 100,text='Volver', text_font=("Helvetica", "13"), command=lambda: parent.update_frame(parent.screenBuscarMascota, parent, container))
            self.botonVolverSAbstract.grid(row=1, column=2, padx=20, pady=20)

    def setCadenaVacunasAlergias(self, mascotaActual:Mascota):
        vacunasTabla = mascotaActual.getVacunasSuministradas()
        vacunas = ''
        i = 0
        while(i <= (len(vacunasTabla)-1)):
            if(i == (len(vacunasTabla)-1)):
                vacunas = vacunas + str(vacunasTabla[i]['nomVacuna']) + '.'
            else:
                vacunas = vacunas + str(vacunasTabla[i]['nomVacuna']) + ', '
            i += 1
        vacunasString = f'Vacunas: \n{vacunas}'

        i = 0
        alergiasTabla = mascotaActual.getAlergias()
        alergias = ''
        while(i <= (len(alergiasTabla)-1)):
            if(i==(len(alergiasTabla)-1)):
                alergias = alergias + str(alergiasTabla[i]['nombre']) + '.'
            else:
                alergias = alergias + str(alergiasTabla[i]['nombre']) + ', '
            i += 1
        alergiasString = f'Alergias: \n{alergias}'

        stringRetorno = vacunasString + '\n' + alergiasString

        return stringRetorno

    def setCadenaOperaciones(self, mascotaActual:Mascota):
        operacionesTabla = mascotaActual.getRegistroDeOperaciones()
        operaciones = ''
        i = 0
        while(i <= (len(operacionesTabla)-1)):
            if(i==(len(operacionesTabla)-1)):
                operaciones = operaciones + str(operacionesTabla[i]['operacion']) + '.'
            else:
                operaciones = operaciones + str(operacionesTabla[i]['operacion']) + ', '
            i += 1
        operacionesString = f'Operaciones: {operaciones}'

        return operacionesString

    def setCadenaMedicamentos(self, mascotaActual:Mascota):
        idsFichas = mascotaActual.getIdsFichas()
        medicamentos = ''
        i = 0
        while(i <= (len(idsFichas)-1)):
          
            listaMedicamanetos = terminalVet.getMedicamentosConsulta(idsFichas[i], mascotaActual.getId())
          
            if(len(listaMedicamanetos)>0):
             
                for medicamento in listaMedicamanetos:
                    medicamentos = medicamentos + str(medicamento['nomMedicamento']) + '\n'
                
            i += 1
        
        return medicamentos
    
    def setCadenaMedicamentosFlase(self, listaMedicamanetos):
        medicamentos = ''
        i = 0
        for i in range(len(listaMedicamanetos)):
            for medicamento in listaMedicamanetos[i]:
                medicamentos = medicamentos + str(medicamento[0]['nomMedicamento']) + '\n'
        
        return medicamentos
    
    def insetarMascotaEnVeterinariaActual(self, parent, mascotaActual, container):
        
        
        #self, id, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, alergias, tablaMedica, fechaNacimiento
        

        if(terminalVet.verificarPresenciaDeTablaDeMascota(mascotaActual.getId()) != None):
            
            terminalVet.setMascotaOtraVeterinaria(mascotaActual.getId())
            mascotalol = terminalVet.getMascota(mascotaActual.getId())
            terminalVet.buscarMascotaLocal2(mascotalol.getId())
            mascotalol.setAlergias(mascotaActual.getAlergias())

            parent.setMascotaApp(mascotalol)
            parent.update_frame(parent.screenDatosTotalMascota, parent, container)
        else:
            alergias = ""
            for alegia in  mascotaActual.getAlergias():
                alergias += alergias+str(alegia['nombre'])+';'

            terminalVet.setMascotaOtraVeterinaria(mascotaActual.getId()) #agrega la nueva mascota al arreglo de mascotas locales para su manejo
            mascotalol = terminalVet.getMascota(mascotaActual.getId())
            tablaMedica = TablaMedica(uuid.uuid4())
            
            terminalVet.agregarMascotaDesdeAbstractPrimeraVez(mascotaActual.getId(), mascotaActual.getNombreMascota(), mascotaActual.getEspecie(), mascotaActual.getColorMascota(), mascotaActual.getRaza(), mascotaActual.getNombreTutor(), mascotaActual.getRutTutor(),
            mascotaActual.getNumeroTelefono(), mascotaActual.getDireccion(), alergias, tablaMedica.getId(), mascotaActual.getFechaDeNacimiento())
            parent.setMascotaApp(mascotalol)
            parent.update_frame(parent.screenDatosTotalMascota, parent, container)

           
        #*quitar tablaMedica de mascota en insert into
        #*agregar terminal a tabla en insert into

    

app = App()
app.mainloop()