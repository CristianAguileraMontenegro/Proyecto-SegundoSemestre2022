import mysql.connector

class sqlClass:

    def __init__(self):
        self.db = mysql.connector.connect( user='root', password='root', host='localhost', database='mydb', port='3306')
        self.mycursor = self.db.cursor()

    def query(self,sql):
        self.mycursor.execute(sql)
        return self.cursor.fetchone()
    
    def queryVariable(self, sql, id, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, tablaMedica, fechaNacimiento):
        self.mycursor.execute(sql, (id, str(nombre), str(especie), str(color), str(raza), str(nombreTutor), str(rutTutor), str(numeroTelefono), str(direccion), str(tablaMedica), str(fechaNacimiento)))
        self.db.commit()

    def queryReturn(self, sql, variable):
  
        self.mycursor.execute(sql, (str(variable),))
        resultadoMascota = self.mycursor.fetchone()
        return resultadoMascota
        
    
    def queryFetchAll(self,sql, variable):
        self.mycursor.execute(sql, (str(variable),))
        resultadoMascota = self.mycursor.fetchall()
        return resultadoMascota

    def rows(self):
        return self.cursor.rowcount