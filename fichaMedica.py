from typing_extensions import Self
import mysql.connector


db = mysql.connector.connect(
    user='root',
    password='root',
    host='localhost',
    database='mydb',
    port='3306'
)

mycursor = db.cursor()

class FichaMedica:

    def __init__(self, idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, idTabla):
        
        self.idFicha = idFicha
        self.idTabla = idTabla
        self.idSucursalVeterinaria = sucursalVeterinaria
        self.veterinarioACargo = veterinarioACargo
        self.fechaConsulta = fechaConsulta

        self.medicamentosConsulta = [] #arreglo de diccionario porque pueden ser mas de uno 
        self.vacunasSuministradasConsulta = []
        self.tratamientoConsulta = []

        self.frecRespiratoria = frecRespiratoria
        self.frecCardiaca = frecCardiaca
        self.peso = peso
        self.edad = edad
        self.temperatura = temp

        self.operacion = operacion #indicar boolean
        self.operacionFicha = None #diccionario
        self.hospitalizacion = hospitalizacion #indicar boolean
        self.hospitalizacionFicha = None #diccionario
        self.sedacion = sedacion #indicar boolean
        self.sedacionFicha = None #diccionario

        
        

    def editarFichaMedica(self):
        pass

    def crearFichaMedica(self):
        pass

    def editarFichaMedica(self):
        pass

    def crearFichaMedica(self):
        pass

#getters
    def getId(self):
        return self.id

    def getIdTabla(self):
        return self.idTabla
    
    def getSucursalVeterinaria(self):
        return self.sucursalVeterinaria

    def getTemp(self):
        return self.temp

    def getVeterinarioACargo(self):
        return self.veterinarioACargo

    def getFechaConsulta(self):
        return self.fechaConsulta

    def getMedicamentosConsulta(self):
        return self.medicamentosConsulta

    def getOperacion(self):
        return self.operacion

    def getOperacionFicha(self):
        return self.operacionFicha
    
    def getVacunasSuministradasConsulta(self):
        return self.vacunasSuministradasConsulta

    def getFrecRespiratoria(self):
        return self.frecRespiratoria
    
    def getFrecCardiaca(self):
        return self.frecCardiaca
    
    def getPeso(self):
        return self.peso
    
    def getEdad(self):
        return self.edad
    
    def getHospitalizacion(self):
        return self.hospitalizacion
    
    def getHospitalizacionFicha(self):
        return self.hospitalizacionFicha
    
    def getSedacion(self):
        return self.sedacion
    
    def getSedacioFicha(self):
        return self.sedacionFicha
    
    def getTratamiento(self):
        return self.tratamientoConsulta

#setters 

    def setId(self, id):
        self.id = id

    def setIdTabla(self, idTabla):
        self.idTabla = idTabla
    
    def setSucursalVeterinaria(self, sucursalVeterinaria):
        self.sucursalVeterinaria = sucursalVeterinaria
    
    def setVeterinarioACargo(self, veterinarioACargo):
        self.veterinarioACargo = veterinarioACargo
    
    def setFechaConsulta(self, fechaConsulta):
        self.fechaConsulta = fechaConsulta

    def setOperacion(self, operacion):
        self.operacion = operacion

    def setFrecRespiratoria(self, frecRespiratoria):
        self.frecRespiratoria = frecRespiratoria

    def setFrecCardiaca(self, frecCardiaca):
        self.frecCardiaca = frecCardiaca

    def setPeso(self, peso):
        self.peso = peso

    def setEdad(self, edad):
        self.edad = edad

    def setHospitalizacion(self, hospitalizacion):
        self.hospitalizacion = hospitalizacion

    def setSedacion(self, sedacion):
        self.sedacion = sedacion

    def setTemp(self, temp):
        self.temp = temp

    def solicitarFichaDeOperacionEnBaseDeDatos(self):
        sql = 'SELECT * FROM fichaOperación WHERE FichaMedica_idFichaMedica = (%s)' #se genera la consulta en base al id unico de la ficha medica 
        mycursor.execute(sql, (str(self.id),)) #ejecuta la consulta
        opFicha = mycursor.fetchone() #captura el resultado 
        if(opFicha[3] == 1):
            aut = True #autorización del tutor
        else:
            aut = False
        self.operacionFicha = { #al ser una ficha se guarda directamente en el tributo relerente al diccionario
            'id':opFicha[0],
            'diagnostico':opFicha[1],
            'cirugiaARealizar':opFicha[2],
            'autTutor': aut
        }

    def guardarFichaDeOperacionEnBaseDeDatos(self):
        sql = 'INSERT INTO fichaOperación VALUES (%s, %s, %s, %s, %s, %s)'
        mycursor.execute(sql, (str(self.operacionFicha['id']), str(self.operacionFicha['diagnostico']), str(self.operacionFicha['cirugiaARealizar']), str(self.operacionFicha['autTutor']), str(self.getId()), str(self.getIdTabla())))
        db.commit()

    def setFichaOperacion(self, opFicha):
        self.operacionFicha = opFicha #se guarda el diccionario correpondiente a la ficha de operacion 
        if(self.operacion == 1): #se verifica que la ficha posee una ficha de operación 
            self.guardarFichaDeOperacionEnBaseDeDatos()
    #aqui 22-07-2022 22:58 cristian Aguilera


    #24-07-2022 Cristian Aguilera

    #ficha de hospitalizacion 
    def solicitarFichaDeHospitalizacionEnBaseDeDatos(self):
        if(self.hospitalizacion == 1):
            sql = 'SELECT * FROM FichaHospitalización WHERE FichaMedica_idFichaMedica = (%s)'
            mycursor.execute(sql, (str(self.id),))
            hospiFicha = mycursor.fetchone()
            self.hospitalizacionFicha = { #al ser una ficha se guarda directamente en el tributo relerente al diccionario
                'id':hospiFicha[0],
                'motivo':hospiFicha[1],
            }

    def guardarFichaDeHospitalizacionEnBaseDeDatos(self):
        sql = 'INSERT INTO fichahospitalización VALUES (%s, %s, %s, %s)'
        mycursor.execute(sql, (str(self.hospitalizacionFicha['id']), str(self.hospitalizacionFicha['motivo']), str(self.getId()), str(self.getIdTabla())))
        db.commit()
    
    def setFichaDeHospitalizacion(self, hospFicha):
        self.hospitalizacionFicha = hospFicha
        self.guardarFichaDeHospitalizacionEnBaseDeDatos()

    #ficha de hospitalizacion 

    #ficha de sedacion
    def solicitarFichaDeSedacionEnBaseDeDatos(self):
        if (self.sedacion == 1):
            sql = 'SELECT * FROM FichaSedación WHERE FichaMedica_idFichaMedica = (%s)'
            mycursor.execute(sql, (str(self.id),))
            sedacion = mycursor.fetchone()
            if(sedacion[1] == 1):
                aut = True
            else:
                aut = False
            self.sedacionFicha =  {
                'id':sedacion[0],
                'autorizacion':aut,
            }
    
    def guardarFichaDeSedacionEnBaseDeDatos(self):
        sql = 'INSERT INTO fichasedación VALUES (%s, %s, %s, %s)'
        mycursor.execute(sql, (str(self.sedacionFicha['id']), str(self.sedacionFicha['autorizacion']), str(self.getId()), str(self.getIdTabla())))
        db.commit()

    def setFichaDeSefacion(self, sedDicc):
        self.sedacionFicha = sedDicc
        self.guardarFichaDeSedacionEnBaseDeDatos()

    #ficha de sedacion

    #tratamientos en la consulta
    
    def solicitarTratamientosConsultaBaseDeDatos(self):
        sql = 'SELECT * FROM TratamientosConsulta WHERE FichaMedica_idFichaMedica = (%s)'
        mycursor.execute(sql, (str(self.id),))
        tratamientos = mycursor.fetchall()
        for tratamiento in tratamientos: #solicitamos todos los tratamientos en la base de datos y los guardamos en la clase 
            trat = {
            'id' : tratamiento[0],
            'nombreTratamiento': tratamiento[1],
            'causaVisita' : tratamiento[2],
            }
            self.tratamientoConsulta.append(trat)
        
    def guargarTratamientosConsultaEnBaseDeDatos(self):
        for tratamiento in self.getTratamiento(): #recorremos todos los tratamientos aplicados en la consulta y los guardamos en la base de datos 
            sql = 'INSERT INTO TratamientosConsulta (idTratamientosConsulta, nombreTratamientos, caudaDeLaVisita, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica) VALUES (%s, %s, %s, %s, %s)'
            mycursor.execute(sql, (str(tratamiento['id']), str(tratamiento['nombreTratamiento']), str(tratamiento['causaVisita']), str(self.getId()), str(self.getIdTabla())))
            db.commit()
    
    def setTratamientosConsulta(self, tratamiento): 
        self.tratamientoConsulta = tratamiento
        self.guargarTratamientosConsultaEnBaseDeDatos()
    
    def agregarTratamientosConsulta(self, tratamiento):
        self.tratamientoConsulta.append(tratamiento)

    #tratamientos en la consulta

    #medicamentos 
    def solicitarMedicamentosConsultaEnBaseDeDatos(self):
        sql = 'SELECT * FROM medicamentosconsulta WHERE FichaMedica_idFichaMedica = (%s)'
        mycursor.execute(sql, (str(self.getId),))
        medicamentos = mycursor.fetchall()
        for medicamento in medicamentos:
            med = {
            'id' : medicamento[0],
            'nomMedicamento' : medicamento[1],
            }
            self.medicamentosConsulta.append(med)

    def guardarMedicamentosConsultaEnBaseDeDatos(self): 
        for medicamento in self.getMedicamentosConsulta():
            sql = 'INSERT INTO MedicamentosConsulta (idMedicamentosConsulta, nombreMedicamentos, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica) VALUES (%s, %s, %s, %s)'
            mycursor.execute(sql, (str(medicamento['id']), str(medicamento['nomMedicamento']), str(self.getId()), str(self.getIdTabla())))
            db.commit()

    def setMedicamentosConsulta(self, medicamentos):
        self.medicamentosConsulta = medicamentos #al momento de guardar los datos en el objeto tambien se guardan en la base de datos
        self.guardarMedicamentosConsultaEnBaseDeDatos()
    
    def agregarMedicamentosConsulta(self, medicamentos):
        self.medicamentosConsulta.append(medicamentos)
    #medicamentos 

    #vacunas 
    def solicitarVacunacionEnBaseDeDatos(self):
        sql = 'SELECT * FROM VacunasSuministradasConsulta WHERE FichaMedica_idFichaMedica = (%s)'
        mycursor.execute(sql, (str(self.id),))
        vacunas = mycursor.fetchall()
        for vacuna in vacunas:
            vac = {
            'id' : vacuna[0],
            'nomVacuna' : vacuna[1],
            }
            self.vacunasSuministradasConsulta.append(vac)
    
    def guardarVacunacionEnBaseDeDatos(self):
        for vacuna in self.getVacunasSuministradasConsulta():
            sql = 'INSERT INTO VacunasSuministradasConsulta (idVacunasSuministradas, nombreVacuna, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica) VALUES (%s, %s, %s, %s)'
            mycursor.execute(sql, (str(vacuna['id']), str(vacuna['nomVacuna']), str(self.getId()), str(self.getIdTabla())))
            db.commit() #aqui se guardan las vacunas correspondientes a la ficha de vacunación, en la funcion superior se realizara en guardado en la tabla 

    def setVacunacion(self, vacunas):
        self.vacunasSuministradasConsulta = vacunas
        self.guardarVacunacionEnBaseDeDatos()

    def agregarVacunacion(self, vacunas):
        self.vacunasSuministradasConsulta.append(vacunas)
    #vacunas
    
    def validarFormatoDatos(self): #validar formato de datos en la propia clase ya que pueden saltarse validacioines mediante ui
        pass