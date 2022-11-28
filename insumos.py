class insumoVeterinario:

    def __init__(self, *args): #debido al funcionamiento de python
        #solo manejaremos un constructor que sera ocupado para principalmente el manejo en base de datos, pero tambien para el ingresao normal 
        if(len(args) == 0):
            self.idInsumo = None
            self.PrecioInsumo = None
            self.nombreDeInsumo = None
        elif(len(args) == 1):
            self.idInsumo = args[0]
            self.PrecioInsumo = None
            self.nombreDeInsumo = None
        elif(len(args) == 3):
            self.idInsumo = args[0]
            self.PrecioInsumo = args[1]
            self.nombreDeInsumo = args[2]
    
    def getId(self):
        return self.idInsumo
    
    def getPrecioInsumo(self):
        return self.PrecioInsumo
    
    def getNombreDeInsumo(self):
        return self.nombreDeInsumo
    
    def setId(self, id):
        self.idInsumo = id
    
    def setPrecioInsumo(self, precio):
        self.PrecioInsumo = precio
    
    def setNombreDeInsumo(self, nombreDeInsumo):
        self.nombreDeInsumo = nombreDeInsumo
    
    def guardarInsumoEnBaseDeDatos(self, dB, myCursor, idVeterinaria, nombreVeterinaria):
        sql = 'INSERT INTO Insumos (idInsumos, nombre, valor, Veterinaria_idVeterinaria, Veterinaria_nombreVeterinaria) VALUES (%s, %s, %s, %s, %s)' 
        myCursor.execute(sql, (str(self.idInsumo), str(self.nombreDeInsumo), str(self.PrecioInsumo), str(idVeterinaria), str(nombreVeterinaria)))
        dB.commit()

    def editarInsumoBaseDeDatos(self, dB, myCursor):
        sql = 'UPDATE Insumos SET valor = %s, nombre = %s WHERE idInsumos = %s' 
        myCursor.execute(sql, (str(self.PrecioInsumo), str(self.nombreDeInsumo), str(self.idInsumo)))
        dB.commit()
    
    def eliminarInsumoBaseDeDatos(self, dB, myCursor):
        sql = 'DELETE FROM Insumos WHERE idInsumos = %s'
        myCursor.execute(sql, (str(self.idInsumo),))
        dB.commit()
    
    def obtenerDatosBaseDeDatos(self, dB, mycursor):
        dB.commit()
        sql = 'SELECT valor, nombre FROM Insumos WHERE idInsumos = %s' 
        mycursor.execute(sql, (str(self.idInsumo),))
        datos = mycursor.fetchall()

        self.setNombreDeInsumo(datos[0][1])
        self.setPrecioInsumo(datos[0][0])