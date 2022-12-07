from datetime import datetime
from operator import truediv
from sqlite3 import Date
import mysql.connector
import uuid

class Calendario:

    def __init__(self, *args): #debido al funcionamiento de python
        #solo manejaremos un constructor que sera ocupado para principalmente el manejo en base de datos, pero tambien para el ingresao normal 
        if(len(args) == 0):
            self.idCalendario = None
            self.fechasAsignadas = []
        elif( len(args) == 1 ):
            self.idCalendario = args[0]
            self.fechasAsignadas = []

    def getId(self):
        return self.idCalendario
    
    def setId(self, idCalendario):
        self.idCalendario = idCalendario
    
    def agregarCalendarioBaseDeDatos(self, idVeterinaria, nombreVeterinaria, mycursor, db):
        sql = 'INSERT INTO calendario VALUES (%s, %s, %s)'
        mycursor.execute(sql, (str(self.idCalendario), str(idVeterinaria), str(nombreVeterinaria)))
        db.commit()
    
    def getFecha(self, fecha):
        for i in range(len(self.fechasAsignadas)): #recorremos las fechas y obetemos la elegida
            if (self.fechasAsignadas[i]["fecha"] == fecha):
                return self.fechasAsignadas[i]
        return False

    def getFechas(self): #obtenemos todas las fechas
        return self.fechasAsignadas
    
    def verificarFecha(self, fecha): #verificamos que la fecha ya haya sido agregada previamente
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha):
                
                return True
        
        return False
    
    def verificarFechaHorario(self, fecha, horaInicial, horaFinal): #verificamos que la fecha ya haya sido agregada previamente
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha):
                for j in range(len(self.fechasAsignadas[i]["ruts"])):
                    print("50 calendario :"+str(self.fechasAsignadas[i]["horasInicio"][j])+"-"+str(horaInicial))
                    print("51 calendario :"+str(self.fechasAsignadas[i]["horasFin"][j])+"-"+str(horaFinal))
                    if(str(self.fechasAsignadas[i]["horasInicio"][j]) == str(horaInicial) and str(self.fechasAsignadas[i]["horasFin"][j]) == str(horaFinal)):
                        print("51 -")
                        return True #existe la cita en la fecha
        
        return False

    def agregarFechas(self, fecha, mycursor, db):
        self.fechasAsignadas.append(fecha) #agregamos la fecha al arreglos
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha["fecha"]):
                print("45 "+str(fecha["fecha"]))
                self.guardarDatosDeCalendarioEnBaseDeDatos(i, mycursor, db)
                break

    def agregarFechasSinGuardadoEnBaseDeDatos(self, fecha, diccionarioDeFecha):
        if(self.verificarFecha(fecha) == False): #si ya existe la fecha no se agrega nuevamente, esto se hace ya que desde la base de datos habran muchas horas asignadas a las fechas, por que para evitar repeticiones debemos verificar
            self.fechasAsignadas.append(diccionarioDeFecha)
    
    def agregarDatosAFecha(self, fecha, rut, telefono, mascota ,horasInicio, minutosInicio, horasFinal, minutosFinal, mycursor, db): #agregamos datos a una fecha ya existente 
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha):
                id  = str(uuid.uuid4())
                self.fechasAsignadas[i]["ruts"].append(rut)
                self.fechasAsignadas[i]["numeros"].append(telefono)
                self.fechasAsignadas[i]["mascota"].append(mascota)
                self.fechasAsignadas[i]["horasInicio"].append(horasInicio)
                self.fechasAsignadas[i]["minutosInicio"].append(minutosInicio)
                self.fechasAsignadas[i]["horasFin"].append(horasFinal)
                self.fechasAsignadas[i]["minutosFin"].append(minutosFinal)
                self.fechasAsignadas[i]["id"].append(id)
                self.guardarDatosDeCalendarioEnBaseDeDatos(i, mycursor, db)
                break
       
    def agregarDatosAFechaSinGuardadoEnBaseDeDatos(self, fecha, rut, telefono, mascota ,horasInicio, minutosInicio, horasFinal, minutosFinal, id): #agregamos datos a una fecha ya existente 
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha):
                self.fechasAsignadas[i]["ruts"].append(rut)
                self.fechasAsignadas[i]["mascota"].append(mascota)
                self.fechasAsignadas[i]["numeros"].append(telefono)
                self.fechasAsignadas[i]["horasInicio"].append(horasInicio)
                self.fechasAsignadas[i]["minutosInicio"].append(minutosInicio)
                self.fechasAsignadas[i]["horasFin"].append(horasFinal)
                self.fechasAsignadas[i]["minutosFin"].append(minutosFinal)
                self.fechasAsignadas[i]["id"].append(id)
                break
    
    #def guardarCalendariosEnBaseDeDatos(self, idVeterinaria, nombreVeterinaria):
     #   sql = 'INSERT INTO calendario (Veterinaria_idVeterinaria, Veterinaria_nombreVeterinaria) VALUES (%s, %s)' 
      #  mycursor.execute(sql, (str(idVeterinaria), str(nombreVeterinaria),)) #cambiar al terminal en el que nos encontramos
       # db.commit()

    def guardarDatosDeCalendarioEnBaseDeDatos(self, idFecha, mycursor, db):

        ulitmo =  len(self.fechasAsignadas[idFecha]["numeros"])-1 #ocupamos ultimo para identificar la ultimo hora, minuot, rut y numero gingresda y que sera guardado en la base de datos
        fecha = self.fechasAsignadas[idFecha]["fecha"].split('/')
        fechaCompletaInicial = str(fecha[2])+"-"+str(fecha[1])+"-"+str(fecha[0])+" "+str(self.fechasAsignadas[idFecha]["horasInicio"][ulitmo])+":"+str(self.fechasAsignadas[idFecha]["minutosInicio"][ulitmo])+":00"
        fechaCompletaFinal = str(fecha[2])+"-"+str(fecha[1])+"-"+str(fecha[0])+" "+str(self.fechasAsignadas[idFecha]["horasFin"][ulitmo])+":"+str(self.fechasAsignadas[idFecha]["minutosFin"][ulitmo])+":00"

        print("82 "+str(str(self.fechasAsignadas[idFecha]["id"][ulitmo])))
        print("83 "+str(str(self.fechasAsignadas[idFecha])))

        sql = 'INSERT INTO fechassolicitadas (idFechasSolicitadas, FechaInicial, FechaFinal, Rut, NumeroDeContacto, nombreMascota, Calendario_idCalendario) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        mycursor.execute(sql, (str(self.fechasAsignadas[idFecha]["id"][ulitmo]), str(fechaCompletaInicial), str(fechaCompletaFinal), str(self.fechasAsignadas[idFecha]["ruts"][ulitmo]), str(self.fechasAsignadas[idFecha]["numeros"][ulitmo]), str(self.fechasAsignadas[idFecha]["mascota"][ulitmo]) ,str(self.idCalendario))) #cambiar al terminal en el que nos encontramos
        db.commit()

    def solicitarDatosCalendarioBaseDeDatos(self, mycursor):

        sql = 'SELECT * FROM fechassolicitadas WHERE Calendario_idCalendario = (%s) AND FechaInicial >= CURDATE() ' #solo tomamos aquellas fechas que sean de el dia actual en adelante
        mycursor.execute(sql, (str(self.idCalendario),))
        DatosCalendario = mycursor.fetchall()
        self.fechasAsignadas = []

        if(DatosCalendario != None):
            self.ProcesarDatosBaseDeDatos(DatosCalendario)

    def ProcesarDatosBaseDeDatos(self, datosCalendario):
        for i in range(len(datosCalendario)):
            #en total son 4 campos de los que sacar datos

            fecha = '%02d' % datosCalendario[i][1].day+'/'+ '%02d' % datosCalendario[i][1].month +'/'+str(datosCalendario[i][1].year) #dado que los datos de la cita son un objeto datetime podemos ocupar sus metodos para sacar lso datos
            horaInicial = str(datosCalendario[i][1].hour)
            minutosInicial = str(datosCalendario[i][1].minute)
            horaFinal = str(datosCalendario[i][2].hour)
            minutosFinal = str(datosCalendario[i][2].minute)
            rut = str(datosCalendario[i][3])
            numero = str(datosCalendario[i][4])
            nombreMascota = str(datosCalendario[i][5])

            diccionarioDeFecha = {'fecha': fecha, 'ruts':[], 'numeros':[], 'mascota':[] ,'horasInicio':[],  'minutosInicio':[], 'horasFin':[], 'minutosFin':[] , 'id': []}

            self.agregarFechasSinGuardadoEnBaseDeDatos(fecha, diccionarioDeFecha)
            
            self.agregarDatosAFechaSinGuardadoEnBaseDeDatos(fecha, rut, numero, nombreMascota ,horaInicial, minutosInicial, horaFinal, minutosFinal ,str(datosCalendario[i][0]))
    
    def editarDatosDeFecha(self, fecha, rut, telefono,mascota, horasInicio, minutosInicio, horasFinal, minutosFinal, cita, mysql, db): #agregamos datos a una fecha ya existente 
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha):

                self.fechasAsignadas[i]["ruts"][cita] = rut
                self.fechasAsignadas[i]["numeros"][cita]= telefono
                self.fechasAsignadas[i]["mascota"][cita]= mascota
                self.fechasAsignadas[i]["horasInicio"][cita] = horasInicio
                self.fechasAsignadas[i]["minutosInicio"][cita] = minutosInicio
                self.fechasAsignadas[i]["horasFin"][cita] = horasFinal
                self.fechasAsignadas[i]["minutosFin"][cita] = minutosFinal
   
                self.editarDatosDeFechaEnBaseDeDatos(i, cita, mysql, db)
                break
    
    def editarDatosDeFechaEnBaseDeDatos(self, idFecha, idicadorDeDatosAAgregar, mycursor, db):

        fecha = self.fechasAsignadas[idFecha]["fecha"].split('/') #dividimos la fecha en componentes
        fechaCompletaInicial = str(fecha[2])+"-"+str(fecha[1])+"-"+str(fecha[0])+" "+str(self.fechasAsignadas[idFecha]["horasInicio"][idicadorDeDatosAAgregar])+":"+str(self.fechasAsignadas[idFecha]["minutosInicio"][idicadorDeDatosAAgregar])+":00"
        fechaCompletaFinal = str(fecha[2])+"-"+str(fecha[1])+"-"+str(fecha[0])+" "+str(self.fechasAsignadas[idFecha]["horasFin"][idicadorDeDatosAAgregar])+":"+str(self.fechasAsignadas[idFecha]["minutosFin"][idicadorDeDatosAAgregar])+":00"

        print("162 calendario : "+str(fechaCompletaInicial))
        print("163 calendario : "+str(fechaCompletaFinal))
    
        sql = 'UPDATE fechassolicitadas SET Rut =%s, NumeroDeContacto = %s, FechaInicial = %s, FechaFinal = %s, nombreMascota = %s WHERE idFechasSolicitadas = %s'
        mycursor.execute(sql, (str(self.fechasAsignadas[idFecha]["ruts"][idicadorDeDatosAAgregar]), str(self.fechasAsignadas[idFecha]["numeros"][idicadorDeDatosAAgregar]), str(fechaCompletaInicial), str(fechaCompletaFinal), str(self.fechasAsignadas[idFecha]["mascota"][idicadorDeDatosAAgregar]) ,str(self.fechasAsignadas[idFecha]["id"][idicadorDeDatosAAgregar]))) #cambiar al terminal en el que nos encontramos
        db.commit()
    
    def eliminarDatosDeFecha(self, fecha, cita, mysql, db): #agregamos datos a una fecha ya existente 
        for i in range(len(self.fechasAsignadas)):
            if (self.fechasAsignadas[i]["fecha"] == fecha):

                self.fechasAsignadas[i]["ruts"].pop(cita)
                self.fechasAsignadas[i]["numeros"].pop(cita)
                self.fechasAsignadas[i]["mascota"].pop(cita)
                self.fechasAsignadas[i]["horasInicio"].pop(cita)
                self.fechasAsignadas[i]["minutosInicio"].pop(cita)
                self.fechasAsignadas[i]["horasFin"].pop(cita)
                self.fechasAsignadas[i]["minutosFin"].pop(cita)
   
                self.eliminarDatosDeFechaBaseDeDatos(i, cita, mysql, db)
                break
    
    def eliminarDatosDeFechaBaseDeDatos(self, idFecha, idicadorDeDatosAAgregar, mycursor, db):

        sql = 'DELETE FROM fechassolicitadas WHERE idFechasSolicitadas = %s'
        mycursor.execute(sql, (str(self.fechasAsignadas[idFecha]["id"][idicadorDeDatosAAgregar]),)) #cambiar al terminal en el que nos encontramos
        db.commit()

    
    def actualizarCitaEnBaseDeDatos(self, idFecha, mycursor, db):
        pass
        
        

    