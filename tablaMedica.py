import mysql.connector

from fichaMedica import FichaMedica #importamos la clase 

class TablaMedica:

    listaDeFichasCorrespondientesTablaMedica = []

    def __init__(self, id):
        self.id = id
        self.fichas:FichaMedica = [] #arreglo 
        self.alergias = [] #diccionario
        self.registroDeOperaciones = [] #diccionario
        self.vacunasSuministradas = [] #diccionario
    

    def solicitarFichasEnBaseDeDatos(self, myCursor):
        sql = 'SELECT * FROM fichaMedica WHERE Tablamedica_idTablamedica = (%s)'
        myCursor.execute(sql, (str(self.id),))
        fichas = myCursor.fetchall()
        for ficha in fichas: #se recorren todas las ficha correspondientes a la tabla medica en particular 
            #las posiciones son correspondientes a el dato en la clase fichaMedica, se realiza de esta manera ya que lo que se entrega desde la base de datos es un aareglo de string por lo tanto se debe acceder a cada
            #posicion a fin de obtener los datos del mismo 

            #solicitamos todos los datos asociados en la base de datos
            
            self.agregarFichaMedicaExistente(ficha[0],ficha[2],ficha[3],ficha[4],ficha[5],ficha[6],ficha[7],ficha[8],ficha[9],ficha[10],ficha[11], ficha[12], myCursor)
            #self.fichas.append(fichaMedica)
    
    def solicitarFichasParcialesEnBaseDeDatos(self, myCursor):
        sql = 'SELECT idFichaMedica, fechaConsulta FROM fichaMedica WHERE Tablamedica_idTablamedica = (%s)' #seleccionamos solo el id y la fecha de creacion
        myCursor.execute(sql, (str(self.id),))
        fichas = myCursor.fetchall()
        for ficha in fichas: #se recorren todas las ficha correspondientes a la tabla medica en particular 
            print("35 tabla medica")
            self.agregarFichaMedicaParcial(ficha[0],ficha[1])
            #self.fichas.append(fichaMedica)


    def guardarTablaEnBaseDeDatos(self, myCursor, dB):
        sql = "INSERT INTO tablamedica values (%s)"
        myCursor.execute(sql, (str(self.id),))
        dB.commit()

    def agregarFichaMedicaConsultaATabla(self, idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, myCursor, dB):
        fichaMedicaConsulta = FichaMedica(idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp)
        self.fichas.append(fichaMedicaConsulta)
        self.guardarFichaGeneralEnBaseDeDatos(fichaMedicaConsulta, myCursor, dB)

    def agregarFichaMedicaExistente(self, idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, myCursor):
        fichaMedicaConsulta = FichaMedica(idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp)
        #print(fichaMedicaConsulta.getId())
        fichaMedicaConsulta.solicitarFichaDeHospitalizacionEnBaseDeDatos(myCursor)
        fichaMedicaConsulta.solicitarMedicamentosConsultaEnBaseDeDatos(myCursor)
        fichaMedicaConsulta.solicitarVacunacionEnBaseDeDatos(myCursor)
        fichaMedicaConsulta.solicitarFichaDeOperacionEnBaseDeDatos(myCursor)
        fichaMedicaConsulta.solicitarFichaDeSedacionEnBaseDeDatos(myCursor)
        fichaMedicaConsulta.solicitarTratamientosConsultaBaseDeDatos(myCursor)
        self.fichas.append(fichaMedicaConsulta)
    
    def agregarFichaMedicaParcial(self, idFicha, fechaConsulta):
        fichaMedicaConsulta = FichaMedica(idFicha, fechaConsulta)
        #print(fichaMedicaConsulta.getId())
        self.fichas.append(fichaMedicaConsulta)
    
    def completarFichaParcial(self, idFicha, myCursor):
        
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                print("70 tablaMedica llegue")
                sql = 'SELECT * FROM fichaMedica WHERE idFichaMedica = (%s)'
                myCursor.execute(sql, (str(idFicha),))
                fichas = myCursor.fetchall()

                ficha.setSucursalVeterinaria(fichas[0][2])
                ficha.setVeterinarioACargo(fichas[0][3])
                ficha.setOperacion(fichas[0][5])
                ficha.setFrecRespiratoria(fichas[0][6])
                ficha.setFrecCardiaca(fichas[0][7])
                ficha.setPeso(fichas[0][8])
                ficha.setEdad(fichas[0][9])
                ficha.setHospitalizacion(fichas[0][10])
                ficha.setSedacion(fichas[0][11])
                ficha.setTemp(fichas[0][12])

                if(fichas[0][5] == 1):
                    ficha.solicitarFichaDeOperacionEnBaseDeDatos(myCursor)
                
                if(fichas[0][10] == 1):
                    ficha.solicitarFichaDeHospitalizacionEnBaseDeDatos(myCursor)
                
                if(fichas[0][11] == 1):
                    ficha.solicitarFichaDeSedacionEnBaseDeDatos(myCursor)

                print("94 tablaMedica llegue")
                ficha.solicitarMedicamentosConsultaEnBaseDeDatos(myCursor)
                ficha.solicitarVacunacionEnBaseDeDatos(myCursor)
                ficha.solicitarTratamientosConsultaBaseDeDatos(myCursor)

                break

    def guardarFichaGeneralEnBaseDeDatos(self, fichaMedicaConsulta:FichaMedica, myCursor, dB):
        fichaMedicaConsulta.guardarFichaGeneralEnBaseDeDatos(self.getId(), myCursor, dB)

    def editarFichaMedicaConsulta(self, idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, myCursor, dB, fechaModificacion, vacunas, medicamentos, tratamientos):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                ficha.modificarFichaGeneralEnBaseDeDatos(sucursalVeterinaria, veterinarioACargo, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, myCursor, dB, fechaModificacion)
                ficha.actualizarVacunasConsultaEnBaseDeDatos(vacunas ,myCursor, dB)
                ficha.actualizarMedicamentosConsultaEnBaseDeDatos(medicamentos ,myCursor, dB)
                ficha.actualizarTratamientosConsultaEnBaseDeDatos(tratamientos ,myCursor, dB)
                self.editarRegistroVacunaEnBaseDeDatos(vacunas, myCursor, dB)
                break
    
    def editarFichaOperacion(self, idFicha, operacion, fechaUltimaModificacion, myCursor, dB):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                ficha.modificarOperacionEnBaseDeDatos(operacion, fechaUltimaModificacion, myCursor, dB)
    
    def editarFichaHospitalizacion(self, idFicha, hospitalizacion, fechaUltimaModificacion, myCursor, dB):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                ficha.modificarHopitalizacionEnBaseDeDatos(hospitalizacion, fechaUltimaModificacion, myCursor, dB)

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
    
    def setAlergiasBas(self, alergias, myCursor, dB):
        self.alergias = alergias
        self.guardarAlergiasEnBaseDeDatos(myCursor, dB)

    def solicitarAlergiasEnBaseDeDatos(self, myCursor):
        sql = 'SELECT * FROM Alergias WHERE TablaMedica_idTablaMedica = (%s)'
        myCursor.execute(sql, (str(self.getId()),))
        alergiasMascota = myCursor.fetchall()
        alergia = {}
        alergiasFinal = []
        for alergiaMascota in alergiasMascota:
            alergia = {
                'id': alergiaMascota[0],
                'nombre': alergiaMascota[1]
            }
            alergiasFinal.append(alergia)
        self.alergias = alergiasFinal

    def guardarAlergiasEnBaseDeDatos(self, myCursor, dB):
        for alergia in self.getAlergias():
            sql = "INSERT INTO alergias values (%s, %s, %s)"
            myCursor.execute(sql, (str(alergia['id']), str(alergia['nombre']), str(self.getId())))
            dB.commit()

    def getAlergias(self):
        return self.alergias

#alergias

#Registro de operaciones 

    def agregarOperaciones(self, operacion, myCursor, dB):
        self.registroDeOperaciones.append(operacion)

        sql = 'Insert INTO registroDeOperaciones VALUES (%s, %s,%s)'
        myCursor.execute(sql, (str(operacion['id']), str(operacion['operacion']),  str(self.getId())))
        dB.commit()
    
    def setRegistroDeOperaciones(self, operacion):
        self.registroDeOperaciones = operacion

    def editarRegistroDeOperaciones(self, operacion):
        for i in range(len(self.registroDeOperaciones)):
            if(self.registroDeOperaciones[i]['id'] == operacion['id']):
                self.registroDeOperaciones[i] = operacion
    
    def setRegistroDeOperacionesBas(self, operaciones, myCursor, dB): #local
        self.registroDeOperaciones = operaciones
        self.guardarOperacionesEnBaseDeDatos(myCursor, dB)

    def solicitarRegistroDeOperacionesEnBaseDeDatos(self, myCursor):
        sql = 'SELECT * FROM RegistroDeOperaciones WHERE TablaMedica_idTablaMedica = (%s)'
        myCursor.execute(sql, (str(self.getId()),))
        registroOperaciones = myCursor.fetchall()

        for operaciones in registroOperaciones:
            operacion = {
                'id': operaciones[0],
                'operacion': operaciones[1],
            }
            self.agregarOperaciones.append(operacion)
    
    def editarRegistroDeOperacionesEnBaseDeDatos(self, operacion, myCursor, dB):
        sql = 'UPDATE registroDeOperaciones SET operación = %s WHERE idRegistroDeOperaciones = %s'
        myCursor.execute(sql, (str(operacion['operacion']),  str(operacion['id'])))
        dB.commit()

        for i in range(len(self.registroDeOperaciones)):
            if(self.registroDeOperaciones[i]['id'] == operacion['id']):
                self.registroDeOperaciones[i] = operacion
                break

    def guardarOperacionesEnBaseDeDatos(self, myCursor, dB):
        for operacion in self.getRegistroDeOperaciones():
            sql = 'Insert INTO registroDeOperaciones VALUES (%s, %s,%s)'
            myCursor.execute(sql, (str(operacion['id']), str(operacion['operacion']),  str(self.getId())))
            dB.commit()

    def getRegistroDeOperaciones(self):
        return self.registroDeOperaciones

#Registro de operaciones 

#Vacunas suministradas 

    def agregarVacunas(self, vacunas, myCursor, dB):

        self.vacunasSuministradas.append(vacunas) #agregamos tanto las vacunas a la tabla como a la base de datos

        sql = 'INSERT INTO registrovacunassuministradas (idVacunasSuministradas, nombreVacuna, TablaMedica_idTablaMedica) VALUES (%s, %s, %s)'
        myCursor.execute(sql, (str(vacunas['id']), str(vacunas['nomVacuna']), str(self.getId())))
        dB.commit()

    def editarRegistroVacunaEnBaseDeDatos(self, vacunas ,myCursor, dB):
        for vacuna in vacunas:
            sql = 'UPDATE registrovacunassuministradas SET nombreVacuna = %s WHERE idVacunasSuministradas = %s'
            myCursor.execute(sql, (str(vacuna['nomVacuna']), str(vacuna['id'])))
            dB.commit()
        self.setRegistroDeVacunas(vacunas)

    def setRegistroDeVacunas(self, vacunas):
        self.vacunasSuministradas = vacunas 
    
    def solicitarVacunasEnBaseDeDatos(self, myCursor):
        sql = 'SELECT * FROM RegistroVacunasSuministradas WHERE TablaMedica_idTablaMedica = (%s)'
        myCursor.execute(sql, (str(self.getId()),))
        registroVacunas = myCursor.fetchall()

        for vacunas in registroVacunas:
            vacuna = {
                'id': vacunas[0],
                'nomVacuna': vacunas[1],
            }
            self.vacunasSuministradas.append(vacuna)

    def guardarRegistroVacunasEnBaseDeDatos(self, myCursor, dB):
        for vacunas in self.getVacunasSuministradas():
            sql = 'INSERT INTO registrovacunassuministradas (idVacunasSuministradas, nombreVacuna, TablaMedica_idTablaMedica) VALUES (%s, %s, %s)'
            myCursor.execute(sql, (str(vacunas['id']), str(vacunas['nomVacuna']), str(self.getId())))
            dB.commit()

    def getVacunasSuministradas(self):
        return self.vacunasSuministradas

#Vacunas suministradas 


#todos los set se realizaran sobre la ultima ficha agregada, esto debido a que solo la utima puede llegar a ser modificada o se agregaran datos 
#metodos de bajada de datos a clase inferior, fichas extra 

    def setFichaDeOperacion(self, opFicha, myCursor, dB): #se ocupa el id para identificar la ficha especifica a la que añadir
        self.fichas[len(self.fichas)-1].setFichaOperacion(opFicha, myCursor, dB) #siempre se agrega a la ultima ficha generada
    
    def setFichaDeHospitalizacion(self, hospFicha, myCursor, dB): #se ocupa el id para identificar
        self.fichas[len(self.fichas)-1].setFichaDeHospitalizacion(hospFicha, myCursor, dB)
    
    def setFichaDeSefacion(self, sedFicha, myCursor, dB): #se ocupa el id
        self.fichas[len(self.fichas)-1].setFichaDeSefacion(sedFicha, myCursor, dB)
    
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
    
    def setTratamientos(self, tratamiento, myCursor, dB):
        self.fichas[len(self.fichas)-1].setTratamientosConsulta(tratamiento, myCursor, dB)

    def setMedicamentos(self, medicamentos, myCursor, dB):
        self.fichas[len(self.fichas)-1].setMedicamentosConsulta(medicamentos, myCursor, dB)

    def setVacunas(self, operacion, myCursor, dB):
        self.fichas[len(self.fichas)-1].setVacunacion(operacion, myCursor, dB)
  

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
                return ficha.getTemp()

    def getVeterinarioACargo(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getVeterinarioACargo()

    def getFechaConsulta(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getFechaConsulta()

    def getFechaModificacion(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getFechaModificacion()

    def getMedicamentosConsulta(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                print("371 tablaMedica "+str(ficha.getMedicamentosConsulta()))
                return ficha.getMedicamentosConsulta()

    def getOperacion(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getOperacion()

    def getOperacionFicha(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getOperacionFicha()
    
    def getIdOperacion(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getIdOperacion()
    
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
    
    def getIdHospitalizacion(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                return ficha.getIdHospitalizacion()
    
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
                #print("hola soy tu validacion de tratamiento")
                return ficha.getTratamiento()

    def getId(self):
        return self.id

    def getidFichaActual(self):
        for ficha in self.fichas:
            if(ficha.getActual() == True):
                return ficha.getId()

    def getIdsFichas(self)->list:
        fichasTrabajar = self.fichas
        listRetorno = []
        for ficha in fichasTrabajar:
            listRetorno.append(ficha.getId())

        return listRetorno

    def setActualFichaMedicaConsulta(self, fecha, actual):
        for ficha in self.fichas:
            if(str(ficha.getFechaConsulta()) in fecha):
                ficha.setActual(actual)

    def quitarActualFichaMedica(self, idFicha):
        for ficha in self.fichas:
            if(ficha.getId() == idFicha):
                ficha.setActual(False)
    
                
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
