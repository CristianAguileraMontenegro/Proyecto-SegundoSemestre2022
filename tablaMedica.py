import mysql.connector

from fichaMedica import FichaMedica #importamos la clase 

db = mysql.connector.connect(
    user='piero',
    password='pieron123',
    host='localhost',
    database='mydb',
    port='3306'
)


mycursor = db.cursor()

class TablaMedica:

    listaDeFichasCorrespondientesTablaMedica = []

    def __init__(self, id):
        self.id = id
        self.fichas:FichaMedica = [] #arreglo 
        self.alergias = [] #diccionario
        self.registroDeOperaciones = [] #diccionario
        self.vacunasSuministradas = [] #diccionario
    

    def solicitarFichasEnBaseDeDatos(self):
        sql = 'SELECT * FROM fichaMedica WHERE Tablamedica_idTablamedica = (%s)'
        mycursor.execute(sql, (str(self.id),))
        fichas = mycursor.fetchall()
        for ficha in fichas: #se recorren todas las ficha correspondientes a la tabla medica en particular 
            fichaMedica = FichaMedica(ficha[0],ficha[2],ficha[3],ficha[4],ficha[5],ficha[6],ficha[7],ficha[8],ficha[9],ficha[10],ficha[11], ficha[12]) 
            #las posiciones son correspondientes a el dato en la clase fichaMedica, se realiza de esta manera ya que lo que se entrega desde la base de datos es un aareglo de string por lo tanto se debe acceder a cada
            #posicion a fin de obtener los datos del mismo 

            #solicitamos todos los datos asociados en la base de datos
            fichaMedica.solicitarFichaDeHospitalizacionEnBaseDeDatos()
            fichaMedica.solicitarMedicamentosConsultaEnBaseDeDatos()
            fichaMedica.solicitarVacunacionEnBaseDeDatos()
            fichaMedica.solicitarFichaDeHospitalizacionEnBaseDeDatos()
            fichaMedica.solicitarFichaDeSedacionEnBaseDeDatos()
            fichaMedica.solicitarTratamientosConsultaBaseDeDatos()
            self.agregarFichaMedicaExistente(ficha[0],ficha[2],ficha[3],ficha[4],ficha[5],ficha[6],ficha[7],ficha[8],ficha[9],ficha[10],ficha[11], ficha[12])
            #self.fichas.append(fichaMedica)


    def guardarTablaEnBaseDeDatos(self):
        sql = "INSERT INTO tablamedica values (%s)"
        mycursor.execute(sql, (str(self.id)))
        db.commit()

    def agregarFichaMedicaConsultaATabla(self, idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp):
        fichaMedicaConsulta = FichaMedica(idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp)
        self.fichas.append(fichaMedicaConsulta)
        self.guardarFichaGeneralEnBaseDeDatos(fichaMedicaConsulta)

    def agregarFichaMedicaExistente(self, idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp):
        fichaMedicaConsulta = FichaMedica(idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp)
        self.fichas.append(fichaMedicaConsulta)

    def guardarFichaGeneralEnBaseDeDatos(self, fichaMedicaConsulta:FichaMedica):
        fichaMedicaConsulta.guardarFichaGeneralEnBaseDeDatos(self.getId())

    def editarFichaMedicaConsulta(self):
        pass

    def mostrarFichasMedicas(self):
        pass

    def validarFormatoDatos(self): #validar en el propio objeto los datos y entregar el retorno en numero para identificar el mensaje de error a mostar
        pass

    def solicitudConexionServCrear(self):
        pass

    def solicitudConexionServEditar(self):
        pass

    def solicitudConexionServMostrar(self):
        pass

    
        

#alergias
    def agregarAlergias(self, alergia):
        self.alergias.append(alergia)
    
    def setAlergias(self, alergias):
        self.alergias = alergias
        #self.guardarAlergiasEnBaseDeDatos()
    
    def solicitarAlergiasEnBaseDeDatos(self):
        sql = 'SELECT * FROM Alergias WHERE TablaMedica_idTablaMedica = (%s)'
        mycursor.execute(sql, (str(self.getId()),))
        alergiasMascota = mycursor.fetchall()
        for alergiaMascota in alergiasMascota:
            alergia = {
                'id': alergiaMascota[0],
                'nombre': alergiaMascota[1],
            }
            self.agregarAlergias(alergia)


    def guardarAlergiasEnBaseDeDatos(self):
        for alergia in self.getAlergias():
            sql = "INSERT INTO alergias values (%s, %s, %s)"
            mycursor.execute(sql, (str(alergia['id']), str(alergia['nombre']), str(self.getId())))
            db.commit()

    def getAlergias(self):
        return self.alergias

#alergias

#Registro de operaciones 

    def agregarOperaciones(self, operacion):
        self.registroDeOperaciones.append(operacion)

    def setRegistroDeOperaciones(self, operaciones): #local
        self.registroDeOperaciones = operaciones

    def solicitarRegistroDeOperacionesEnBaseDeDatos(self):
        sql = 'SELECT * FROM RegistroDeOperaciones WHERE TablaMedica_idTablaMedica = (%s)'
        mycursor.execute(sql, (str(self.getId()),))
        registroOperaciones = mycursor.fetchall()

        for operaciones in registroOperaciones:
            operacion = {
                'id': operaciones[0],
                'operacion': operaciones[1],
            }
            self.agregarOperaciones.append(operacion)

    def guardarOperacionesEnBaseDeDatos(self):
        for operacion in self.getRegistroDeOperaciones():
            sql = 'Insert INTO registroDeOperaciones VALUES (%s, %s,%s)'
            mycursor.execute(sql, (str(operacion['id']), str(operacion['operacion']),  str(self.getId())))
            db.commit()

    def getRegistroDeOperaciones(self):
        return self.registroDeOperaciones

#Registro de operaciones 

#Vacunas suministradas 

    def agregarVacunas(self, vacunas):
        self.vacunasSuministradas.append(vacunas)

    def setRegistroDeVacunas(self, vacunas):
        self.vacunasSuministradas = vacunas 
    
    def solicitarVacunasEnBaseDeDatos(self):
        sql = 'SELECT * FROM RegistroVacunasSuministradas WHERE TablaMedica_idTablaMedica = (%s)'
        mycursor.execute(sql, (str(self.getId()),))
        registroVacunas = mycursor.fetchall()

        for vacunas in registroVacunas:
            vacuna = {
                'id': vacunas[0],
                'nombre': vacunas[1],
            }
            self.vacunasSuministradas.append(vacuna)

    def guardarRegistroVacunasEnBaseDeDatos(self):
        for vacunas in self.getVacunasSuministradas():
            sql = 'INSERT INTO registrovacunassuministradas (idVacunasSuministradas, nombreVacuna, TablaMedica_idTablaMedica) VALUES (%s, %s, %s)'
            mycursor.execute(sql, (str(vacunas['id']), str(vacunas['nombre']), str(self.getId())))
            db.commit()

    def getVacunasSuministradas(self):
        return self.vacunasSuministradas

#Vacunas suministradas 


#todos los set se realizaran sobre la ultima ficha agregada, esto debido a que solo la utima puede llegar a ser modificada o se agregaran datos 
#metodos de bajada de datos a clase inferior, fichas extra 

    def setFichaDeOperacion(self, opFicha, idFicha): #se ocupa el id para identificar la ficha especifica a la que añadir
        self.fichas[len(self.fichas)-1].setFichaOperacion(opFicha) #siempre se agrega a la ultima ficha generada
    
    def setFichaDeHospitalizacion(self, hospFicha, idFicha): #se ocupa el id para identificar
        self.fichas[len(self.fichas)-1].setFichaDeHospitalizacion(hospFicha)
    
    def setFichaDeSefacion(self, sedFicha, idFicha): #se ocupa el id
        self.fichas[len(self.fichas)-1].setFichaDeSefacion(sedFicha)
    
    def setOperacionFicha(self, operacion): #indicadores de que existe una ficha de cada tipo
        self.fichas[len(self.fichas)-1].setOperacion(operacion)
    
    def setHospitalizacionFicha(self, hospitalizacion):
        self.fichas[len(self.fichas)-1].setHospitalizacion(hospitalizacion)

    def setSedacionFicha(self, sedacion):
        self.fichas[len(self.fichas)-1].setSedacion(sedacion)

#metodos de bajada de datos a clase inferior, fichas extra

# metodos de bajada de datos a clase inferior ne ficha general

    def setIdFicha(self, idFicha):
        self.fichas[len(self.fichas)-1].setId(idFicha) 
    
    def setSucursalVeterinariaFicha(self, sucursalVeterinaria):
        self.fichas[len(self.fichas)-1].setSucursalVeterinaria(sucursalVeterinaria)
    
    def setVeterinarioACargoFicha(self, veterinarioACargo):
        self.fichas[len(self.fichas)-1].setVeterinarioACargo(veterinarioACargo)
    
    def setFechaConsultaFicha(self, fechaConsulta):
        self.fichas[len(self.fichas)-1].setFechaConsulta(fechaConsulta)

    def setFrecRespiratoriaFicha(self, frecRespiratoria):
        self.fichas[len(self.fichas)-1].setFrecRespiratoria(frecRespiratoria)

    def setFrecCardiacaFicha(self, frecCardiaca):
        self.fichas[len(self.fichas)-1].setFrecCardiaca(frecCardiaca)

    def setPesoFicha(self, peso):
        self.fichas[len(self.fichas)-1].setPeso(peso)

    def setEdadFicha(self, edad):
        self.fichas[len(self.fichas)-1].setEdad(edad)

    def setTempFicha(self, temp):
        self.fichas[len(self.fichas)-1].setTempFicha(temp)

# metodos de bajada de datos a clase inferior ne ficha general

# metodos de subida de datos a clase superior de ficha general 
#para los metodos get de subida deben ser para cada ficha generada, estos se usaran en temas de modificacion y en el mustreto de fichas 

    def getIdFicha(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getId()
    
    def getSucursalVeterinaria(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getSucursalVeterinaria()

    def getTemp(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getSucursalVeterinaria()

    def getVeterinarioACargo(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getVeterinarioACargo()

    def getFechaConsulta(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getFechaConsulta()

    def getMedicamentosConsulta(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getMedicamentosConsulta()

    def getOperacion(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getOperacion()

    def getOperacionFicha(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getOperacionFicha()
    
    def getVacunasSuministradasConsulta(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getVacunasSuministradasConsulta()

    def getFrecRespiratoria(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getFrecRespiratoria()
    
    def getFrecCardiaca(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getFrecCardiaca()
    
    def getPeso(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getPeso()
    
    def getEdad(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getEdad()
    
    def getHospitalizacion(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getHospitalizacion()
    
    def getHospitalizacionFicha(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getHospitalizacionFicha()
    
    def getSedacion(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getSedacion()
    
    def getSedacioFicha(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getSedacioFicha()
    
    def getTratamiento(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getTratamiento()

    def getId(self):
        return self.id

    def getIdsFichas(self)->list:
        fichasTrabajar = self.fichas
        listRetorno = []
        for ficha in fichasTrabajar:
            listRetorno.append(ficha.getId())

        return listRetorno

    """def setRegistroDeVacunasTrue(self, vacuna):
        for vac in vacuna:
            self.vacunasSuministradas.append(vac)

    def setOpFichaLocal(self, idFicha, opDicc, operacion):
        for ficha in self.fichas:
            if ficha.getId() == idFicha:
                ficha.setOperacion(operacion)
                ficha.setOpFichaLocal(opDicc)

    def setVacFichaLocal(self, idFicha, vacDicc):
        for ficha in self.fichas:
            if ficha.getId() == idFicha:
                ficha.setVacFichaLocal(vacDicc)
    
    def setHospFichaLocal(self, idFicha, hospFicha, hosp):
        for ficha in self.fichas:
            if ficha.getId() == idFicha:
                ficha.setHospitalizacion(hosp)
                ficha.setHospFichaLocal(hospFicha)
    
    def setSedFichaLocal(self, idFicha, sedDicc, sedacion):
        for ficha in self.fichas:
            if ficha.getId() == idFicha:
                ficha.setSedacion(sedacion)
                ficha.setSedFichaLocal(sedDicc)
    
    def setTratamientoLocal(self, idFicha, tratamiento):
        for ficha in self.fichas:
            if ficha.getId() == idFicha:
                ficha.setTratamientoLocal(tratamiento)

    def setMedicamentosConsultaLocal(self, idFicha, medicamentos):
        for ficha in self.fichas:
            if ficha.getId() == idFicha:
                ficha.setMedicamentosConsultaLocal(medicamentos)


    def getFichas(self) -> list:
        return self.fichas

    def getId(self):
        return self.id
    
    def getId(self):
        return self.id
#setter
    def setId(self, id):
        self.id = id

    def setFichas(self, fichas):
        self.fichas.append(fichas)
    
    
    
    def setRegistroDeOperaciones(self, registroDeOperaciones):
        self.registroDeOperaciones = registroDeOperaciones """
