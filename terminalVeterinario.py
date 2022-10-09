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
from calendario import Calendario

db = mysql.connector.connect(
    user='piero',
    password='pieron123',
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
            self.mascotasExternas:Mascota = [] #masconas no pertenecientes a la veterinrias
            self.calendaio:Calendario

            self.validarTokenDeActivacion()

            if (self.tokenActivacion == True):
                # De ser el caso que el token esta ya activado, se instancian aquí, debido a que actToken no se llamará
                self.setIdVeterinaria()
                self.setNombreVeterinaria()
                print("46 terminalVterinario")
                self.setMascotas()
                self.setCalendario()

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
                print("67 terminal")
                mascotalol= Mascota(str(ids[i][0]))
                self.mascotas.append(mascotalol)
        
        def setMascotaOtraVeterinaria(self, idMascota):
            mascotalol= Mascota(str(idMascota))
            self.mascotasExternas.append(mascotalol)
            self.setMascotaEspecifica(idMascota, mascotalol)


        
        def setMascotaOtraVeterinariaBeta(self, idMascota):
            sql = 'SELECT idMascota FROM mascota WHERE idMascota = (%s)'
            mycursor.execute(sql, (str(self.idVeterinaria),))
            ids = mycursor.fetchall()
            for i in range(len(ids)):
                print("67 terminal")
                mascotalol= Mascota(str(ids[i][0]))
                self.mascotas.append(mascotalol)
        
        def setMascotaEspecifica(self, idMascota, mascota:Mascota):

            #sql = 'SELECT * FROM Mascota WHERE idMascota = (%s)'
            #mycursor.execute(sql, (str(ids[i][0]),))
            #resultado = mycursor.fetchone()

            print(str(idMascota)+" el id del se5t")

            sql = 'SELECT * FROM Mascota WHERE idMascota = (%s)' #"obtenemos todoas los demas datos de la mascota"
            mycursor.execute(sql, (str(idMascota),))
            resultadoMascota = mycursor.fetchone()

            print(str(resultadoMascota))
            sql = 'SELECT * FROM RegistroDeOperaciones WHERE TablaMedica_idTablaMedica = (%s)'
            mycursor.execute(sql, (str(resultadoMascota[9]),)) #el numero 9 representa el campo 10 de la tabla de mascotas = id tabla medica 
            registroOp = mycursor.fetchall()

            sql = 'SELECT * FROM RegistroVacunasSuministradas WHERE TablaMedica_idTablaMedica = (%s)'
            mycursor.execute(sql, (str(resultadoMascota[9]),))
            registroVac = mycursor.fetchall()

            vacunasFinal = []##arreglo donde se almacena el diccionario de vacunas
            vacunaDicc = {}
                
            for vacuna in registroVac:
                vacunaDicc = {
                    'id':vacuna[0],
                    'nomVacuna':vacuna[1]
                }
                vacunasFinal.append(vacunaDicc)

            sql = 'SELECT * FROM Alergias WHERE TablaMedica_idTablaMedica = (%s)'
            mycursor.execute(sql, (str(resultadoMascota[9]),))
            alergiasEntregar = mycursor.fetchall()

            alergiaFinal = []##arreglo donde se almacena el diccionario de alergias
            alergiaDicc = {}
                
            for alergia in alergiasEntregar:
                alergiaDicc = {
                    'id':alergia[0],
                    'nombre':alergia[1]
                }
                alergiaFinal.append(alergiaDicc)
            

            registroOperacionesFinal = []##arreglo donde se almacena el diccionario de registro de Operaciones
            operacionesDicc = {}
            for operacion in registroOp:
                operacionesDicc = {
                    'id':operacion[0],
                    'operacion':operacion[1]
                }
                registroOperacionesFinal.append(operacionesDicc)
            
            
                
            #tablaEntregar = TablaMedica(resultadoMascota[9])

            #self, id, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, tablaMedica
            
            mascota.setNombreMascota(resultadoMascota[1])
            mascota.setEspecie(resultadoMascota[2])
            mascota.setColorMascota(resultadoMascota[3])
            mascota.setRaza(resultadoMascota[4])
            mascota.setNombreTutor(resultadoMascota[5])
            mascota.setRutTutor(resultadoMascota[6])
            mascota.setNumeroTelefono(resultadoMascota[7])
            mascota.setDireccion(resultadoMascota[8])
            mascota.agregarTablaMedica(resultadoMascota[9])
            
            #mascotaEncontrada= Mascota(resultadoMascota[0], resultadoMascota[1], resultadoMascota[2], resultadoMascota[3], resultadoMascota[4], resultadoMascota[5], resultadoMascota[6],
            #                                resultadoMascota[7], resultadoMascota[8], tablaEntregar)

            mascota.setAlergias(alergiaFinal)
            print("192 :"+str(mascota.getAlergias()))
            mascota.setRegistroDeVacunas(vacunasFinal)
            mascota.setRegistroDeOperaciones(registroOperacionesFinal)
            mascota.solicitarFichasParcialesEnBaseDeDatos(mycursor)
            
            #tablaEntregar.setAlergias(alergiaFinal)
            #tablaEntregar.setRegistroDeVacunas(vacunasFinal)
            #tablaEntregar.setRegistroDeOperaciones(registroOperacionesFinal)
                
            #tablaEntregar.solicitarFichasEnBaseDeDatos()#solicitamos las fichas correspondientes a la tabla, si embargo solo se solicitan los datos necesarios como fecha e id para realizar consultas mas rapidamente
                #print(str(tablaEntregar.getIdsFichas()))

            
        
        def setCalendario(self):
            sql = 'SELECT idCalendario FROM calendario WHERE (Veterinaria_idVeterinaria, Veterinaria_nombreVeterinaria) = (%s, %s)'
            mycursor.execute(sql, (str(self.idVeterinaria), str(self.nombreVeterinaria)))
            self.calendaio = Calendario(mycursor.fetchone())
        
        def getIdCalendario(self):
            return self.calendaio.getId()
        
        def agregarMascota(self, id, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, alergias, tablaMedica, fechaNacimiento):
            mascotaNueva = Mascota(id, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, tablaMedica,  fechaNacimiento)

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

            mascotaNueva.guardarTablaEnBaseDeDatos(mycursor, db)
            
            mascotaNueva.setAlergiasBas(alergiasFinal, mycursor, db)

            mascotaNueva.agregarMascotaEnBaseDeDatos(mycursor, db) 

            mascotaNueva.agregarTablaMascota(self.id, mycursor, db)
            

        def agregarFichaMedica(self, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, idMascota, tratamientos, causaVisita, medicamentos, vacunas):
            idFicha = uuid.uuid4()
            for mascota in self.mascotas:
                if mascota.getId() == idMascota:
                    mascota.agregarFichaMedicaConsultaATabla(idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, mycursor, db)
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
                    mascota.setTratamientos(tratClase, mycursor, db)

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
                    mascota.setMedicamentos(medClase, mycursor, db)

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
                        mascota.agregarVacunas(vacDicc, mycursor, db) #agregamos las vacunas indicadas a la tabla 
                    mascota.setVacunas(vacClase, mycursor, db) #seteamos las vacunas en la ficha
           

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
        
        def editarFichaMedica(self, idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, idMascota, tratamientos, causaVisita, medicamentos, vacunas, fechaModificacion):
            
            for mascota in self.mascotas:
                if mascota.getId() == idMascota:

                    #agregamos los demas datos
                    tratamientosID = mascota.getTratamiento(idFicha)
                    tratamientosA = tratamientos.split(';')
                    tratClase = []
                    tratDicc = {}
                    i = 0
                    for trat in tratamientosA:
                        tratDicc = {
                            'id' : tratamientosID[i]['id'],
                            'nombreTratamiento': trat,
                            'causaVisita' : causaVisita,
                        }
                        i = i+1
                        tratClase.append(tratDicc)

                    medicamentosID = mascota.getMedicamentosConsulta(idFicha)
                    medicamentosA = medicamentos.split(';')
                    medClase = []
                    medDicc = {}
                    i = 0
                    for med in medicamentosA:
                        medDicc = {
                            'id' : medicamentosID[i]['id'],
                            'nomMedicamento' : med,
                        }
                        i = i+1
                        medClase.append(medDicc)
        
                    vacunasID = mascota.getVacunasSuministradasConsulta(idFicha)
                    vacunasA = vacunas.split(';')
                    vacClase = []
                    vacDicc = {}
                    i = 0
                    for vac in vacunasA:
                        vacDicc = {
                            'id' : vacunasID[i]['id'],
                            'nomVacuna' : vac,
                        }    
                        i = i+1
                        vacClase.append(vacDicc)
                    
                    mascota.editarFichaMedicaConsulta(idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, mycursor, db, fechaModificacion, vacClase, medClase, tratClase) #modificamos los datos de la ficha primeramente
                    break

        def completarFichaParcial(self, idMascota, idFicha):
            for mascota in self.mascotas:
                print("307 terminalveterinario "+str(mascota.getId()))
                if mascota.getId() == idMascota:
                    
                    mascota.completarFichaParcial(idFicha, mycursor)
        
        def completarFichaParcialMascotasExternas(self, idMascota, idFicha):
            #medicamentos = []
            for mascota in self.mascotasExternas:

                if mascota.getId() == idMascota:
                    print("337 terminal")
                    mascota.completarFichaParcial(idFicha, mycursor)
                    break


        def agregarFichaOperacion(self, idMascota, opFicha):
            for mascota in self.mascotas:
                if mascota.getId() == idMascota:

                    operacion = {
                        'id': opFicha['id'],
                        'operacion': opFicha['cirugiaARealizar'],
                     }
                    mascota.agregarOperaciones(operacion, mycursor, db)

                    mascota.setFichaDeOperacion(opFicha, mycursor, db)
        
        def editarFichaOperacion(self, idMascota, idFicha, diagnostico, cirugia, fechaUltimaModificacion):

            for mascota in self.mascotas:
                if mascota.getId() == idMascota:
                            
                    idOperacion = mascota.getIdOperacion(idFicha)

                    opFicha = { #al ser una ficha se guarda directamente en el tributo relerente al diccionario
                        'id':idOperacion,
                        'diagnostico':diagnostico,
                        'cirugiaARealizar':cirugia,
                        'autTutor': True
                    }
                    operacion = {
                        'id': opFicha['id'],
                        'operacion': opFicha['cirugiaARealizar'],
                     }
                    mascota.editarRegistroDeOperaciones(operacion, mycursor, db)

                    mascota.editarFichaOperacion(idFicha, opFicha, fechaUltimaModificacion, mycursor, db)
        
        def agregarFichaSedacion(self, idMascota, sedFicha):
            for mascota in self.mascotas:
                if mascota.getId() == idMascota:
                    mascota.setFichaDeSefacion(sedFicha, mycursor, db)

        def agregarFichaHospitalizacion(self, idMascota, hospFicha):
            for mascota in self.mascotas:
                if mascota.getId() == idMascota:
                    mascota.setFichaDeHospitalizacion(hospFicha, mycursor, db)
        
        def editarFichaHospitalizacion(self, idMascota, idFicha, motivoHospitalización, fechaUltimaModificacion):

            for mascota in self.mascotas:
                if mascota.getId() == idMascota:
                            
                    idHospitalizacion = mascota.getIdHospitalizacion(idFicha)

                    hospFicha = { #al ser una ficha se guarda directamente en el tributo relerente al diccionario
                        'id':idHospitalizacion,
                        'motivo':motivoHospitalización
                    }

                    mascota.editarFichaHospitalizacion(idFicha, hospFicha, fechaUltimaModificacion, mycursor, db)


        def buscarMascotaRemota(self, idMascotaBuscada):
            sql = 'SELECT * FROM mascota WHERE idMascota = (%s)' #muestra informacion bascia buscar 
            mycursor.execute(sql, (idMascotaBuscada,))
            resultadoMascota = mycursor.fetchone()

            
            if(resultadoMascota != None):
                
                for mascota in self.mascotas: #indica que la mascota pertenece a la veterinraia actual
                    if(mascota.getId() == str(idMascotaBuscada)): #si se encuentra se cargan los datos restantes
                        print("Estoy en remoto "+ str(resultadoMascota))
                        sql = 'SELECT * FROM RegistroDeOperaciones WHERE TablaMedica_idTablaMedica = (%s)'
                        mycursor.execute(sql, (str(resultadoMascota[9]),)) #el numero 9 representa el campo 10 de la tabla de mascotas = id tabla medica 
                        registroOp = mycursor.fetchall()

                        sql = 'SELECT * FROM RegistroVacunasSuministradas WHERE TablaMedica_idTablaMedica = (%s)'
                        mycursor.execute(sql, (str(resultadoMascota[9]),))
                        registroVac = mycursor.fetchall()

                        vacunasFinal = []##arreglo donde se almacena el diccionario de vacunas
                        vacunaDicc = {}
                            
                        for vacuna in registroVac:
                            vacunaDicc = {
                                'id':vacuna[0],
                                'nomVacuna':vacuna[1]
                            }
                            vacunasFinal.append(vacunaDicc)

                        sql = 'SELECT * FROM Alergias WHERE TablaMedica_idTablaMedica = (%s)'
                        mycursor.execute(sql, (str(resultadoMascota[9]),))
                        alergiasEntregar = mycursor.fetchall()

                        alergiaFinal = []##arreglo donde se almacena el diccionario de alergias
                        alergiaDicc = {}
                            
                        for alergia in alergiasEntregar:
                            alergiaDicc = {
                                'id':alergia[0],
                                'nombre':alergia[1]
                            }
                            alergiaFinal.append(alergiaDicc)

                        registroOperacionesFinal = []##arreglo donde se almacena el diccionario de registro de Operaciones
                        operacionesDicc = {}
                        for operacion in registroOp:
                            operacionesDicc = {
                                'id':operacion[0],
                                'operacion':operacion[1]
                            }
                            registroOperacionesFinal.append(operacionesDicc)
                            
                        #tablaEntregar = TablaMedica(resultadoMascota[9])

                        #self, id, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, tablaMedica
                        mascota.setNombreMascota(resultadoMascota[1])
                        mascota.setEspecie(resultadoMascota[2])
                        mascota.setColorMascota(resultadoMascota[3])
                        mascota.setRaza(resultadoMascota[4])
                        mascota.setNombreTutor(resultadoMascota[5])
                        mascota.setRutTutor(resultadoMascota[6])
                        mascota.setNumeroTelefono(resultadoMascota[7])
                        mascota.setDireccion(resultadoMascota[8])
                        mascota.agregarTablaMedica(resultadoMascota[9])
                        
                        #mascotaEncontrada= Mascota(resultadoMascota[0], resultadoMascota[1], resultadoMascota[2], resultadoMascota[3], resultadoMascota[4], resultadoMascota[5], resultadoMascota[6],
                        #                                resultadoMascota[7], resultadoMascota[8], tablaEntregar)

                        mascota.setAlergias(alergiaFinal)
                        mascota.setRegistroDeVacunas(vacunasFinal)
                        mascota.setRegistroDeOperaciones(registroOperacionesFinal)
                        mascota.solicitarFichasParcialesEnBaseDeDatos(mycursor)

                        print("dentro de remoto lol")
                        return mascota
                
                if(len(self.mascotas) == 0):
                        mascota = Mascota(idMascotaBuscada)

                        sql = 'SELECT * FROM RegistroDeOperaciones WHERE TablaMedica_idTablaMedica = (%s)'
                        mycursor.execute(sql, (str(resultadoMascota[9]),)) #el numero 9 representa el campo 10 de la tabla de mascotas = id tabla medica 
                        registroOp = mycursor.fetchall()

                        sql = 'SELECT * FROM RegistroVacunasSuministradas WHERE TablaMedica_idTablaMedica = (%s)'
                        mycursor.execute(sql, (str(resultadoMascota[9]),))
                        registroVac = mycursor.fetchall()

                        vacunasFinal = []##arreglo donde se almacena el diccionario de vacunas
                        vacunaDicc = {}
                            
                        for vacuna in registroVac:
                            vacunaDicc = {
                                'id':vacuna[0],
                                'nomVacuna':vacuna[1]
                            }
                            vacunasFinal.append(vacunaDicc)

                        sql = 'SELECT * FROM Alergias WHERE TablaMedica_idTablaMedica = (%s)'
                        mycursor.execute(sql, (str(resultadoMascota[9]),))
                        alergiasEntregar = mycursor.fetchall()

                        alergiaFinal = []##arreglo donde se almacena el diccionario de alergias
                        alergiaDicc = {}
                            
                        for alergia in alergiasEntregar:
                            alergiaDicc = {
                                'id':alergia[0],
                                'nombre':alergia[1]
                            }
                            alergiaFinal.append(alergiaDicc)

                        registroOperacionesFinal = []##arreglo donde se almacena el diccionario de registro de Operaciones
                        operacionesDicc = {}
                        for operacion in registroOp:
                            operacionesDicc = {
                                'id':operacion[0],
                                'operacion':operacion[1]
                            }
                            registroOperacionesFinal.append(operacionesDicc)
                            
                        #tablaEntregar = TablaMedica(resultadoMascota[9])

                        #self, id, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, tablaMedica
                        mascota.setNombreMascota(resultadoMascota[1])
                        mascota.setEspecie(resultadoMascota[2])
                        mascota.setColorMascota(resultadoMascota[3])
                        mascota.setRaza(resultadoMascota[4])
                        mascota.setNombreTutor(resultadoMascota[5])
                        mascota.setRutTutor(resultadoMascota[6])
                        mascota.setNumeroTelefono(resultadoMascota[7])
                        mascota.setDireccion(resultadoMascota[8])
                        mascota.agregarTablaMedica(resultadoMascota[9])
                        
                        #mascotaEncontrada= Mascota(resultadoMascota[0], resultadoMascota[1], resultadoMascota[2], resultadoMascota[3], resultadoMascota[4], resultadoMascota[5], resultadoMascota[6],
                        #                                resultadoMascota[7], resultadoMascota[8], tablaEntregar)

                        mascota.setAlergias(alergiaFinal)
                        mascota.setRegistroDeVacunas(vacunasFinal)
                        mascota.setRegistroDeOperaciones(registroOperacionesFinal)
                        mascota.solicitarFichasParcialesEnBaseDeDatos(mycursor)
                        self.mascotasExternas.append(mascota)

                        return mascota
                

        def buscarMascotaLocal(self, idMascota):
            mascotaEncontrada:Mascota = None
            print("estoy en local con este id :"+ str(idMascota))
            print("largo de masctoa :"+ str(idMascota))
            for mascota in self.mascotas:
                
                if((mascota.getId() == str(idMascota))): #si se encuentra se cargan los datos restantes
                    self.setMascotaEspecifica(idMascota, mascota)
                    mascotaEncontrada = mascota

            return mascotaEncontrada

        
        def verificarMascotaEnSistema(self, codigoMascotaGUI): #debe ser adaptado y modificado para las nuevas screens
            malCodigo = "MalCodigo"
            mascotaLocal = "MascotaLocal"
            mascotaRemote = "MascotaRemota"
            mascotaNoExiste = "MascotaNoExiste"
            listRetorno = []
            print("codigo dentro de terminal :"+ str(codigoMascotaGUI))
            if(codigoMascotaGUI != ""): #& len(self.inputBuscar.text()) == 15):
                #self.MensajeErrorBusqueda.setVisible(False)
                idMascotaBuscada = codigoMascotaGUI
                flagMascotaEnc = False 
                for mascota in self.mascotas:
                    if(mascota.getId() == str(idMascotaBuscada)):
                        flagMascotaEnc = True
                
                if(flagMascotaEnc):
                    mascotaBuscada = self.buscarMascotaLocal(idMascotaBuscada)
                    print(str(mascotaBuscada.getId()))
                    listRetorno.append(mascotaLocal)
                    listRetorno.append(idMascotaBuscada)
                    return listRetorno
                elif(flagMascotaEnc == False):
                    mascotaBuscada = self.buscarMascotaRemota(idMascotaBuscada)
                    print(str(mascotaBuscada))
                    if(mascotaBuscada != None):
                        listRetorno.append(mascotaRemote)
                        listRetorno.append(idMascotaBuscada)
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

        def getDatosBasicosMascota(self, idMascota):
            sql = 'SELECT * FROM mascota WHERE idMascota = (%s)' #muestra informacion bascia buscar 
            mycursor.execute(sql, (idMascota,))
            resultado = mycursor.fetchone()
            return resultado

        def getMedicamentosConsulta(self, idFicha, idMascota):

            for mascota in self.mascotasExternas:
                if(mascota.getId() == str(idMascota)):
                    return mascota.getMedicamentosConsulta(idFicha)
                