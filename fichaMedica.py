import mysql.connector
from numpy import array

class FichaMedica:

    #idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp
    def __init__(self, *args): #debido al funcionamiento de python
        #solo manejaremos un constructor que sera ocupado para principalmente el manejo en base de datos, pero tambien para el ingresao normal 
        if(len(args) == 2):
            self.idFicha = args[0]
            self.fechaConsulta = args[1]
            self.sucursalVeterinaria = None
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
            self.fechaModificacion = None
            self.indicarModificacion = None
            self.fichaActual = False

            self.receta = None

        elif(len(args) == 12):
            self.idFicha = args[0]
            self.sucursalVeterinaria = args[1]
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

            self.fechaModificacion = None
            self.indicarModificacion = None

            self.fichaActual = False   

            self.receta = None

    def editarFichaMedica(self):
        pass

    def crearFichaMedica(self):
        pass

    def guardarFichaGeneralEnBaseDeDatos(self, idTabla, myCursor, dB):
        sql = 'INSERT INTO FichaMedica (idFichaMedica, TablaMedica_idTablaMedica, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operación, frecuenciaRespiratoria, frecuenciaCardiaca, peso, Edad, hospitalización, sedación, temperatura) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' 
        myCursor.execute(sql, (str(self.getId()), str(idTabla), str(self.getSucursalVeterinaria()), str(self.getVeterinarioACargo()), str(self.getFechaConsulta()), self.getOperacion(), str(self.getFrecRespiratoria()), str(self.getFrecCardiaca()), self.getPeso(), str(self.getEdad()), self.getHospitalizacion(), self.getSedacion(), self.getTemp()))
        dB.commit()
    
    def modificarFichaGeneralEnBaseDeDatos(self, sucursalVeterinaria, veterinarioACargo, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, myCursor, dB, fechaModificacion):
        sql = 'UPDATE fichamedica SET sucursalVeterinaria = %s, veterinarioACargo = %s,  operación = %s, frecuenciaRespiratoria = %s, frecuenciaCardiaca = %s, peso = %s, Edad = %s, hospitalización = %s, sedación = %s, temperatura = %s, fechaUltimaMod = %s, flagModificacion = %s WHERE idFichaMedica = %s'
        myCursor.execute(sql, (str(sucursalVeterinaria), str(veterinarioACargo), str(operacion), str(frecRespiratoria), str(frecCardiaca), str(peso), str(edad), str(hospitalizacion), str(sedacion), str(temp), str(fechaModificacion), True, str(self.idFicha)))
        dB.commit()

        self.fechaModificacion = fechaModificacion
        self.indicarModificacion = True
#getters
    def getId(self):
        return self.idFicha

    #def getIdTabla(self):
        #return self.idTabla
    
    def getSucursalVeterinaria(self):
        return self.sucursalVeterinaria

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
    
    def getIdOperacion(self):
        return self.operacionFicha['id']
    
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

    def getIdHospitalizacion(self):
        return self.hospitalizacionFicha['id']
    
    def getSedacion(self):
        return self.sedacion
    
    def getSedacioFicha(self):
        return self.sedacionFicha
    
    def getTratamiento(self):
        #print(self.tratamientoConsulta)
        return self.tratamientoConsulta
    
    def getFechaModificacion(self):
        return self.fechaModificacion
    
    def getIndicadorModificacion(self):
        return self.indicarModificacion

    def getActual(self):
        return self.fichaActual
    
    def getReceteta(self):
        return self.receta

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
        self.temperatura = temp
    
    def setFechaModificacion(self, fechaModificacion):
        self.fechaModificacion = fechaModificacion
    
    def setIndicadorModificacion(self, indicarModificacion):
        self.indicarModificacion = indicarModificacion

    def setActual(self, actual):
        self.fichaActual = actual
    
    def setReceteta(self, receta):
        self.receta = receta

    def solicitarFichaDeOperacionEnBaseDeDatos(self, myCursor):
        if (self.operacion == 1):
            sql = 'SELECT * FROM fichaOperación WHERE FichaMedica_idFichaMedica = (%s)' #se genera la consulta en base al id unico de la ficha medica 
            myCursor.execute(sql, (str(self.getId()),)) #ejecuta la consulta
            opFicha = myCursor.fetchone() #captura el resultado 
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

    def guardarFichaDeOperacionEnBaseDeDatos(self,  myCursor, dB):
        sql = 'INSERT INTO fichaOperación (idFichaOperación, diagnostico, cirugiaARealizar, autorizacionTutor, FichaMedica_idFichaMedica) VALUES (%s, %s, %s, %s, %s)'
        myCursor.execute(sql, (str(self.operacionFicha['id']), str(self.operacionFicha['diagnostico']), str(self.operacionFicha['cirugiaARealizar']), str(self.operacionFicha['autTutor']), str(self.getId())))
        dB.commit()
    
    def modificarOperacionFichaGeneralEnBaseDeDatos(self, myCursor, dB):
        sql = 'UPDATE fichaMedica SET operación=(%s) WHERE idFichaMedica = (%s)'
        myCursor.execute(sql, (self.operacion, str(self.getId())))
        dB.commit()

    def modificarOperacionEnBaseDeDatos(self, operaciones, fechaUltimaModificacion, myCursor, dB):
        sql = 'UPDATE fichaoperación SET diagnostico = %s, cirugiaARealizar = %s, fechaUltimaMod = %s, flagModificacion = %s WHERE idFichaOperación = (%s)'
        myCursor.execute(sql, (str(operaciones['diagnostico']), str(operaciones['cirugiaARealizar']),str(fechaUltimaModificacion), True, str(operaciones['id']),))
        dB.commit()

        self.operacionFicha = operaciones

    def setFichaOperacion(self, opFicha, myCursor, dB):
        self.operacionFicha = opFicha #se guarda el diccionario correpondiente a la ficha de operacion 
        self.operacion = 1
        self.modificarOperacionFichaGeneralEnBaseDeDatos(myCursor, dB)
        
        if(self.operacion == 1): #se verifica que la ficha posee una ficha de operación 
            print("hola si if")
            self.guardarFichaDeOperacionEnBaseDeDatos(myCursor, dB)
    #aqui 22-07-2022 22:58 cristian Aguilera


    #24-07-2022 Cristian Aguilera

    #ficha de hospitalizacion 
    def solicitarFichaDeHospitalizacionEnBaseDeDatos(self, myCursor):
        if(self.hospitalizacion == 1):
            sql = 'SELECT * FROM FichaHospitalización WHERE FichaMedica_idFichaMedica = (%s)'
        
            myCursor.execute(sql, (str(self.getId()),))
            hospiFicha = myCursor.fetchone()
            if(hospiFicha is not None):
                self.hospitalizacionFicha = { #al ser una ficha se guarda directamente en el tributo relerente al diccionario
                    'id':hospiFicha[0],
                    'motivo':hospiFicha[1],
                }

    def guardarFichaDeHospitalizacionEnBaseDeDatos(self, myCursor, dB):
        sql = 'INSERT INTO fichahospitalización (idFichaHospitalización, motivoHospitalización, FichaMedica_idFichaMedica)  VALUES (%s, %s, %s)'
        myCursor.execute(sql, (str(self.hospitalizacionFicha['id']), str(self.hospitalizacionFicha['motivo']), str(self.getId())) )
        dB.commit()
    
    def modificarHospitalizacionFichaGeneralEnBaseDeDatos(self, myCursor, dB):
        sql = 'UPDATE fichamedica SET hospitalización=(%s) WHERE idFichaMedica = (%s)'
        myCursor.execute(sql, (self.hospitalizacion, str(self.getId())))
        dB.commit()
    
    def modificarHopitalizacionEnBaseDeDatos(self, hospFicha, fechaUltimaModificacion, myCursor, dB):
        sql = 'UPDATE fichahospitalización SET motivoHospitalización = %s, fechaUltimaMod = %s, flagModificacion = %s WHERE idFichaHospitalización = (%s)'
        myCursor.execute(sql, (str(hospFicha['motivo']), str(fechaUltimaModificacion) ,True, str(hospFicha['id'])))
        dB.commit()

        self.hospitalizacionFicha = hospFicha
        pass

    
    def setFichaDeHospitalizacion(self, hospFicha, myCursor, dB):
        self.hospitalizacionFicha = hospFicha
        self.hospitalizacion = 1
        self.modificarHospitalizacionFichaGeneralEnBaseDeDatos(myCursor, dB)
        self.guardarFichaDeHospitalizacionEnBaseDeDatos(myCursor, dB)

    #ficha de hospitalizacion 

    #ficha de sedacion
    def solicitarFichaDeSedacionEnBaseDeDatos(self, myCursor):
        if (self.sedacion == 1):
            sql = 'SELECT * FROM FichaSedación WHERE FichaMedica_idFichaMedica = (%s)'
            myCursor.execute(sql, (str(self.getId()),))
            sedacion = myCursor.fetchone()
            if(sedacion is not None):
                if(sedacion[1] == 1):
                    aut = True
                else:
                    aut = False

                
                self.sedacionFicha =  {
                    'id':sedacion[0],
                    'autorizacion':aut,
                }
        

    
    def guardarFichaDeSedacionEnBaseDeDatos(self, myCursor, dB):
        sql = 'INSERT INTO fichasedación VALUES (%s, %s, %s)'
        myCursor.execute(sql, (str(self.sedacionFicha['id']), str(self.sedacionFicha['autorizacion']), str(self.getId())))
        dB.commit()

    def modificarSedacionFichaGeneralEnBaseDeDatos(self, myCursor, dB):
        sql = 'UPDATE fichamedica SET sedación=(%s) WHERE idFichaMedica = (%s)'
        myCursor.execute(sql, (self.sedacion, str(self.getId())))
        dB.commit()

    def setFichaDeSefacion(self, sedFicha, myCursor, dB):
        self.sedacionFicha = sedFicha
        self.sedacion = 1
        self.modificarSedacionFichaGeneralEnBaseDeDatos(myCursor, dB)
        self.guardarFichaDeSedacionEnBaseDeDatos(myCursor, dB)

    #ficha de sedacion

    #tratamientos en la consulta
    
    def solicitarTratamientosConsultaBaseDeDatos(self, myCursor):
        sql = 'SELECT * FROM TratamientosConsulta WHERE FichaMedica_idFichaMedica = (%s)'
        tratamientosArray = []
        myCursor.execute(sql, (str(self.getId()),))
        tratamientos = myCursor.fetchall()
        if(tratamientos is not None):
            for tratamiento in tratamientos: #solicitamos todos los tratamientos en la base de datos y los guardamos en la clase 
                trat = {
                'id' : tratamiento[0],
                'nombreTratamiento': tratamiento[1],
                'causaVisita' : tratamiento[2],
                }
                tratamientosArray.append(trat)
            self.tratamientoConsulta = tratamientosArray
    
    def guargarTratamientosConsultaEnBaseDeDatos(self, myCursor, dB):
        for tratamiento in self.getTratamiento(): #recorremos todos los tratamientos aplicados en la consulta y los guardamos en la base de datos 
            sql = 'INSERT INTO TratamientosConsulta VALUES (%s, %s, %s, %s)' #(idTratamientosConsulta, nombreTratamientos, caudaDeLaVisita, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica)
            myCursor.execute(sql, (str(tratamiento['id']), str(tratamiento['nombreTratamiento']), str(tratamiento['causaVisita']), str(self.getId()),))
            dB.commit()

    def actualizarTratamientosConsultaEnBaseDeDatos(self, tratamientos ,myCursor, dB):
        for tratamiento in tratamientos: #recorremos todos los tratamientos aplicados en la consulta y los guardamos en la base de datos 
            sql = 'UPDATE TratamientosConsulta SET nombreTratamientos = %s, caudaDeLaVisita = %s WHERE idTratamientosConsulta = %s' #(idTratamientosConsulta, nombreTratamientos, caudaDeLaVisita, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica)
            myCursor.execute(sql, (str(tratamiento['nombreTratamiento']), str(tratamiento['causaVisita']), str(tratamiento['id'])))
            dB.commit()

    def setTratamientosConsulta(self, tratamiento, myCursor, dB): 
        self.tratamientoConsulta = tratamiento
        self.guargarTratamientosConsultaEnBaseDeDatos(myCursor, dB)
    
    def agregarTratamientosConsulta(self, tratamiento):
        self.tratamientoConsulta.append(tratamiento)

    #tratamientos en la consulta

    #medicamentos 
    def solicitarMedicamentosConsultaEnBaseDeDatos(self, myCursor):
        sql = 'SELECT * FROM medicamentosconsulta WHERE FichaMedica_idFichaMedica = (%s)'
        myCursor.execute(sql, (str(self.getId()),))
        medicamentos = myCursor.fetchall()
        medicamentosArray = []
        for medicamento in medicamentos:
            med = {
            'id' : medicamento[0],
            'nomMedicamento' : medicamento[1],
            }
            medicamentosArray.append(med)
            print("380 fichaMedica :"+str(med))
        self.medicamentosConsulta = medicamentosArray

    def guardarMedicamentosConsultaEnBaseDeDatos(self, myCursor, dB): 
        for medicamento in self.getMedicamentosConsulta():
            sql = 'INSERT INTO MedicamentosConsulta VALUES (%s, %s, %s)' #(idMedicamentosConsulta, nombreMedicamentos, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica) 
            myCursor.execute(sql, (str(medicamento['id']), str(medicamento['nomMedicamento']), str(self.getId())))
            dB.commit()
    
    def actualizarMedicamentosConsultaEnBaseDeDatos(self, medicamentos, myCursor, dB): 
        for medicamento in medicamentos:
            sql = 'UPDATE MedicamentosConsulta SET nombreMedicamentos = %s WHERE idMedicamentosConsulta = %s' #(idMedicamentosConsulta, nombreMedicamentos, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica) 
            myCursor.execute(sql, (str(medicamento['nomMedicamento']), str(medicamento['id'])))
            dB.commit()
        
        self.medicamentosConsulta = medicamentos
        

    def setMedicamentosConsulta(self, medicamentos, myCursor, dB):
        print('medicamentos')
        self.medicamentosConsulta = medicamentos #al momento de guardar los datos en el objeto tambien se guardan en la base de datos
        self.guardarMedicamentosConsultaEnBaseDeDatos(myCursor, dB)
    
    def agregarMedicamentosConsulta(self, medicamentos):
        self.medicamentosConsulta.append(medicamentos)
    
    #medicamentos 

    #vacunas 
    def solicitarVacunacionEnBaseDeDatos(self, myCursor):
        sql = 'SELECT * FROM VacunasSuministradasConsulta WHERE FichaMedica_idFichaMedica = (%s)'
        myCursor.execute(sql, (str(self.getId()),))
        vacunas = myCursor.fetchall()
        vacunasArray = []
        for vacuna in vacunas:
            vac = {
            'id' : vacuna[0],
            'nomVacuna' : vacuna[1],
            }
            vacunasArray.append(vac) 
        self.vacunasSuministradasConsulta = vacunasArray
    
    def guardarVacunacionEnBaseDeDatos(self, myCursor, dB):
        for vacuna in self.getVacunasSuministradasConsulta():
            sql = 'INSERT INTO VacunasSuministradasConsulta VALUES (%s, %s, %s)' #(idVacunasSuministradas, nombreVacuna, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica)
            myCursor.execute(sql, (str(vacuna['id']), str(vacuna['nomVacuna']), str(self.getId())))
            dB.commit() #aqui se guardan las vacunas correspondientes a la ficha de vacunación, en la funcion superior se realizara en guardado en la tabla 
    
    def actualizarVacunasConsultaEnBaseDeDatos(self, vacunas, myCursor, dB): 
        for vacuna in vacunas:
            print("430 :"+str(vacuna))
            sql = 'UPDATE vacunassuministradasconsulta SET nombreVacuna = %s WHERE idVacunasSuministradas = %s' #(idMedicamentosConsulta, nombreMedicamentos, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica) 
            myCursor.execute(sql, (str(vacuna['nomVacuna']), str(vacuna['id'])))
            dB.commit()
        
        self.vacunasSuministradasConsulta = vacunas

    def setVacunacion(self, vacunas, myCursor, dB):
        self.vacunasSuministradasConsulta = vacunas
        self.guardarVacunacionEnBaseDeDatos(myCursor, dB)

    def agregarVacunacion(self, vacunas):
        self.vacunasSuministradasConsulta.append(vacunas)
    #vacunas

    def validarFormatoDatos(self): #validar formato de datos en la propia clase ya que pueden saltarse validacioines mediante ui #holka
        pass

    #---------------------receta
    def solicitarRecetaBaseDeDatos(self, myCursor):
        sql = 'SELECT * FROM RecetaMedica WHERE FichaMedica_idFichaMedica = (%s)'
        myCursor.execute(sql, (str(self.getId()),))
        recetaDatos = myCursor.fetchone()
       
        if(recetaDatos is not None):
            self.receta = { #al ser una ficha se guarda directamente en el tributo relerente al diccionario
                'id' : recetaDatos[0],
                'rutVeterinario' : recetaDatos[1],
                'preescripcion' : recetaDatos[2]
            }

    def guardarRecetaBaseDeDatos(self, myCursor, dB):
        sql = 'INSERT INTO RecetaMedica VALUES (%s, %s, %s, %s)'
        myCursor.execute(sql, (str(self.receta['id']), str(self.receta['rutVeterinario']), str(self.receta['preescripcion']) ,str(self.getId())))
        dB.commit()

    def modificarRecetaBaseDeDatos(self, receta, myCursor, dB):
        sql = 'UPDATE RecetaMedica SET rutVeterinario=(%s), prescripcion=(%s) WHERE FichaMedica_idFichaMedica = (%s)' #Habia que arreglar la query
        myCursor.execute(sql, (receta['rutVeterinario'], str(receta['preescripcion']), str(self.getId())))
        dB.commit()

    def setReceta(self, receta, myCursor, dB):
        self.receta = receta
        self.guardarRecetaBaseDeDatos(myCursor, dB)
    
    def getIdReceta(self):
        return self.receta['id']
