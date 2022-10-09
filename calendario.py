from datetime import datetime
from operator import truediv
from sqlite3 import Date
import mysql.connector


class Calendario:

    def __init__(self, *args): #debido al funcionamiento de python
        #solo manejaremos un constructor que sera ocupado para principalmente el manejo en base de datos, pero tambien para el ingresao normal 
        if(len(args) == 0):
            self.idCalendario = None
            self.fechasAsignadas = []
        elif( len(args) == 1 ):
            print("15 calendario "+str(args[0]))
            self.idCalendario = args[0]
            self.fechasAsignadas = []

    def getId(self):
        return self.idCalendario
    
    def setId(self, idCalendario):
        self.idCalendario = idCalendario
    
    def verificarFecha(self, fecha): #verificamos que la fecha ya haya sido agregada previamente
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha):
                
                return True
        
        return False
    
    def agregarFechas(self, fecha, mycursor, db):
        self.fechasAsignadas.append(fecha) #agregamos la fecha al arreglos
        print("32 calendario")
        self.guardarDatosDeCalendarioEnBaseDeDatos(0, mycursor, db)

    def agregarFechasSinGuardadoEnBaseDeDatos(self, fecha, diccionarioDeFecha):
        if(self.verificarFecha(fecha) == False): #si ya existe la fecha no se agrega nuevamente, esto se hace ya que desde la base de datos habran muchas horas asignadas a las fechas, por que para evitar repeticiones debemos verificar
            print("40 calendario :" +str(fecha))
            self.fechasAsignadas.append(diccionarioDeFecha)
    


    def agregarDatosAFecha(self, fecha, rut, telefono, horas, minutos, mycursor, db): #agregamos datos a una fecha ya existente 
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha):
                self.fechasAsignadas[i]["ruts"].append(rut)
                self.fechasAsignadas[i]["minutos"].append(minutos)
                self.fechasAsignadas[i]["horas"].append(horas)
                self.fechasAsignadas[i]["numeros"].append(telefono)
                self.guardarDatosDeCalendarioEnBaseDeDatos(i, mycursor, db)
       
    
    def agregarDatosAFechaSinGuardadoEnBaseDeDatos(self, fecha, rut, telefono, horas, minutos): #agregamos datos a una fecha ya existente 
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha):
                self.fechasAsignadas[i]["ruts"].append(rut)
                self.fechasAsignadas[i]["minutos"].append(minutos)
                self.fechasAsignadas[i]["horas"].append(horas)
                self.fechasAsignadas[i]["numeros"].append(telefono)
    

                
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

    def guardarDatosDeCalendarioEnBaseDeDatos(self, idFecha, mycursor, db):

        ulitmo =  len(self.fechasAsignadas[idFecha]["numeros"])-1 #ocupamos ultimo para identificar la ultimo hora, minuot, rut y numero gingresda y que sera guardado en la base de datos
        fecha = self.fechasAsignadas[idFecha]["fecha"].split('/')
        fechaCompleta = str(fecha[2])+"-"+str(fecha[1])+"-"+str(fecha[0])+" "+str(self.fechasAsignadas[idFecha]["horas"][ulitmo])+":"+str(self.fechasAsignadas[idFecha]["minutos"][ulitmo])+":00"

        print("80 calendario :"+str(self.idCalendario))
        sql = 'INSERT INTO fechassolicitadas (FechasSolicitadascol, Rut, NumeroDeContacto, Calendario_idCalendario) VALUES (%s, %s, %s, %s)'
        mycursor.execute(sql, (str(fechaCompleta), str(self.fechasAsignadas[idFecha]["ruts"][ulitmo]), str(self.fechasAsignadas[idFecha]["numeros"][ulitmo]), str(self.idCalendario))) #cambiar al terminal en el que nos encontramos
        db.commit()

        print("81 calendario")

    def solicitarDatosCalendarioBaseDeDatos(self, mycursor):

        sql = 'SELECT * FROM fechassolicitadas WHERE Calendario_idCalendario = (%s) AND FechasSolicitadascol >= CURDATE() ' #solo tomamos aquellas fechas que sean de el dia actual en adelante
        mycursor.execute(sql, (str(self.idCalendario),))
        DatosCalendario = mycursor.fetchall()

        if(DatosCalendario != None):
            self.ProcesarDatosBaseDeDatos(DatosCalendario)

    def ProcesarDatosBaseDeDatos(self, datosCalendario):

        print("99 Calendario :"+str(len(datosCalendario)))
        for i in range(len(datosCalendario)):
            #en total son 4 campos de los que sacar datos

            fecha = '%02d' % datosCalendario[i][1].day+'/'+ '%02d' % datosCalendario[i][1].month +'/'+str(datosCalendario[i][1].year) #dado que los datos de la cita son un objeto datetime podemos ocupar sus metodos para sacar lso datos
            hora = str(datosCalendario[i][1].hour)
            minutos = str(datosCalendario[i][1].minute)
            rut = str(datosCalendario[i][2])
            numero = str(datosCalendario[i][3])

            
            diccionarioDeFecha = {'fecha': fecha, 'ruts':[], 'numeros':[], 'horas':[], 'minutos':[]}

            self.agregarFechasSinGuardadoEnBaseDeDatos(fecha, diccionarioDeFecha)
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
        
        

    