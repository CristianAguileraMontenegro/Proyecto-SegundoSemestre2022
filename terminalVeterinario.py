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
from insumos import insumoVeterinario

db = mysql.connector.connect(
    user='piero',
    password='pieron123',
    host='localhost',
    database='mydb',
    port='3306'
)

mycursor = db.cursor(buffered=True)

if __name__ != "__main__":
    class Terminal:

        def __init__(self):

            self.id = self.generarIdTerminal()
            self.tokenActivacion = None
            self.idVeterinaria = None
            self.nombreVeterinaria = None
            self.mascotas:Mascota = []
            self.mascotasExternas:Mascota = [] #masconas no pertenecientes a la veterinrias
            self.calendaio = Calendario()
            self.insumos:insumoVeterinario = []

            self.validarTokenDeActivacion()
            

            if (self.tokenActivacion == True):
                # De ser el caso que el token esta ya activado, se instancian aquí, debido a que actToken no se llamará
                print("hola qtrtr")

                self.setIdVeterinaria()
                self.setNombreVeterinaria()
                self.setMascotas()
                self.setCalendario() #las veterinarias tendran calendario independiente de si tienen o no pacientes

        def setIdVeterinaria(self):
            db.commit()
            sql = 'SELECT Veterinaria_idVeterinaria FROM TerminalVeterinario WHERE idTerminalVeterinario = (%s)'
            mycursor.execute(sql, (str(self.id),))
            idVet = mycursor.fetchone()
            self.idVeterinaria = idVet[0]

        def setNombreVeterinaria(self):
            db.commit()
            sql = 'SELECT Veterinaria_nombreVeterinaria FROM TerminalVeterinario WHERE idTerminalVeterinario = (%s)'
            mycursor.execute(sql, (str(self.id),))
            nombreVet = mycursor.fetchone()
            self.nombreVeterinaria = nombreVet[0]
        
        def setMascotas(self):
            db.commit()
            sql = 'SELECT Mascota_idMascota FROM Mascota_has_TerminalVeterinario as maste join terminalveterinario as termi on termi.IdTerminalVeterinario = maste.TerminalVeterinario_idTerminalVeterinario join veterinaria as veti on veti.idVeterinaria = termi.Veterinaria_idVeterinaria WHERE veti.idVeterinaria = (%s)'
            mycursor.execute(sql, (str(self.idVeterinaria),))
            ids = mycursor.fetchall()
            for i in range(len(ids)):
                print("67 terminal :"+str(ids[i][0]))
                mascotalol= Mascota(str(ids[i][0]))
                self.mascotas.append(mascotalol)
        
        def setMascotaOtraVeterinaria(self, idMascota): #seteamos la mascota de otra veterinaria para esta vaterinaria
            mascotalol= Mascota(str(idMascota)) #en los otros metodos como busquedaLocal2 obtendremos solo los datos asociados a esta veterinaria
            self.mascotas.append(mascotalol)
        
        def setMascotaEspecifica(self, idMascota, mascota:Mascota):

            #sql = 'SELECT * FROM Mascota WHERE idMascota = (%s)'
            #mycursor.execute(sql, (str(ids[i][0]),))
            #resultado = mycursor.fetchone()

            db.commit()

            sql = 'SELECT * FROM Mascota WHERE idMascota = (%s)' #"obtenemos todoas los demas datos de la mascota"
            mycursor.execute(sql, (str(idMascota),))
            resultadoMascota = mycursor.fetchone()

            mascota.setNombreMascota(resultadoMascota[1])
            mascota.setEspecie(resultadoMascota[2])
            mascota.setColorMascota(resultadoMascota[3])
            mascota.setRaza(resultadoMascota[4])
            mascota.setNombreTutor(resultadoMascota[5])
            mascota.setRutTutor(resultadoMascota[6])
            mascota.setNumeroTelefono(resultadoMascota[7])
            mascota.setDireccion(resultadoMascota[8])
            mascota.setFechaNacimiento(resultadoMascota[9])

            sql = 'SELECT idTablaMedica FROM TablaMedica WHERE Veterinaria_idVeterinaria = %s AND Veterinaria_nombreVeterinaria = %s AND Mascota_idMascota = %s' #"obtenemos todoas los demas datos de la mascota"
            mycursor.execute(sql, (str(self.idVeterinaria), str(self.nombreVeterinaria) ,str(idMascota)))
            ResultadoTabla = mycursor.fetchone()

            mascota.agregarTablaMedica(ResultadoTabla[0])

            mascota.solicitarRegistroDeOperacionesEnBaseDeDatos(mycursor)

            mascota.solicitarVacunasEnBaseDeDatos(mycursor)

            mascota.solicitarAlergiasEnBaseDeDatos(mycursor) 
    
            mascota.solicitarFichasParcialesEnBaseDeDatos(mycursor, ResultadoTabla[0])
        

        def getMascota(self, idMascota):
            for mascota in self.mascotas:
                if((mascota.getId() == str(idMascota))): 
                    return mascota
        
        def getMascotaExterna(self, idMascota):
            for mascota in self.mascotasExternas:
                if((mascota.getId() == str(idMascota))): 
                    return mascota
                                                    
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

            mascotaNueva.agregarMascotaEnBaseDeDatos(mycursor, db)    

            mascotaNueva.guardarTablaEnBaseDeDatos(mycursor, db, self.idVeterinaria, self.nombreVeterinaria, id)
            
            mascotaNueva.setAlergiasBas(alergiasFinal, mycursor, db)

            mascotaNueva.agregarTablaMascota(self.id, mycursor, db)
        
        def editarMascota(self, id, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, alergias, fechaNacimiento):
            db.commit()
            for mascota in self.mascotas:
                if (str(mascota.getId()) == str(id)):
                    print("158 terminal")
                    mascota.setNombreMascota(nombre)
                    mascota.setColorMascota(especie)
                    mascota.setEspecie(color)
                    mascota.setRaza(raza)
                    mascota.setNombreTutor(nombreTutor)
                    mascota.setRutTutor(rutTutor)
                    mascota.setNumeroTelefono(numeroTelefono)
                    mascota.setDireccion(direccion)
                    mascota.setFechaNacimiento(fechaNacimiento)

                    alergiasActuales = mascota.getAlergias()

                    alergiasArray = alergias.split(';')
                    alergiaDicc = {}
                    alergiasFinal = []
                    i = 0
                    for alergia in alergiasArray:
                        alergiaDicc = {
                            'id':alergiasActuales[i]['id'],
                            'nombre':alergia
                        }
                        i = i+1
                        alergiasFinal.append(alergiaDicc)
                    
                    mascota.setAlergias(alergiasFinal)

                    mascota.actualizarMascota(mycursor, db)
                    mascota.editarRegistroDeAlergias(mycursor, db)
        
        def verificarPresenciaDeTablaDeMascota(self, idMascota):

            sql = 'SELECT idTablaMedica FROM TablaMedica WHERE Veterinaria_idVeterinaria = %s AND Veterinaria_nombreVeterinaria = %s AND Mascota_idMascota = %s' #"obtenermos el id de la tablaMedica para verificar si la macota ya posee una en la veterinaira actual"
            mycursor.execute(sql, (str(self.idVeterinaria), str(self.nombreVeterinaria) ,str(idMascota)))
            ResultadoTabla = mycursor.fetchone()

            return ResultadoTabla
        
        def agregarMascotaDesdeAbstractPrimeraVez(self, idMascota, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, alergias, tablaMedicaId, fechaNacimiento):

            for mascota in self.mascotas:
                if((mascota.getId() == str(idMascota))):
                    
                    mascota.setNombreMascota(nombre)
                    mascota.setEspecie(especie)
                    mascota.setColorMascota(color)
                    mascota.setRaza(raza)
                    mascota.setNombreTutor(nombreTutor)
                    mascota.setRutTutor(rutTutor)
                    mascota.setNumeroTelefono(numeroTelefono)
                    mascota.setDireccion(direccion)
                    mascota.setFechaNacimiento(fechaNacimiento)

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

                   
                    mascota.agregarTablaMedica(tablaMedicaId) 
                    mascota.guardarTablaEnBaseDeDatos(mycursor, db, self.idVeterinaria, self.nombreVeterinaria, idMascota)
                    mascota.setAlergias(alergiasFinal)
                    #mascota.agregarTablaMascota(self.id, mycursor, db)
                    break

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
            db.commit()
            for mascota in self.mascotas:
                if mascota.getId() == idMascota:
                    mascota.completarFichaParcial(idFicha, mycursor)
        
        def completarFichaParcialMascotasExternas(self, idMascota, idFicha):
            db.commit()
            for mascota in self.mascotasExternas:
                if mascota.getId() == idMascota:
                    print("337 terminal")
                    mascota.completarFichaParcial(idFicha, mycursor)
                    break


        def agregarFichaOperacion(self, idFicha, idMascota, opFicha):
            for mascota in self.mascotas:
                if mascota.getId() == idMascota:

                    operacion = {
                        'id': opFicha['id'],
                        'operacion': opFicha['cirugiaARealizar'],
                     }
                    mascota.agregarOperaciones(operacion, mycursor, db)

                    mascota.setFichaDeOperacion(idFicha, opFicha, mycursor, db)
        
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
        
        def agregarFichaSedacion(self, idFicha, idMascota, sedFicha):
            for mascota in self.mascotas:
                if mascota.getId() == idMascota:
                    mascota.setFichaDeSefacion(idFicha, sedFicha, mycursor, db)

        def agregarFichaHospitalizacion(self, idFicha, idMascota, hospFicha):
            for mascota in self.mascotas:
                if mascota.getId() == idMascota:
                    mascota.setFichaDeHospitalizacion(idFicha, hospFicha, mycursor, db)
        
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
            db.commit()
            sql = 'SELECT * FROM mascota WHERE idMascota = (%s)' #muestra informacion bascia buscar 
            mycursor.execute(sql, (idMascotaBuscada,))
            resultadoMascota = mycursor.fetchone()
            flagMascota = False
            
            if(resultadoMascota != None):
                
                return True
            else:
                return False

        def agregarMascotaRemota(self, idMascotaBuscada):
            mascota = Mascota(idMascotaBuscada)
            self.mascotasExternas.append(mascota)
            return mascota
            
        
        def buscarMascotaRemota2(self, idMascotaBuscada):
            db.commit()
            sql = 'SELECT * FROM mascota WHERE idMascota = (%s)' #muestra informacion bascia buscar 
            mycursor.execute(sql, (idMascotaBuscada,))
            resultadoMascota = mycursor.fetchone()
            flagMascota = False
            
            if(resultadoMascota != None):
                for mascota in self.mascotasExternas:
                    if(mascota.getId() == idMascotaBuscada):
                        sql = 'SELECT idTablaMedica FROM TablaMedica WHERE Mascota_idMascota = %s' #"obtenemos todoas los demas datos de la mascota"
                        mycursor.execute(sql, (str(idMascotaBuscada),))
                        ResultadoTablaX = mycursor.fetchall()

                        mascota.setNombreMascota(resultadoMascota[1])
                        mascota.setEspecie(resultadoMascota[2])
                        mascota.setColorMascota(resultadoMascota[3])
                        mascota.setRaza(resultadoMascota[4])
                        mascota.setNombreTutor(resultadoMascota[5])
                        mascota.setRutTutor(resultadoMascota[6])
                        mascota.setNumeroTelefono(resultadoMascota[7])
                        mascota.setDireccion(resultadoMascota[8])
                        mascota.setFechaNacimiento(resultadoMascota[9])
                        mascota.solicitarAlergiasEnBaseDeDatos(mycursor)

                        idTabla = str(uuid.uuid4())
                        mascota.agregarTablaMedica(idTabla)
                        
                        for ResultadoTabla in ResultadoTablaX:
                            
                            if(flagMascota is False):
                                sql = 'SELECT * FROM RegistroDeOperaciones WHERE TablaMedica_idTablaMedica = (%s)'
                                mycursor.execute(sql, (str(ResultadoTabla[0]),)) #el numero 9 representa el campo 10 de la tabla de mascotas = id tabla medica 
                                registroOp = mycursor.fetchall()

                                sql = 'SELECT * FROM RegistroVacunasSuministradas WHERE TablaMedica_idTablaMedica = (%s)'
                                mycursor.execute(sql, (str(ResultadoTabla[0]),))
                                registroVac = mycursor.fetchall()

                                vacunasFinal = []##arreglo donde se almacena el diccionario de vacunas
                                vacunaDicc = {}
                                    
                                for vacuna in registroVac:
                                    vacunaDicc = {
                                        'id':vacuna[0],
                                        'nomVacuna':vacuna[1]
                                    }
                                    vacunasFinal.append(vacunaDicc)

                                registroOperacionesFinal = []##arreglo donde se almacena el diccionario de registro de Operaciones
                                operacionesDicc = {}
                                for operacion in registroOp:
                                    operacionesDicc = {
                                        'id':operacion[0],
                                        'operacion':operacion[1]
                                    }
                                    registroOperacionesFinal.append(operacionesDicc)

                                mascota.setRegistroDeVacunas(vacunasFinal)
                                mascota.setRegistroDeOperaciones(registroOperacionesFinal)
                                flagMascota = True
                            else:
                                sql = 'SELECT * FROM RegistroDeOperaciones WHERE TablaMedica_idTablaMedica = (%s)'
                                mycursor.execute(sql, (str(ResultadoTabla[0]),)) #el numero 9 representa el campo 10 de la tabla de mascotas = id tabla medica 
                                registroOp = mycursor.fetchall()

                                sql = 'SELECT * FROM RegistroVacunasSuministradas WHERE TablaMedica_idTablaMedica = (%s)'
                                mycursor.execute(sql, (str(ResultadoTabla[0]),))
                                registroVac = mycursor.fetchall()

                                vacunasFinal = []##arreglo donde se almacena el diccionario de vacunas
                                vacunaDicc = {}
                                    
                                for vacuna in registroVac:
                                    vacunaDicc = {
                                        'id':vacuna[0],
                                        'nomVacuna':vacuna[1]
                                    }
                                    mascota.agregarVacunasSinBd(vacunaDicc)
                                
                                registroOperacionesFinal = []##arreglo donde se almacena el diccionario de registro de Operaciones
                                operacionesDicc = {}
                                for operacion in registroOp:
                                    operacionesDicc = {
                                        'id':operacion[0],
                                        'operacion':operacion[1]
                                    }
                                    mascota.agregarOperacionesSinBd(operacionesDicc)

                            mascota.solicitarFichasParcialesEnBaseDeDatos(mycursor, ResultadoTabla[0])
                                
                            #tablaEntregar = TablaMedica(resultadoMascota[9])

                        #self, id, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, tablaMedica
                        
                        
                        #mascotaEncontrada= Mascota(resultadoMascota[0], resultadoMascota[1], resultadoMascota[2], resultadoMascota[3], resultadoMascota[4], resultadoMascota[5], resultadoMascota[6],
                        #                                resultadoMascota[7], resultadoMascota[8], tablaEntregar)

                        


        def buscarMascotaLocal(self, idMascota):
            mascotaEncontrada:Mascota = None
            print("estoy en local con este id :"+ str(idMascota))
            print("largo de masctoa :"+ str(idMascota))
            for mascota in self.mascotas:
                
                if((mascota.getId() == str(idMascota))): #si se encuentra se cargan los datos restantes
                    return True

            return False
        
        def buscarMascotaLocal2(self, idMascota):
            for mascota in self.mascotas:
                if((mascota.getId() == str(idMascota))): #si se encuentra se cargan los datos restantes
                    self.setMascotaEspecifica(idMascota, mascota)

                
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
                print("codigo dentro de terminal 665 :"+ str(flagMascotaEnc))
                if(flagMascotaEnc):
                    mascotaBuscada = self.buscarMascotaLocal(idMascotaBuscada)

                    if(mascotaBuscada is True):
                        listRetorno.append(mascotaLocal)
                        listRetorno.append(idMascotaBuscada)
                        return listRetorno

                elif(flagMascotaEnc == False):
                    mascotaBuscada = self.buscarMascotaRemota(idMascotaBuscada)
                    if(mascotaBuscada is True):

                        listRetorno.append(mascotaRemote)
                        listRetorno.append(idMascotaBuscada)
                        return listRetorno
                
                db.commit()
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
            db.commit()
            if(llaveEntrada == ''):
                 return False

            sql = 'SELECT Llaves FROM keysactivacion WHERE Llaves = (%s)' #ocupamos sql para la consulta ya que si se aplica directamente en my cursos general problemas
            mycursor.execute(sql, (llaveEntrada,))
            resultado = mycursor.fetchone()

            print("615 terminal "+str(resultado))
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
            self.setCalendario()
        
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
            db.commit()
            sql = 'SELECT * FROM mascota WHERE idMascota = (%s)' #muestra informacion bascia buscar 
            mycursor.execute(sql, (idMascota,))
            resultado = mycursor.fetchone()
            return resultado

        def getMedicamentosConsulta(self, idFicha, idMascota):

            for mascota in self.mascotasExternas:
                if(mascota.getId() == str(idMascota)):
                    return mascota.getMedicamentosConsulta(idFicha)
        
        #calendario
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------         
        def setCalendario(self):
            db.commit()
            sql = 'SELECT idCalendario FROM calendario WHERE (Veterinaria_idVeterinaria, Veterinaria_nombreVeterinaria) = (%s, %s)'
            mycursor.execute(sql, (str(self.idVeterinaria), str(self.nombreVeterinaria)))
            Resultado = mycursor.fetchone()
            print("181 termianl "+str(Resultado))
            if(Resultado == None):
                self.crearCalendario()
            else:
                self.calendaio.setId(Resultado[0])
                self.solicitarDatosCalendarioBaseDeDatos()

        def crearCalendario(self):
            idCalendario = (uuid.uuid4())
            self.calendaio.setId(idCalendario)
            self.calendaio.agregarCalendarioBaseDeDatos(self.idVeterinaria, self.nombreVeterinaria, mycursor, db)
        
        def solicitarDatosCalendarioBaseDeDatos(self):
            self.calendaio.solicitarDatosCalendarioBaseDeDatos(mycursor)
        
        def getIdCalendario(self):
            return self.calendaio.getId()
        
        def getFechasCalendario(self):
            return self.calendaio.getFechas()
        
        def getFechaCalendario(self, fechaSeleccionada):
            return self.calendaio.getFecha(fechaSeleccionada)
        
        def verificarFechaCalendario(self, fecha):
            return self.calendaio.verificarFecha(fecha)
        
        def verificarFechaEnHorario(self, fecha, horaInicial, horaFinal):
            return self.calendaio.verificarFechaHorario(fecha, horaInicial, horaFinal) 
        
        def agregarFechasCalendario(self, fechas):
            self.calendaio.agregarFechas(fechas,mycursor, db)
        
        def agregarDatosAFechasCalendario(self, fechaSeleccionada, rutIngresado, numeroIngresado, horaInicialSeleccionada, minutosInicialSeleccionados, horaFinalSeleccionada, minutosFinalSeleccionada):
            self.calendaio.agregarDatosAFecha(fechaSeleccionada, rutIngresado, numeroIngresado, horaInicialSeleccionada, minutosInicialSeleccionados, horaFinalSeleccionada, minutosFinalSeleccionada, mycursor, db)
        
        def editarDatosDeFecha(self, fechaSeleccionada, rutIngresado, numeroIngresado, horaInicialSeleccionada, minutosInicialSeleccionados, horaFinalSeleccionada, minutosFinalSeleccionada, cita):
            self.calendaio.editarDatosDeFecha(fechaSeleccionada, rutIngresado, numeroIngresado, horaInicialSeleccionada, minutosInicialSeleccionados, horaFinalSeleccionada, minutosFinalSeleccionada, cita, mycursor, db)
        
        def eliminarDatosDeFecha(self, fechaSeleccionada, cita):
            self.calendaio.eliminarDatosDeFecha(fechaSeleccionada, cita, mycursor, db)
        
        def getRutsMascota(self):
            ruts = []
            for mascota in self.mascotas:
                sql = 'SELECT rutTutor FROM mascota WHERE idMascota = (%s)'
                mycursor.execute(sql, (str(mascota.getId()),))
                rutsB = mycursor.fetchone()

                ruts.append(str(rutsB[0]))
            
            print("735 : "+str(ruts))
            return ruts
        
        def getNumeroTelefonoMascota(self):
            numeros = []
            for mascota in self.mascotas:
                sql = 'SELECT numeroTelefono FROM mascota WHERE idMascota = (%s)'
                mycursor.execute(sql, (str(mascota.getId()),))
                numero = mycursor.fetchone()

                numeros.append(str(numero[0]))
            return numeros

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
#-----------Insumo

        def setInsumos(self):
            db.commit()
            sql = 'SELECT idInsumo FROM Insumos WHERE Veterinaria_idVeterinaria = (%s) AND Veterinaria_nombreVeterinaria = (%s)'
            mycursor.execute(sql, (str(self.idVeterinaria), str(self.nombreVeterinaria)))
            datosInsumos = mycursor.fetchone()
            
            for i in range(len(datosInsumos)):
                insumo = insumoVeterinario(datosInsumos[i])
                insumo.obtenerDatosBaseDeDatos(db, mycursor)
                self.insumos.append(insumo)
        
        def getNombreInsumo(self, idInsumo):
            for i in range(len(self.insumos)):
                if(str(self.insumos[i].getId()) == str(idInsumo)):
                    return self.insumos[i].getNombreDeInsumo()
            return False
        
        def getPrecioInsumo(self, idInsumo):
            for i in range(len(self.insumos)):
                if(str(self.insumos[i].getId()) == str(idInsumo)):
                    return self.insumos[i].getPrecioInsumo()
            return False
        
        def getIdInsumos(self):
            idInsumos = []
            for i in range(len(self.insumos)):
                idInsumos.append(self.insumos[i].getId())
            return idInsumos


#-----------Insumo
#-----------rECETA

        def agregarReceta(self, idFicha, idMascota, receta):
            for mascota in self.mascotas:
                if mascota.getId() == idMascota:
                    mascota.setReceta(idFicha, receta, mycursor, db)
        
        def editarReceta(self, idMascota, idFicha, rutVeterinario, preescripcion, fechaUltimaModificacion):

            for mascota in self.mascotas:
                if mascota.getId() == idMascota:
                            
                    idReceta = mascota.getIdReceta(idFicha)

                    receta = { #al ser una ficha se guarda directamente en el tributo relerente al diccionario
                        'id' : idReceta,
                        'rutVeterinario' : rutVeterinario,
                        'preescripcion' : preescripcion
                    }

                    mascota.editarReceta(idFicha, receta, fechaUltimaModificacion, mycursor, db)