import mysql.connector
from tablaMedica import TablaMedica

class Mascota:

    #self, id, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, tablaMedica
    def __init__(self, *args):

        if(len(args) == 1):
            self.nombre = None
            self.id = args[0]
            self.especie = None
            self.color = None
            self.raza = None
            self.nombreTutor = None
            self.rutTutor = None
            self.numeroTelefono = None
            self.direccion = None
            self.tablaMedica:TablaMedica = None
            self.FechaNacimiento = None
            self.alergias = [] #diccionario
        elif(len(args) == 11):
            print("hola llegue a entrar")
            self.nombre = args[1]
            self.id = args[0]
            self.especie = args[2]
            self.color = args[3]
            self.raza = args[4]
            self.nombreTutor = args[5]
            self.rutTutor = args[6]
            self.numeroTelefono = args[7]
            self.direccion = args[8]
            self.tablaMedica:TablaMedica = args[9]
            self.FechaNacimiento = args[10]
            self.alergias = [] #diccionario
    
    def agregarMascotaEnBaseDeDatos(self, myCursor, dB):
        sql = "INSERT INTO mascota (idMascota, nombreMascota, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, Dirección, FechaDeNacimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        myCursor.execute(sql, (str(self.id), str(self.nombre), str(self.especie), str(self.color), str(self.raza), str(self.nombreTutor), str(self.rutTutor), str(self.numeroTelefono), str(self.direccion), str(self.FechaNacimiento)))
        dB.commit()
    
    def actualizarMascota(self, myCursor, dB):
        sql = "UPDATE mascota SET nombreMascota = %s, especie = %s, color = %s, raza = %s, nombreTutor = %s, rutTutor = %s, numeroTelefono = %s, Dirección = %s,  FechaDeNacimiento = %s WHERE idMascota = %s"
        myCursor.execute(sql, (str(self.nombre), str(self.especie), str(self.color), str(self.raza), str(self.nombreTutor), str(self.rutTutor), str(self.numeroTelefono), str(self.direccion), str(self.FechaNacimiento), str(self.id)))
        dB.commit()
    
    def agregarTablaMascota(self, idTerminal, myCursor, dB):
        sql = "INSERT INTO mascota_has_terminalveterinario values (%s, %s)"
        myCursor.execute(sql, (str(self.id), str(idTerminal)))
        dB.commit()

    def solicitarFichasEnBaseDeDatos(self, myCursor):
        self.tablaMedica.solicitarFichasEnBaseDeDatos(myCursor)
    
    def solicitarFichasParcialesEnBaseDeDatos(self, myCursor, idTabla):
        print("57 mascota -------------------")
        self.tablaMedica.solicitarFichasParcialesEnBaseDeDatos(myCursor, idTabla)
    
    def completarFichaParcial(self, idFicha, myCursor):
        self.tablaMedica.completarFichaParcial(idFicha, myCursor)
    
    def editarFichaMedicaConsulta(self, idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, myCursor, dB, fechaModificacion, vacunas, medicamentos, consulta):
        self.tablaMedica.editarFichaMedicaConsulta(idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, myCursor, dB, fechaModificacion, vacunas, medicamentos, consulta)

    def editarFichaOperacion(self, idFicha, operacion, fechaUltimaModificacion, myCursor, dB):
        self.tablaMedica.editarFichaOperacion(idFicha, operacion, fechaUltimaModificacion, myCursor, dB)
    
    def solicitarVacunasEnBaseDeDatos(self, myCursor):
        self.tablaMedica.solicitarVacunasEnBaseDeDatos(myCursor)
    
    def editarRegistroDeOperaciones(self, operacion, myCursor, dB):
        self.tablaMedica.editarRegistroDeOperacionesEnBaseDeDatos(operacion, myCursor, dB)
    
    def solicitarRegistroDeOperacionesEnBaseDeDatos(self, myCursor):
        self.tablaMedica.solicitarRegistroDeOperacionesEnBaseDeDatos(myCursor)
    
    def editarFichaHospitalizacion(self, idFicha, hospitalización, fechaUltimaModificacion, myCursor, dB):
        self.tablaMedica.editarFichaHospitalizacion(idFicha, hospitalización, fechaUltimaModificacion, myCursor, dB)
    
    def editarReceta(self, idFicha, receta, fechaUltimaModificacion, myCursor, dB):
        self.tablaMedica.editarReceta( idFicha, receta, fechaUltimaModificacion, myCursor, dB)

    def getId(self):
        return self.id
    
    def getNombreMascota(self):
        return self.nombre

    def getColorMascota(self):
        return self.color

    def getEspecie(self):
        return self.especie

    def getRaza(self):
        return self.raza

    def getNombreTutor(self):
        return self.nombreTutor

    def getRutTutor(self):
        return self.rutTutor

    def getNumeroTelefono(self):
        return self.numeroTelefono

    def getDireccion(self):
        return self.direccion

    def getFechaDeNacimiento(self):
        return self.FechaNacimiento
    
    def setId(self, id):
        self.id = id
    
    def setNombreMascota(self, nombre):
        self.nombre = nombre

    def setColorMascota(self, color):
        self.color = color

    def setEspecie(self, especie):
        self.especie = especie

    def setRaza(self, raza):
        self.raza = raza

    def setNombreTutor(self, nombreTutor):
        self.nombreTutor = nombreTutor

    def setRutTutor(self, rutTutor):
        self.rutTutor = rutTutor

    def setNumeroTelefono(self, numeroTelefono):
        self.numeroTelefono = numeroTelefono

    def setDireccion(self, direccion):
        self.direccion = direccion
    
    def setFechaNacimiento(self, fechaNacimiento):
        self.FechaNacimiento = fechaNacimiento
    
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
        sql = 'SELECT * FROM Alergias WHERE Mascota_idMascota = (%s)'
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
    
    def getIDAlergias(self):
        ids = []
        for alergia in self.getAlergias():
            ids.append(alergia)

        return ids
    
    def editarRegistroDeAlergias(self, myCursor, dB):
        for i in range(len(self.alergias)):
            sql = 'UPDATE alergias SET nombreAlergia = %s WHERE idAlergias = %s'
            myCursor.execute(sql, (str(self.alergias[i]['nombre']),  str(self.alergias[i]['id'])))
            dB.commit()

#alergias

    #metodos de bajada para la tabla
    

    def agregarTablaMedica(self, id):
        self.tablaMedica = TablaMedica(id)
        #self.guardarTablaEnBaseDeDatos()

    def guardarTablaEnBaseDeDatos(self, myCursor, dB, idVeterinaria, nombreVeterinaria, idMascota):
        self.tablaMedica.guardarTablaEnBaseDeDatos(myCursor, dB, idVeterinaria, nombreVeterinaria, idMascota)
    
    def setRegistroDeOperaciones(self, operaciones):
        self.tablaMedica.setRegistroDeOperaciones(operaciones)
    
    def setRegistroDeOperacionesBas(self, operaciones, myCursor, dB):
        self.tablaMedica.setRegistroDeOperacionesBas(operaciones, myCursor, dB)
    
    def agregarOperaciones(self, operacion, myCursor, dB):
        self.tablaMedica.agregarOperaciones(operacion, myCursor, dB)
    
    def agregarOperacionesSinBd(self, operacion):
        self.tablaMedica.agregarOperacionesSinBd(operacion)

    def setRegistroDeVacunas(self, vacunas):
        self.tablaMedica.setRegistroDeVacunas(vacunas)
    
    def agregarVacunas(self, vacuna, myCursor, dB):
        self.tablaMedica.agregarVacunas(vacuna, myCursor, dB)

    def agregarVacunasSinBd(self, vacuna):
        self.tablaMedica.agregarVacunasSinBd(vacuna)

    #metodos de bajada para la tabla

    #metodos de subida para tabla
    
    def getRegistroDeOperaciones(self):
        return self.tablaMedica.getRegistroDeOperaciones()

    def getVacunasSuministradas(self):
        return self.tablaMedica.getVacunasSuministradas()

    #metodos de subida para tabla

    # metodos de bajada para ficha

    def agregarFichaMedicaConsultaATabla(self, idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, myCursor, dB):
        self.tablaMedica.agregarFichaMedicaConsultaATabla(idFicha, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, myCursor, dB)
        

    def setIdFicha(self, idFicha): 
        self.tablaMedica.setIdFicha(idFicha)
    
    def setSucursalVeterinariaFicha(self, sucursalVeterinaria):
        self.tablaMedica.setSucursalVeterinariaFicha(sucursalVeterinaria)
    
    def setVeterinarioACargoFicha(self, veterinarioACargo):
        self.tablaMedica.setVeterinarioACargoFicha(veterinarioACargo)

    def setFechaConsultaFicha(self, fechaConsulta):
        self.tablaMedica.setFechaConsultaFicha(fechaConsulta)
    
    def setFrecRespiratoriaFicha(self, frecRespiratoria):
        self.tablaMedica.setFrecRespiratoriaFicha(frecRespiratoria)
    
    def setFrecCardiacaFicha(self, frecCardiaca):
        self.tablaMedica.setFrecCardiacaFicha(frecCardiaca)
    
    def setPesoFicha(self, peso):
        self.tablaMedica.setPesoFicha(peso)

    def setEdadFicha(self, edad):
        self.tablaMedica.setEdadFicha(edad)

    def setTempFicha(self, temp):
        self.tablaMedica.setTempFicha(temp)

    def setFichaDeOperacion(self, idFicha, opFicha, myCursor, dB): #se ocupa el id para identificar la ficha especifica a la que añadir
        self.tablaMedica.setFichaDeOperacion(idFicha, opFicha, myCursor, dB)
    
    def setFichaDeHospitalizacion(self, idFicha,hospFicha, myCursor, dB): #se ocupa el id para identificar
        self.tablaMedica.setFichaDeHospitalizacion(idFicha,hospFicha, myCursor, dB)
    
    def setFichaDeSefacion(self, idFicha,sedFicha, myCursor, dB): #se ocupa el id
        self.tablaMedica.setFichaDeSefacion(idFicha,sedFicha, myCursor, dB)
    
    def setOperacionFicha(self, idFicha,operacion): #indicadores de que existe una ficha de cada tipo
        self.tablaMedica.setOperacionFicha(idFicha,operacion)
    
    def setHospitalizacionFicha(self, idFicha,hospitalizacion):
        self.tablaMedica.setHospitalizacionFicha(idFicha,hospitalizacion)

    def setSedacionFicha(self, idFicha,sedacion):
        self.tablaMedica.setSedacionFicha(idFicha,sedacion)

    def setTratamientos(self, tratamiento, myCursor, dB):
        self.tablaMedica.setTratamientos(tratamiento, myCursor, dB)

    def setMedicamentos(self, medicamentos, myCursor, dB):
        self.tablaMedica.setMedicamentos(medicamentos, myCursor, dB)

    def setVacunas(self, vacunas, myCursor, dB):
        self.tablaMedica.setVacunas(vacunas, myCursor, dB)
    
    def setReceta(self, idFicha, receta, myCursor, dB):
        self.tablaMedica.setReceta(idFicha, receta, myCursor, dB)

    # metodos de subida para ficha

    def getIdFicha(self, idFicha):
        return self.tablaMedica.getIdFicha(idFicha)

    def getIdsFichas(self) ->list:
        return self.tablaMedica.getIdsFichas()
    
    def getSucursalVeterinaria(self, idFicha):
        return self.tablaMedica.getSucursalVeterinaria(idFicha)

    def getTemp(self, idFicha):
        return self.tablaMedica.getTemp(idFicha)

    def getVeterinarioACargo(self, idFicha):
        return self.tablaMedica.getVeterinarioACargo(idFicha)

    def getFechaConsulta(self, idFicha):
        return self.tablaMedica.getFechaConsulta(idFicha)

    def getFechaModificacion(self, idFicha):
        return self.tablaMedica.getFechaModificacion(idFicha)

    def getMedicamentosConsulta(self, idFicha):
        return self.tablaMedica.getMedicamentosConsulta(idFicha)

    def getOperacion(self, idFicha):
        return self.tablaMedica.getOperacion(idFicha)

    def getOperacionFicha(self, idFicha):
        return self.tablaMedica.getOperacionFicha(idFicha)

    def getIdOperacion(self, idFicha):
        return self.tablaMedica.getIdOperacion(idFicha)
    
    def getVacunasSuministradasConsulta(self, idFicha):
        return self.tablaMedica.getVacunasSuministradasConsulta(idFicha)

    def getFrecRespiratoria(self, idFicha):
        return self.tablaMedica.getFrecRespiratoria(idFicha)
    
    def getFrecCardiaca(self, idFicha):
        return self.tablaMedica.getFrecCardiaca(idFicha)
    
    def getPeso(self, idFicha):
        return self.tablaMedica.getPeso(idFicha)
    
    def getEdad(self, idFicha):
        return self.tablaMedica.getEdad(idFicha)
    
    def getHospitalizacion(self, idFicha):
        return self.tablaMedica.getHospitalizacion(idFicha)
    
    def getHospitalizacionFicha(self, idFicha):
        return self.tablaMedica.getHospitalizacionFicha(idFicha)
    
    def getIdHospitalizacion(self, idFicha):
        return self.tablaMedica.getIdHospitalizacion(idFicha)
    
    def getSedacion(self, idFicha):
        return self.tablaMedica.getSedacion(idFicha)
    
    def getSedacioFicha(self, idFicha):
        return self.tablaMedica.getSedacioFicha(idFicha)
    
    def getTratamiento(self, idFicha):
        return self.tablaMedica.getTratamiento(idFicha)
    
    def getReceta(self, idFicha):
        return self.tablaMedica.getReceta(idFicha)
    
    def getIdReceta(self, idFicha):
        return self.tablaMedica.getIdReceta(idFicha)

    def setActualFichaMedicaConsulta(self, fecha, actual):
        self.tablaMedica.setActualFichaMedicaConsulta(fecha, actual)

    def quitarActualFichaMedicaConsulta(self, idFicha):
        self.tablaMedica.quitarActualFichaMedica(idFicha)

    def getidFichaActual(self):
        return self.tablaMedica.getidFichaActual()


    """def setOpFichaLocal(self, idFicha, opDicc, operacion):
        self.tablaMedica.setOpFichaLocal(idFicha, opDicc, operacion)

    def setVacFichaLocal(self, idFicha, vacDicc):
        self.tablaMedica.setVacFichaLocal(idFicha, vacDicc)

    def setHospFichaLocal(self, idFicha, hospFicha, hosp):
        self.tablaMedica.setHospFichaLocal(idFicha, hospFicha, hosp)

    def setSedFichaLocal(self, idFicha, sedDicc, sedacion):
        self.tablaMedica.setSedFichaLocal(idFicha, sedDicc, sedacion)

    def setTratamientoLocal(self, idFicha, tratamiento):
        self.tablaMedica.setTratamientoLocal(idFicha, tratamiento)

    def setMedicamentosConsultaLocal(self, idFicha, medicamentos):
        self.tablaMedica.setMedicamentosConsultaLocal(idFicha, medicamentos)

    def setRegistroDeOperaciones(self, operacion):
        self.tablaMedica.setRegistroDeOperacionesTrue(operacion)
        print(operacion)
    
    def setRegistroDeVacunas(self, vacuna):
        self.tablaMedica.setRegistroDeVacunasTrue(vacuna)

    def setRegistroAlergias(self, alergias):
        self.tablaMedica.setAlergiasTrue(alergias)

    #def editarInfoBasicaMascota(self):
        #pass

    def crearFichaMedicaConsulta(self,fichaMedica):
        pass

    # def editarFichaMedicaConsulta(self,fichaMedica):
    #     pass

    

    # def validarFormatoDatosFichaMedicaGeneral():
    #     pass

    # def validarFormatoDatosFichaMedica():
    #     pass

    # def solicitudServCrear():
    #     pass

    # def solicitudServEditar():
    #     pass

    
    #faltan Getter y Setters"""