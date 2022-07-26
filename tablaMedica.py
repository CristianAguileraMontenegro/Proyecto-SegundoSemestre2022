from typing_extensions import Self
import mysql.connector

from fichaMedica import FichaMedica #importamos la clase 

db = mysql.connector.connect(
    user='root',
    password='root',
    host='localhost',
    database='mydb',
    port='3306'
)


mycursor = db.cursor()

class TablaMedica:

    listaDeFichasCorrespondientesTablaMedica = []

    def __init__(self, id, alergias, registroDeOperaciones, vacunasSuministradas):
        self.id = id
        self.fichas = [] #arreglo 
        self.alergias = [] #diccionario
        self.registroDeOperaciones = [] #diccionario
        self.vacunasSuministradas = [] #diccionario
    

    def solicitarFichasEnBaseDeDatos(self):
        sql = 'SELECT * FROM fichaMedica WHERE Tablamedica_idTablamedica = (%s)'
        mycursor.execute(sql, (str(self.id),))
        fichas = mycursor.fetchall()
        for ficha in fichas: #se recorren todas las ficha correspondientes a la tabla medica en particular 
            fichaMedica = FichaMedica(ficha[0],ficha[1],ficha[2],ficha[3],ficha[4],ficha[5],ficha[6],ficha[7],ficha[8],ficha[9],ficha[10],ficha[11], ficha[12]) 
            #las posiciones son correspondientes a el dato en la clase fichaMedica, se realiza de esta manera ya que lo que se entrega desde la base de datos es un aareglo de string por lo tanto se debe acceder a cada
            #posicion a fin de obtener los datos del mismo 

            #solicitamos todos los datos asociados en la base de datos
            fichaMedica.solicitarFichaDeHospitalizacionEnBaseDeDatos()
            fichaMedica.solicitarMedicamentosConsultaEnBaseDeDatos()
            fichaMedica.solicitarVacunacionEnBaseDeDatos()
            fichaMedica.solicitarFichaDeHospitalizacionEnBaseDeDatos()
            fichaMedica.solicitarFichaDeSedacionEnBaseDeDatos()
            fichaMedica.solicitarTratamientosConsultaBaseDeDatos()
            self.fichas.append(fichaMedica)


    def agregarFichaMedicaConsultaATabla(self, fichaMedicaConsulta:FichaMedica):
        self.fichas.append(fichaMedicaConsulta)

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

    def setRegistroDeOperacionesTrue(self, operacion): #local
        print("----------")
        self.registroDeOperaciones.append(operacion)
        

#alergias
    def agregarAlergias(self, alergia):
        self.alergias.append(alergia)
    
    def setAlergias(self, alergias):
        self.alergias = alergias
        self.guardarAlergiasEnBaseDeDatos()
    
    def solicitarAlergiasEnBaseDeDatos(self, idMascota):
        sql = 'SELECT * FROM Alergias WHERE TablaMedica_idTablaMedica = (%s)'
        mycursor.execute(sql, (str(idMascota),))
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

















    def setRegistroDeVacunasTrue(self, vacuna):
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

    def getAlergias(self):
        return self.alergias
    
    def getRegistroDeOperaciones(self):
        return self.registroDeOperaciones
    
    def getVacunasSuministradas(self):
        return self.vacunasSuministradas
    
    def getId(self):
        return self.id
#setter
    def setId(self, id):
        self.id = id

    def setFichas(self, fichas):
        self.fichas.append(fichas)
    
    
    
    def setRegistroDeOperaciones(self, registroDeOperaciones):
        self.registroDeOperaciones = registroDeOperaciones
