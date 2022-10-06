import mysql.connector
from numpy import array


db = mysql.connector.connect(
    user='root',
    password='root',
    host='localhost',
    database='mydb',
    port='3306'
)

mycursor = db.cursor()

class FichaMedica:

    #idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp
    def __init__(self, *args): #debido al funcionamiento de python
        #solo manejaremos un constructor que sera ocupado para principalmente el manejo en base de datos, pero tambien para el ingresao normal 
        if(len(args) == 2):
            self.idFicha = args[0]
            self.fechaConsulta = args[1]
            self.idSucursalVeterinaria = None
            self.veterinarioACargo = None

            self.medicamentosConsulta = [] #arreglo de diccionario porque pueden ser mas de uno 
            self.vacunasSuministradasConsulta = []
            self.tratamientoConsulta = []

            self.frecRespiratoria = None
            self.frecCardiaca = None
            self.peso = None
            self.edad = None
            self.temperatura = None

            self.operacion = None #indicar boolean
            self.operacionFicha = None #diccionario
            self.hospitalizacion = None #indicar boolean
            self.hospitalizacionFicha = None #diccionario
            self.sedacion = None #indicar boolean
            self.sedacionFicha = None #diccionario

            self.fichaActual = False

        elif(len(args) == 12):
            self.idFicha = args[0]
            self.idSucursalVeterinaria = args[1]
            self.veterinarioACargo = args[2]
            self.fechaConsulta = args[3]

            self.medicamentosConsulta = [] #arreglo de diccionario porque pueden ser mas de uno 
            self.vacunasSuministradasConsulta = []
            self.tratamientoConsulta = []

            self.frecRespiratoria = args[5]
            self.frecCardiaca = args[6]
            self.peso = args[7]
            self.edad = args[8]
            self.temperatura = args[11]

            self.operacion = args[4] #indicar boolean
            self.operacionFicha = None #diccionario
            self.hospitalizacion = args[9] #indicar boolean
            self.hospitalizacionFicha = None #diccionario
            self.sedacion = args[10] #indicar boolean
            self.sedacionFicha = None #diccionario

            self.fichaActual = False   

    def editarFichaMedica(self):
        pass

    def crearFichaMedica(self):
        pass

    def guardarFichaGeneralEnBaseDeDatos(self, idTabla):
        sql = 'INSERT INTO FichaMedica VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' 
        mycursor.execute(sql, (str(self.getId()), str(idTabla), str(self.getSucursalVeterinaria()), str(self.getVeterinarioACargo()), str(self.getFechaConsulta()), self.getOperacion(), str(self.getFrecRespiratoria()), str(self.getFrecCardiaca()), self.getPeso(), str(self.getEdad()), self.getHospitalizacion(), self.getSedacion(), self.getTemp()))
        db.commit()

#getters
    def getId(self):
        return self.idFicha

    #def getIdTabla(self):
        #return self.idTabla
    
    def getSucursalVeterinaria(self):
        return self.idSucursalVeterinaria

    def getTemp(self):
        return self.temperatura

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
        #print(self.tratamientoConsulta)
        return self.tratamientoConsulta

    def getActual(self):
        return self.fichaActual

#setters 

    def setId(self, id):
        self.id = id
    
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

    def setActual(self, actual):
        self.fichaActual = actual

    def solicitarFichaDeOperacionEnBaseDeDatos(self):
        if (self.operacion == 1):
            sql = 'SELECT * FROM fichaOperación WHERE FichaMedica_idFichaMedica = (%s)' #se genera la consulta en base al id unico de la ficha medica 
            mycursor.execute(sql, (str(self.getId()),)) #ejecuta la consulta
            opFicha = mycursor.fetchone() #captura el resultado 
            if(opFicha[3] == 1):
                aut = True #autorización del tutor
            else:
                aut = False
            
            diccionario= {}
            diccionario = { #al ser una ficha se guarda directamente en el tributo relerente al diccionario
                'id':opFicha[0],
                'diagnostico':opFicha[1],
                'cirugiaARealizar':opFicha[2],
                'autTutor': aut
            }

            self.operacionFicha = diccionario

    def guardarFichaDeOperacionEnBaseDeDatos(self):
        sql = 'INSERT INTO fichaOperación VALUES (%s, %s, %s, %s, %s)'
        mycursor.execute(sql, (str(self.operacionFicha['id']), str(self.operacionFicha['diagnostico']), str(self.operacionFicha['cirugiaARealizar']), str(self.operacionFicha['autTutor']), str(self.getId())))
        db.commit()
    
    def modificarOperacionFichaGeneralEnBaseDeDatos(self):
        sql = 'UPDATE fichaMedica SET operación=(%s) WHERE idFichaMedica = (%s)'
        mycursor.execute(sql, (self.operacion, str(self.getId())))
        db.commit()

    def setFichaOperacion(self, opFicha):
        self.operacionFicha = opFicha #se guarda el diccionario correpondiente a la ficha de operacion 
        self.operacion = 1
        self.modificarOperacionFichaGeneralEnBaseDeDatos()
        
        if(self.operacion == 1): #se verifica que la ficha posee una ficha de operación 
            print("hola si if")
            self.guardarFichaDeOperacionEnBaseDeDatos()
    #aqui 22-07-2022 22:58 cristian Aguilera


    #24-07-2022 Cristian Aguilera

    #ficha de hospitalizacion 
    def solicitarFichaDeHospitalizacionEnBaseDeDatos(self):
        if(self.hospitalizacion == 1):
            sql = 'SELECT * FROM FichaHospitalización WHERE FichaMedica_idFichaMedica = (%s)'
            mycursor.execute(sql, (str(self.getId()),))
            hospiFicha = mycursor.fetchone()
            self.hospitalizacionFicha = { #al ser una ficha se guarda directamente en el tributo relerente al diccionario
                'id':hospiFicha[0],
                'motivo':hospiFicha[1],
            }

    def guardarFichaDeHospitalizacionEnBaseDeDatos(self):
        sql = 'INSERT INTO fichahospitalización VALUES (%s, %s, %s)'
        mycursor.execute(sql, (str(self.hospitalizacionFicha['id']), str(self.hospitalizacionFicha['motivo']), str(self.getId())))
        db.commit()
    
    def modificarHospitalizacionFichaGeneralEnBaseDeDatos(self):
        sql = 'UPDATE fichamedica SET hospitalización=(%s) WHERE idFichaMedica = (%s)'
        mycursor.execute(sql, (self.hospitalizacion, str(self.getId())))
        db.commit()
    
    def setFichaDeHospitalizacion(self, hospFicha):
        self.hospitalizacionFicha = hospFicha
        self.hospitalizacion = 1
        self.modificarHospitalizacionFichaGeneralEnBaseDeDatos()
        self.guardarFichaDeHospitalizacionEnBaseDeDatos()

    #ficha de hospitalizacion 

    #ficha de sedacion
    def solicitarFichaDeSedacionEnBaseDeDatos(self):
        if (self.sedacion == 1):
            sql = 'SELECT * FROM FichaSedación WHERE FichaMedica_idFichaMedica = (%s)'
            mycursor.execute(sql, (str(self.getId()),))
            sedacion = mycursor.fetchone()
            if(sedacion[1] == 1):
                aut = True
            else:
                aut = False

            db.commit()
            self.sedacionFicha =  {
                'id':sedacion[0],
                'autorizacion':aut,
            }
        

    
    def guardarFichaDeSedacionEnBaseDeDatos(self):
        sql = 'INSERT INTO fichasedación VALUES (%s, %s, %s)'
        mycursor.execute(sql, (str(self.sedacionFicha['id']), str(self.sedacionFicha['autorizacion']), str(self.getId())))
        db.commit()

    def modificarSedacionFichaGeneralEnBaseDeDatos(self):
        sql = 'UPDATE fichamedica SET sedación=(%s) WHERE idFichaMedica = (%s)'
        mycursor.execute(sql, (self.sedacion, str(self.getId())))
        db.commit()

    def setFichaDeSefacion(self, sedFicha):
        self.sedacionFicha = sedFicha
        self.sedacion = 1
        self.modificarSedacionFichaGeneralEnBaseDeDatos()
        self.guardarFichaDeSedacionEnBaseDeDatos()

    #ficha de sedacion

    #tratamientos en la consulta
    
    def solicitarTratamientosConsultaBaseDeDatos(self):
        sql = 'SELECT * FROM TratamientosConsulta WHERE FichaMedica_idFichaMedica = (%s)'
        tratamientosArray = []
        mycursor.execute(sql, (str(self.getId()),))
        tratamientos = mycursor.fetchall()
        for tratamiento in tratamientos: #solicitamos todos los tratamientos en la base de datos y los guardamos en la clase 
            trat = {
            'id' : tratamiento[0],
            'nombreTratamiento': tratamiento[1],
            'causaVisita' : tratamiento[2],
            }
            tratamientosArray.append(trat)
        self.tratamientoConsulta = tratamientosArray
    
    def guargarTratamientosConsultaEnBaseDeDatos(self):
        for tratamiento in self.getTratamiento(): #recorremos todos los tratamientos aplicados en la consulta y los guardamos en la base de datos 
            sql = 'INSERT INTO TratamientosConsulta VALUES (%s, %s, %s, %s)' #(idTratamientosConsulta, nombreTratamientos, caudaDeLaVisita, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica)
            mycursor.execute(sql, (str(tratamiento['id']), str(tratamiento['nombreTratamiento']), str(tratamiento['causaVisita']), str(self.getId())))
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
        mycursor.execute(sql, (str(self.getId()),))
        medicamentos = mycursor.fetchall()
        medicamentosArray = []
        for medicamento in medicamentos:
            med = {
            'id' : medicamento[0],
            'nomMedicamento' : medicamento[1],
            }
            medicamentosArray.append(med)
        self.medicamentosConsulta = medicamentosArray

    def guardarMedicamentosConsultaEnBaseDeDatos(self): 
        for medicamento in self.getMedicamentosConsulta():
            sql = 'INSERT INTO MedicamentosConsulta VALUES (%s, %s, %s)' #(idMedicamentosConsulta, nombreMedicamentos, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica) 
            mycursor.execute(sql, (str(medicamento['id']), str(medicamento['nomMedicamento']), str(self.getId())))
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
        mycursor.execute(sql, (str(self.getId()),))
        vacunas = mycursor.fetchall()
        vacunasArray = []
        for vacuna in vacunas:
            vac = {
            'id' : vacuna[0],
            'nomVacuna' : vacuna[1],
            }
            vacunasArray.append(vac) 
        self.vacunasSuministradasConsulta = vacunasArray
    
    def guardarVacunacionEnBaseDeDatos(self):
        for vacuna in self.getVacunasSuministradasConsulta():
            sql = 'INSERT INTO VacunasSuministradasConsulta VALUES (%s, %s, %s)' #(idVacunasSuministradas, nombreVacuna, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica)
            mycursor.execute(sql, (str(vacuna['id']), str(vacuna['nomVacuna']), str(self.getId())))
            db.commit() #aqui se guardan las vacunas correspondientes a la ficha de vacunación, en la funcion superior se realizara en guardado en la tabla 

    def setVacunacion(self, vacunas):
        self.vacunasSuministradasConsulta = vacunas
        self.guardarVacunacionEnBaseDeDatos()

    def agregarVacunacion(self, vacunas):
        self.vacunasSuministradasConsulta.append(vacunas)
    #vacunas

    def validarFormatoDatos(self): #validar formato de datos en la propia clase ya que pueden saltarse validacioines mediante ui #holka
        pass