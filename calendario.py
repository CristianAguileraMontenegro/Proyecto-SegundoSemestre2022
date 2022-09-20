from operator import truediv
from sqlite3 import Date
import mysql.connector


db = mysql.connector.connect(
    user='root',
    password='root',
    host='localhost',
    database='mydb',
    port='3306'
)

mycursor = db.cursor()

class Calendario:

    def __init__(self): #debido al funcionamiento de python
        #solo manejaremos un constructor que sera ocupado para principalmente el manejo en base de datos, pero tambien para el ingresao normal 

        self.fechasAsignadas = []
        self.horasAsignadas = []
        self.minutos = []
        self.comentarios =  []                                 
        self.telefonos = []
        self.ruts = []

    
    def verificarFecha(self, fecha):
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha):
                print("validacion funciono")
                return True
        return False


    def agregarDatosAFecha(self, fecha, rut, telefono, horas, minutos):
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha):
                self.fechasAsignadas[i]["ruts"].append(rut)
                self.fechasAsignadas[i]["minutos"].append(minutos)
                self.fechasAsignadas[i]["horas"].append(horas)
                self.fechasAsignadas[i]["numeros"].append(telefono)

                
    def getFecha(self, fecha):
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha):
                return self.fechasAsignadas[i]
        return False
    
    
    def getFechas(self):
        return self.fechasAsignadas
    
    def getHorasAsignadas(self):
        return self.horasAsignadas
    
    def getMinutosAsignadas(self):
        return self.minutos

    def getComentarios(self):
        return self.comentarios

    def getTelefonos(self):
        return self.telefonos

    def getRuts(self):
        return self.ruts
    
    def setFechas(self, fechas):
        self.fechasAsignadas = fechas

    def setHoras(self, horas):
        self.horasAsignadas = horas
    
    def setMinutos(self, minutos):
        self.minutos = minutos
    
    def setComentarios(self, comentarios):
        self.comentarios = comentarios
    
    def setTelefonos(self, telefonos):
        self.telefonos = telefonos
    
    def setRuts(self, ruts):
        self.ruts = ruts
    
    def agregarFechas(self, fecha:Date):
        self.fechasAsignadas.append(fecha)
    
    def agregarHoras(self, horas):
        self.horasAsignadas.append(horas)
    
    def agregarMinutos(self, minutos):
        self.minutos.append(minutos)
    
    def agregarComentarios(self, comentarios):
        self.comentarios.append(comentarios)
    
    def agregarTelefonos(self, telefono):
        self.telefonos.append(telefono)
    
    def agregarRuts(self, rut):
        self.ruts.append(rut)
    
    def guardarFechasEnBaseDeDatos(self):
        pass
        
        

    