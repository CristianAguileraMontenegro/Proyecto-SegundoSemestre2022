from ast import Str
from subprocess import list2cmdline
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

if __name__ != "__main__":
    class Terminal:

        def __init__(self):

            self.id = self.generarIdTerminal()
            self.tokenActivacion = None
            self.idVeterinaria = None
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
            sql = 'SELECT Mascota_idMascota FROM Mascota_has_TerminalVeterinario as maste join terminalveterinario as termi on termi.IdTerminalVeterinario = maste.TerminalVeterinario_idTerminalVeterinario join veterinaria as veti on veti.idVeterinaria = termi.Veterinaria_idVeterinaria WHERE veti.idVeterinaria = (%s)'
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

                vacunasFinal = []
                vacunaDicc = {}
                
                for vacuna in registroVac:
                    vacunaDicc = {
                        'id':vacuna[0],
                        'nomVacuna':vacuna[1]
                    }
                    vacunasFinal.append(vacunaDicc)

                sql = 'SELECT * FROM Alergias WHERE TablaMedica_idTablaMedica = (%s)'
                mycursor.execute(sql, (str(resultado[9]),))
                alergiasEntregar = mycursor.fetchall()

                alergiaFinal = []
                alergiaDicc = {}
                for alergia in alergiasEntregar:
                    alergiaDicc = {
                        'id':alergia[0],
                        'nombre':alergia[1]
                    }
                    alergiaFinal.append(alergiaDicc)

                registroOperacionesFinal = []
                operacionesDicc = {}
                for operacion in registroOp:
                    operacionesDicc = {
                        'id':operacion[0],
                        'operacion':operacion[1]
                    }
                    registroOperacionesFinal.append(operacionesDicc)
                
                tablaEntregar = TablaMedica(resultado[9])
                tablaEntregar.setAlergias(alergiaFinal)
                tablaEntregar.setRegistroDeVacunas(vacunasFinal)
                tablaEntregar.setRegistroDeOperaciones(registroOperacionesFinal)
                
                tablaEntregar.solicitarFichasEnBaseDeDatos()#solicitamos las fichas correspondientes a la tabla
                #print(str(tablaEntregar.getIdsFichas()))

                mascotalol= Mascota(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5], resultado[6],
                                        resultado[7], resultado[8], tablaEntregar)
                
                
                self.mascotas.append(mascotalol)
        
        def agregarMascota(self, id, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, alergias, tablaMedica):
            mascotaNueva = Mascota(id, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, tablaMedica)

            self.mascotas.append(mascotaNueva)

            alergiasArray = alergias.split(';')
            alergiaDicc = {}
            alergiasFinal = []
            for alergia in alergiasArray:
                idAlergia = str(uuid.uuid4())
                alergiaDicc = {
                    'id':idAlergia,
                    'nombre':alergia
                }
                alergiasFinal.append(alergiaDicc)

            mascotaNueva.guardarTablaEnBaseDeDatos()
            
            mascotaNueva.setAlergiasBas(alergiasFinal)

            mascotaNueva.agregarMascotaEnBaseDeDatos() 

            mascotaNueva.agregarTablaMascota(self.id)
            

        def agregarFichaMedica(self, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, idMascota, tratamientos, causaVisita, medicamentos, vacunas):
            idFicha = uuid.uuid4()
            for mascota in self.mascotas:
                if mascota.getId() == idMascota:
                    mascota.agregarFichaMedicaConsultaATabla(idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp)
                    #los indicadores de fichas especiales simpre seran 0 en un inicio

                    #agregamos los demas datos

                    tratamientosA = tratamientos.split(';')
                    tratClase = []
                    tratDicc = {}
                    for trat in tratamientosA:
                        idTratamiento = str(uuid.uuid4())
                        tratDicc = {
                            'id' : idTratamiento,
                            'nombreTratamiento': trat,
                            'causaVisita' : causaVisita,
                        }
                        tratClase.append(tratDicc)
                    mascota.setTratamientos(tratClase)

                    medicamentosA = medicamentos.split(';')
                    medClase = []
                    medDicc = {}
                    for med in medicamentosA:
                        idMedicamento = str(uuid.uuid4())
                        medDicc = {
                            'id' : idMedicamento,
                            'nomMedicamento' : med,
                        }
                        medClase.append(medDicc)
                    mascota.setMedicamentos(medClase)

                    vacunasA = vacunas.split(';')
                    vacClase = []
                    vacDicc = {}
                    for vac in vacunasA:
                        idVacunas = str(uuid.uuid4())
                        vacDicc = {
                            'id' : idVacunas,
                            'nomVacuna' : vac,
                        }    
                        vacClase.append(vacDicc)
                        mascota.agregarVacunas(vacDicc) #agregamos las vacunas indicadas a la tabla 
                    mascota.setVacunas(vacClase) #seteamos las vacunas en la ficha
           

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


        def buscarMascotaRemota(self, idMascotaBuscada):
            sql = 'SELECT * FROM mascota WHERE idMascota = (%s)' #muestra informacion bascia buscar 
            mycursor.execute(sql, (idMascotaBuscada,))
            resultado = mycursor.fetchone()
            if(resultado != None):

                sql = 'SELECT * FROM RegistroDeOperaciones WHERE TablaMedica_idTablaMedica = (%s)'
                mycursor.execute(sql, (str(resultado[9]),)) #el numero 9 representa el campo 10 de la tabla de mascotas = id tabla medica 
                registroOp = mycursor.fetchall()

                sql = 'SELECT * FROM RegistroVacunasSuministradas WHERE TablaMedica_idTablaMedica = (%s)'
                mycursor.execute(sql, (str(resultado[9]),))
                registroVac = mycursor.fetchall()

                sql = 'SELECT * FROM Alergias WHERE TablaMedica_idTablaMedica = (%s)'
                mycursor.execute(sql, (str(resultado[9]),))
                alergiasEntregar = mycursor.fetchall()

                tablaEntregar = TablaMedica(resultado[9])
                
                tablaEntregar.setAlergias(alergiasEntregar)
                tablaEntregar.setRegistroDeVacunas(registroVac)
                tablaEntregar.setRegistroDeOperaciones(registroOp)

                tablaEntregar.solicitarFichasEnBaseDeDatos()
                
                mascotaEncontrada= Mascota(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5], resultado[6],
                                            resultado[7], resultado[8], tablaEntregar)

                return mascotaEncontrada

        def buscarMascotaLocal(self, idMascota):
            mascotaEncontrada:Mascota = None
            for mascota in self.mascotas:
                if(mascota.getId() == str(idMascota)):
                    mascotaEncontrada = mascota

            return mascotaEncontrada

        
        def verificarMascotaEnSistema(self, codigoMascotaGUI): #debe ser adaptado y modificado para las nuevas screens
            malCodigo = "MalCodigo"
            mascotaLocal = "MascotaLocal"
            mascotaRemote = "MascotaRemota"
            mascotaNoExiste = "MascotaNoExiste"
            listRetorno = []

            if(codigoMascotaGUI != ""): #& len(self.inputBuscar.text()) == 15):
                #self.MensajeErrorBusqueda.setVisible(False)
                idMascotaBuscada = codigoMascotaGUI
                flagMascotaEnc = False 
                for mascota in self.mascotas:
                    if(mascota.getId() == str(idMascotaBuscada)):
                        flagMascotaEnc = True
                
                if(flagMascotaEnc):
                    mascotaBuscada = self.buscarMascotaLocal(idMascotaBuscada)
                    listRetorno.append(mascotaLocal)
                    listRetorno.append(mascotaBuscada)
                    return listRetorno
                elif(flagMascotaEnc == False):
                    mascotaBuscada = self.buscarMascotaRemota(idMascotaBuscada)
                    if(mascotaBuscada != None):
                        listRetorno.append(mascotaRemote)
                        listRetorno.append(mascotaBuscada)
                        return listRetorno
                
                sql = 'SELECT idMascota FROM mascota WHERE idMascota = (%s)'
                mycursor.execute(sql, (idMascotaBuscada,))
                resultado = mycursor.fetchone()
                if(resultado == None):
                #Funcion registrar mascota
                    listRetorno.append(mascotaNoExiste)
                    return listRetorno
            else:
                listRetorno.append(malCodigo)
                return listRetorno


        #Metodos relacionados con la validación del terminal

        def validarConexionInternet(self):
            try:
                socket.create_connection(('Google.com',80))
                return True
            except OSError:
                return False    
                
        def validarLlaveConServidor(self, llaveEntrada):

            #uic.loadUi("Proyecto-PetRecord/Complementos/AbstracMedico.ui", self)

            if(llaveEntrada == ''):
                 return False

            mycursor.execute(f'SELECT Llaves FROM keysactivacion WHERE Llaves = {llaveEntrada}')
            resultado = mycursor.fetchone()
            
            if(resultado == None):
                return False
            else:
                mycursor.execute(f'SELECT Veterinaria_idVeterinaria FROM Keysactivacion WHERE Llaves = {llaveEntrada}')
                idVetActual = mycursor.fetchone()
                
                mycursor.execute(f'SELECT Veterinaria_nombreVeterinaria FROM Keysactivacion WHERE Llaves = {llaveEntrada}')
                nombreVetActual = mycursor.fetchone()
                self.activarTokenDeActivacion(idVetActual[0], nombreVetActual[0])
                return True

        def activarTokenDeActivacion(self, idVet, nombreVet):
            self.tokenActivacion = True
            sql = 'INSERT INTO terminalveterinario (idTerminalVeterinario, tokenDeActivación, Veterinaria_idVeterinaria, Veterinaria_nombreVeterinaria) VALUES (%s,%s,%s,%s)'
            val = (str(self.id),self.tokenActivacion,idVet,nombreVet)
            mycursor.execute(sql, val)
            db.commit()
            # Se setean los atributos de la clase cuando se activa el token
            self.consultaBDtokenDeActivacion()
            #self.cargarScreenBuscarMascota() #se carga la screen buscarMascota

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
                    return False
                elif(resultado[0] == 1):
                    self.tokenActivacion = True
                    return True
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