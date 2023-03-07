import csv
import config



class Vehiculo():
    def __init__(self, numero_de_serie, color, ruedas):
     self.color = color
     self.ruedas = ruedas
     self.numero_de_serie = numero_de_serie
    def __str__(self):
        return "numero de serie: {}, color {}, {} ruedas".format( self.numero_de_serie, self.color, self.ruedas )
    def to_dict(self):
        return {'numero de serie': self.numero_de_serie, 'color': self.color, 'ruedas': self.ruedas}
class Coche(Vehiculo):
    def __init__(self, numero_de_serie,color, velocidad, cilindrada):
     super().__init__(numero_de_serie,color, ruedas = 4)
     self.velocidad = velocidad
     self.cilindrada = cilindrada
    def __str__(self):
     return super().__str__() + ", {} km/h, {} cc".format(self.velocidad, self.cilindrada)
    def to_dict(self):
       return super().to_dict() | {'velocidad': self.velocidad, 'cilindrada': self.cilindrada}

class Camioneta(Coche):
    def __init__(self, numero_de_serie, color, velocidad, cilindrada, carga):
     super().__init__( numero_de_serie, color, velocidad, cilindrada)
     self.carga = carga
    def __str__(self):
     return super().__str__() + ", {} kg de carga".format(self.carga)  
    def to_dict(self):
       return super().to_dict() | {'carga': self.carga}

class Bicicleta(Vehiculo):
    def __init__(self, numero_de_serie, color, tipo):
     super().__init__(numero_de_serie, color, 2)
     if tipo in ("urbana", "deportiva"):
        self.tipo = tipo
     else:
       raise ValueError("El tipo de bicicleta debe ser urbana o deportiva")    
    def __str__(self):
     return super().__str__() + ", {}".format(self.tipo)
    def to_dict(self):
       return super().to_dict() | {'tipo': self.tipo} 
    
class Motocicleta(Vehiculo):
    def __init__(self, numero_de_serie, color, velocidad, cilindrada):
     super().__init__(numero_de_serie, color)
     self.velocidad = velocidad
     self.cilindrada = cilindrada
    def __str__(self):
     return Vehiculo.__str__() + ", {} km/h, {} cc".format(self.velocidad, self.cilindrada)
    def to_dict(self):
       return super().to_dict() | {'velocidad': self.velocidad, 'cilindrada': self.cilindrada}

class Formula1(Coche):
    def __init__(self, numero_de_serie, color, velocidad, cilindrada, equipo):
     super().__init__(numero_de_serie, color, velocidad, cilindrada)
     self.equipo = equipo
    def __str__(self):
     return super().__str__() + ", {}".format(self.equipo)
    def to_dict(self):
       return super().to_dict() | {'equipo': self.equipo}

class Quad(Coche):
    def __init__(self, numero_de_serie, color, velocidad, cilindrada, carga, tipo ):
     super().__init__(numero_de_serie, color ,velocidad, cilindrada)
     self.tipo = tipo
     self.carga = carga
    def __str__(self):
     return super().__str__() + ", {} kg de carga".format(self.carga)
    def to_dict(self):
         return super().to_dict() | {'carga': self.carga}



class Vehiculos:
    lista = []
    with open(config.DATABASE_PATH, newline='\n') as fichero:
        reader = csv.reader(fichero, delimiter=';')

        #si tiene tipo del ultimo, append, si no que pruebe con otra clase

        for fila in reader:
            if fila[8] != '':
                quad = Quad(fila[0], fila[1], fila[3], fila[4], fila[6], fila[7])
                lista.append(quad)
            elif fila[2] == '4':
             if fila[5] != '':
                    formula1 = Formula1(fila[0], fila[1], fila[3], fila[4], fila[5])
                    lista.append(formula1)
             elif fila[6] != '':
                    camioneta = Camioneta(fila[0], fila[1], fila[3], fila[4], fila[6])
                    lista.append(camioneta)
             else:
                    coche = Coche(fila[0], fila[1], fila[3], fila[4]) 
                    lista.append(coche)

            elif fila[2] == '2':
             if fila[3] != '':
                    motocicleta = Motocicleta(fila[0], fila[1], fila[3], fila[4])
                    lista.append(motocicleta)
             elif fila[7] != '':
                    bicicleta = Bicicleta(fila[0], fila[1], fila[7])
                    lista.append(bicicleta)
            else:
                vehiculo = Vehiculo(fila[0], fila[1], fila[2])
                lista.append(vehiculo)

    @staticmethod
    def buscar(numero_de_serie):
        for vehiculo in Vehiculos.lista:
            if vehiculo.numero_de_serie == numero_de_serie:
                return vehiculo


    @staticmethod
    def crear(numero_de_serie, color, ruedas, velocidad, cilindrada, carga, equipo, tipo, modelo):
        if modelo != '':
           quad = Quad(numero_de_serie, color, velocidad, cilindrada, carga, tipo)
           Vehiculos.lista.append(quad)
        elif ruedas == '4':
           if equipo != '':
                formula1 = Formula1(numero_de_serie, color, velocidad, cilindrada, equipo)
                Vehiculos.lista.append(formula1)
           elif carga != '':
                camioneta = Camioneta(numero_de_serie, color, velocidad, cilindrada, carga)
                Vehiculos.lista.append(camioneta)
           else:
                coche = Coche(numero_de_serie, color, velocidad, cilindrada) 
                Vehiculos.lista.append(coche)

        elif ruedas == '2':
           if velocidad != '':
                motocicleta = Motocicleta(numero_de_serie, color, velocidad, cilindrada)
                Vehiculos.lista.append(motocicleta)
           elif tipo != '':
                bicicleta = Bicicleta(numero_de_serie, color, tipo)
                Vehiculos.lista.append(bicicleta)
        else:
            vehiculo = Vehiculo(numero_de_serie, color, ruedas)
            Vehiculos.lista.append(vehiculo) 
        Vehiculos.guardar()
        return vehiculo

    @staticmethod
    def modificar(numero_de_serie, color, ruedas, velocidad, cilindrada, equipo, carga, tipo, modelo):
        for indice, vehiculo in enumerate(Vehiculos.lista):
            if vehiculo.numero_de_serie == numero_de_serie:
                Vehiculos.lista[indice].color = color
                if Vehiculos.lista[indice].__class__.__name__ == 'Vehiculo':
                    Vehiculos.lista[indice].ruedas = ruedas
                if Vehiculos.lista[indice].velocidad != '':
                    Vehiculos.lista[indice].velocidad = velocidad
                if Vehiculos.lista[indice].cilindrada != '':
                    Vehiculos.lista[indice].cilindrada = cilindrada
                if Vehiculos.lista[indice].equipo != '':
                    Vehiculos.lista[indice].equipo = equipo
                if Vehiculos.lista[indice].carga != '':
                    Vehiculos.lista[indice].carga = carga
                if Vehiculos.lista[indice].tipo != '':
                    Vehiculos.lista[indice].tipo = tipo
                if Vehiculos.lista[indice].modelo != '':
                    Vehiculos.lista[indice].modelo = modelo
                Vehiculos.guardar()
                return Vehiculos.lista[indice]

    @staticmethod
    def borrar(numero_de_serie):
        for indice, vehiculo in enumerate(Vehiculos.lista):
            if vehiculo.numero_de_serie == numero_de_serie:
                vehiculo = Vehiculos.lista.pop(indice)
                Vehiculos.guardar()
                return vehiculo

    @staticmethod
    def guardar():
        with open(config.DATABASE_PATH, 'w', newline='\n') as fichero:
            writer = csv.writer(fichero, delimiter=';')
            for vehiculo in Vehiculos.lista:
                writer.writerow([vehiculo.numero_de_serie, vehiculo.color, vehiculo.ruedas, vehiculo.velocidad if hasattr(vehiculo, "velocidad") else "" , vehiculo.cilindrada if hasattr(vehiculo, "cilindrada") else "", vehiculo.equipo if hasattr(vehiculo, "equipo") else "", vehiculo.carga if hasattr(vehiculo, "carga") else "", vehiculo.tipo if hasattr(vehiculo, "tipo") else "", vehiculo.modelo if hasattr(vehiculo, "modelo") else ""])


