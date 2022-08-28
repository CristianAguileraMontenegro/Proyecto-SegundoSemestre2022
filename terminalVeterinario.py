from ast import Str
from tkinter import *
import os
import os.path
import uuid

from datetime import datetime
from webbrowser import get
import mysql.connector
import socket

from mascota import Mascota 
from tablaMedica import TablaMedica
from fichaMedica import FichaMedica

db = mysql.connector.connect(
    user='root',
    password='root',
    host='localhost',
    database='mydb',
    port='3306'
)

mycursor = db.cursor()

class terminal:

    def __init__(self):

        self.id = self.generarIdTerminal()
        self.tokenActivacion = None
        self.idVeterianria = None
        self.nombreVeterinaria = None
        self.mascotas:Mascota = []

        self.validarTokenDeActivacion()

        if (self.tokenActivacion == True):
             # De ser el caso que el token esta ya activado, se instancian aquí, debido a que actToken no se llamará
            self.setIdVeterinaria()
            self.setNombreVeterinaria()
            self.setMascotas()

    def setIdVeterinaria(self):
        sql = 'SELECT Veterinaria_idVeterinaria FROM TerminalVeterinario WHERE idTerminalVeterinario = (%s)'
        mycursor.execute(sql, (str(self.id),))
        idVet = mycursor.fetchone()
        self.idVeterinaria = idVet[0]

    def setNombreVeterinaria(self):
        sql = 'SELECT Veterinaria_nombreVeterinaria FROM TerminalVeterinario WHERE idTerminalVeterinario = (%s)'
        mycursor.execute(sql, (str(self.id),))
        nombreVet = mycursor.fetchone()
        self.nombreVeterinaria = nombreVet[0]
    
    def setMascotas(self):
        sql = 'SELECT Mascota_idMascota FROM Mascota_has_TerminalVeterinario WHERE TerminalVeterinario_idTerminalVeterinario = (%s)'
        mycursor.execute(sql, (str(self.idVeterinaria),))
        ids = mycursor.fetchall()
        for i in range(len(ids)):

            sql = 'SELECT * FROM Mascota WHERE idMascota = (%s)'
            mycursor.execute(sql, (str(ids[i][0]),))
            resultado = mycursor.fetchone()

            sql = 'SELECT * FROM RegistroDeOperaciones WHERE TablaMedica_idTablaMedica = (%s)'
            mycursor.execute(sql, (str(resultado[9]),)) #el numero 9 representa el campo 10 de la tabla de mascotas = id tabla medica 
            registroOp = mycursor.fetchall()

            sql = 'SELECT * FROM RegistroVacunasSuministradas WHERE TablaMedica_idTablaMedica = (%s)'
            mycursor.execute(sql, (str(resultado[9]),))
            registroVac = mycursor.fetchall()

            sql = 'SELECT * FROM Alergias WHERE TablaMedica_idTablaMedica = (%s)'
            mycursor.execute(sql, (str(resultado[9]),))
            alergiasEntregar = mycursor.fetchall()

            tablaEntregar = TablaMedica(resultado[9],  alergiasEntregar, registroOp, registroVac)
            tablaEntregar.solicitarFichasEnBaseDeDatos()#solicitamos las fichas correspondientes a la tabla

            mascotalol= Mascota(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5], resultado[6],
                                    resultado[7], resultado[8], tablaEntregar)
            self.mascotas.append(mascotalol)
    
    def agregarMascota(self, id, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, tablaMedica):
        mascotaNueva = Mascota(id, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, tablaMedica)
        self.mascotas.append(mascotaNueva)
        mascotaNueva.agregarMascotaEnBaseDeDatos()
        mascotaNueva.agregarTablaMascota(self.id)
        mascotaNueva.guardarTablaEnBaseDeDatos()



    def agregarFichaMedica(self, idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, idMascota):
        for mascota in self.mascotas:
            if mascota.getId() == idMascota:
                mascota.agregarFichaMedicaConsultaATabla(idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp)
                #mascota.setIdFicha(fichaMedica.getId())
                #mascota.setSucursalVeterinariaFicha(fichaMedica.getSucursalVeterinaria())
                #mascota.setVeterinarioACargoFicha(fichaMedica.getVeterinarioACargo())
                #mascota.setFechaConsultaFicha()
                #mascota.setFrecRespiratoriaFicha()
                #mascota.setFrecCardiacaFicha()
                #mascota.setPesoFicha()
                #mascota.setEdadFicha()
                #mascota.setTempFicha()
                #mascota.setFichaDeOperacion()
                #mascota.setFichaDeHospitalizacion()
                #mascota.setFichaDeSefacion()
                #mascota.setOperacionFicha()
                #mascota.setHospitalizacionFicha()
                #mascota.setSedacionFicha()
                break

    def agregarFichaOperacion(self, idFicha, idMascota, opFicha):
        for mascota in self.mascotas:
            if mascota.getId() == idMascota:
                mascota.setFichaDeOperacion(opFicha, idFicha)
    
    def agregarFichaSedacion(self, idFicha, idMascota, sedFicha):
        for mascota in self.mascotas:
            if mascota.getId() == idMascota:
                mascota.setFichaDeSefacion(sedFicha, idFicha)

    def agregarFichaHospitalizacion(self, idFicha, idMascota, hospFicha):
        for mascota in self.mascotas:
            if mascota.getId() == idMascota:
                mascota.setFichaDeHospitalizacion(hospFicha, idFicha)


    def BuscarMascota(self, idMascotaBuscada):
        sql = 'SELECT * FROM mascota WHERE idMascota = (%s)' #muestra informacion bascia buscar 
        mycursor.execute(sql, (idMascotaBuscada,))
        resultado2 = mycursor.fetchone()
    
    def verificarMascotaEnSistema(self): #debe ser adaptado y modificado para las nuevas screens

        if(self.inputBuscar.text() != ""): #& len(self.inputBuscar.text()) == 15):
            self.MensajeErrorBusqueda.setVisible(False)
            idMascotaBuscada = self.inputBuscar.text()
            sql = 'SELECT idMascota FROM mascota WHERE idMascota = (%s)'
            mycursor.execute(sql, (idMascotaBuscada,))
            resultado = mycursor.fetchone()
            if(resultado != None):
                sql = 'SELECT Mascota_idMascota FROM Mascota_has_TerminalVeterinario WHERE TerminalVeterinario_idTerminalVeterinario = (%s)'
                mycursor.execute(sql, (self.idVeterinaria,))
                resultado = mycursor.fetchall()
                flagMascotaEnc = False
                for id in resultado:
                    if(id[0] == str(idMascotaBuscada)):
                        flagMascotaEnc = True
                self.botonAgregar.setVisible(False)
                if(flagMascotaEnc):    
                    self. buscarMascotaLocal(idMascotaBuscada)
                else:
                    self.BuscarMascota(idMascotaBuscada)
                    self.datosMostrar.setVisible(True)
                    self.botonAbstracto.setVisible(True)
                    self.botonEntrar.setVisible(False)
            else:
                #Funcion registrar mascota
                self.datosMostrar.setText('Mascota no ingresada en el sistema')
                self.botonAgregar.setVisible(True)
                self.datosMostrar.setVisible(True)
                self.botonAbstracto.setVisible(False)
                self.botonEntrar.setVisible(False)
                self.botonAgregar.clicked.connect(lambda : self.agregarMascota(idMascotaBuscada))
        else:
            self.MensajeErrorBusqueda.setVisible(True)


    #Metodos relacionados con la validación del terminal

    def validarConexionInternet(self):
        try:
            socket.create_connection(('Google.com',80))
            return True
        except OSError:
            return False    
            
    def validarLlaveConServidor(self):

        #uic.loadUi("Proyecto-PetRecord/Complementos/AbstracMedico.ui", self) 

        llaveEntrada = self.keyInput.text()##obtiene los datos ingresados de tiene que ponder en nombre de la clase 
        #toma los valores como string
        mycursor.execute(f'SELECT Llaves FROM keysactivación WHERE Llaves = {llaveEntrada}')
        resultado = mycursor.fetchone()
        
        if(resultado == None):
            self.label_3.setVisible(True)
        else:
            mycursor.execute(f'SELECT Veterinaria_idVeterinaria FROM Keysactivación WHERE Llaves = {llaveEntrada}')
            idVetActual = mycursor.fetchone()
            
            mycursor.execute(f'SELECT Veterinaria_nombreVeterinaria FROM Keysactivación WHERE Llaves = {llaveEntrada}')
            nombreVetActual = mycursor.fetchone()
            self.activarTokenDeActivacion(idVetActual[0], nombreVetActual[0])

    def activarTokenDeActivacion(self, idVet, nombreVet):
        self.tokenActivacion = True
        sql = 'INSERT INTO terminalveterinario (idTerminalVeterinario, tokenDeActivación, Veterinaria_idVeterinaria, Veterinaria_nombreVeterinaria) VALUES (%s,%s,%s,%s)'
        val = (str(self.id),self.tokenActivacion,idVet,nombreVet)
        mycursor.execute(sql, val)
        db.commit()
        # Se setean los atributos de la clase cuando se activa el token
        self.consultaBDtokenDeActivacion()
        self.cargarScreenBuscarMascota() #se carga la screen buscarMascota

    def consultaBDtokenDeActivacion(self):
        self.setIdVeterinaria()
        self.setNombreVeterinaria()
        self.setMascotas()
    
    def validarTokenDeActivacion(self):
        
        if(self.validarConexionInternet()): #pimero valida la conexión si hay pasa
            print("si hay conexion")
            sql = 'SELECT tokenDeActivación FROM terminalveterinario WHERE idTerminalVeterinario = (%s)'
            val = (self.id)
            mycursor.execute(sql, (val,))
            resultado = mycursor.fetchone()
            
            if(resultado == None):
                pass
            elif(resultado[0] == 1):
                self.tokenActivacion = True
            
                
        else:
            print("no hay conexion a internet") 
            #hacer una screen de volver aconectar  

    def generarIdTerminal(self):
        if (os.path.exists("infoTerminal.txt")):
            with open("infoTerminal.txt", "r") as f:
                return f.read()
                
        else:
            with open("infoTerminal.txt", "w") as f: #si no existe el archivo lo creamos y le damos el formato default
                idRand = uuid.uuid4()
                f.write(f"{idRand}")
                return str(idRand)
