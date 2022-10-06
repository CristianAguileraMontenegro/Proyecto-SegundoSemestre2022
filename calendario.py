from datetime import datetime
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

    def __init__(self, idCalendario): #debido al funcionamiento de python
        #solo manejaremos un constructor que sera ocupado para principalmente el manejo en base de datos, pero tambien para el ingresao normal 
        self.idCalendario = idCalendario
        self.fechasAsignadas = []
    
    def getId(self):
        return self.idCalendario
    
    def verificarFecha(self, fecha): #verificamos que la fecha ya haya sido agregada previamente
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha):
                print("validacion funciono")
                return True
        return False
    
    def agregarFechas(self, fecha):
        self.fechasAsignadas.append(fecha) #agregamos la fecha al arreglos
        self.guardarDatosDeCalendarioEnBaseDeDatos(0)

    def agregarFechasSinGuardadoEnBaseDeDatos(self, fecha):
        self.fechasAsignadas.append(fecha)

    def agregarDatosAFecha(self, fecha, rut, telefono, horas, minutos): #agregamos datos a una fecha ya existente 
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha):
                self.fechasAsignadas[i]["ruts"].append(rut)
                self.fechasAsignadas[i]["minutos"].append(minutos)
                self.fechasAsignadas[i]["horas"].append(horas)
                self.fechasAsignadas[i]["numeros"].append(telefono)
                self.guardarDatosDeCalendarioEnBaseDeDatos(i)
       
    
    def agregarDatosAFechaSinGuardadoEnBaseDeDatos(self, fecha, rut, telefono, horas, minutos): #agregamos datos a una fecha ya existente 
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha):
                self.fechasAsignadas[i]["ruts"].append(rut)
                self.fechasAsignadas[i]["minutos"].append(minutos)
                self.fechasAsignadas[i]["horas"].append(horas)
                self.fechasAsignadas[i]["numeros"].append(telefono)
                print(str(self.fechasAsignadas[i]))

                
    def getFecha(self, fecha):
        for i in range(len(self.fechasAsignadas)): #recorremos las fechas y obetemos la elegida
            if (self.fechasAsignadas[i]["fecha"] == fecha):
                return self.fechasAsignadas[i]
        return False

    def getFechas(self): #obtenemos todas las fechas
        return self.fechasAsignadas
    
    #def guardarCalendariosEnBaseDeDatos(self, idVeterinaria, nombreVeterinaria):
     #   sql = 'INSERT INTO calendario (Veterinaria_idVeterinaria, Veterinaria_nombreVeterinaria) VALUES (%s, %s)' 
      #  mycursor.execute(sql, (str(idVeterinaria), str(nombreVeterinaria),)) #cambiar al terminal en el que nos encontramos
       # db.commit()

    def guardarDatosDeCalendarioEnBaseDeDatos(self, idFecha):

        ulitmo =  len(self.fechasAsignadas[idFecha]["numeros"])-1 #ocupamos ultimo para identificar la ultimo hora, minuot, rut y numero gingresda y que sera guardado en la base de datos
        fecha = self.fechasAsignadas[idFecha]["fecha"].split('/')
        fechaCompleta = str(fecha[2])+"-"+str(fecha[1])+"-"+str(fecha[0])+" "+str(self.fechasAsignadas[idFecha]["horas"][ulitmo])+":"+str(self.fechasAsignadas[idFecha]["minutos"][ulitmo])+":00"

        sql = 'INSERT INTO fechassolicitadas(FechasSolicitadascol, Rut, NumeroDeContacto, Calendario_idCalendario) VALUES (%s, %s, %s, %s)'
        mycursor.execute(sql, (str(fechaCompleta), str(self.fechasAsignadas[idFecha]["ruts"][ulitmo]), str(self.fechasAsignadas[idFecha]["numeros"][ulitmo]), "1")) #cambiar al terminal en el que nos encontramos
        db.commit()

    def solicitarDatosCalendarioBaseDeDatos(self):

        sql = 'SELECT * FROM fechassolicitadas WHERE Calendario_idCalendario = (%s) AND FechasSolicitadascol >= CURDATE() ' #solo tomamos aquellas fechas que sean de el dia actual en adelante
        mycursor.execute(sql, (str(self.idCalendario),))
        DatosCalendario = mycursor.fetchall()

        if(DatosCalendario != None):
            self.ProcesarDatosBaseDeDatos(DatosCalendario)

    def ProcesarDatosBaseDeDatos(self, datosCalendario):

        for i in range(len(datosCalendario)):
            #en total son 4 campos de los que sacar datos

            fecha = '%02d' % datosCalendario[i][1].day+'/'+ '%02d' % datosCalendario[i][1].month +'/'+str(datosCalendario[i][1].year) #dado que los datos de la cita son un objeto datetime podemos ocupar sus metodos para sacar lso datos
            hora = str(datosCalendario[i][1].hour)
            minutos = str(datosCalendario[i][1].minute)
            rut = str(datosCalendario[i][2])
            numero = str(datosCalendario[i][3])

            print(str(datosCalendario[i][1]))
            print("hola")
            fechas = {'fecha': fecha, 'ruts':[], 'numeros':[], 'horas':[], 'minutos':[]}

            self.agregarFechasSinGuardadoEnBaseDeDatos(fechas)
            self.agregarDatosAFechaSinGuardadoEnBaseDeDatos(fecha, rut, numero, hora, minutos)
    
    
    
    
    
    """def getFechas(self):
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
        pass"""
        
        

    