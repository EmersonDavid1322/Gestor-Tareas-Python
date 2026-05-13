from datetime import datetime

class Tarea:
    def __init__(self,id,creacion,estado,tipo,nombre, prioridad,hora):
        self.id = id
        self.creacion = creacion
        self.nombre = nombre
        self.estado = estado
        self.hora = hora
        self.prioridad = prioridad
        self.tipo = tipo
    
    def mostrar_informacion(self):
        print(f"|Fecha Creación: {self.fecha_creacion} | Nombre: {self.nombre} | Estado: {self.estado} | Hora: {self.hora} | Prioridad: {self.prioridad} |\n")

    def a_diccionario(self):
        return {
            "id": self.id,
            "creacion": self.fecha_creacion,
            "nombre": self.nombre,
            "estado": self.estado,
            "hora": self.hora,
            "prioridad": self.prioridad,
            "tipo": self.tipo
        }
class TareaRutina(Tarea):
    def __init__(self,id,creacion,estado,tipo,racha,nombre, prioridad,hora,dias):
        super().__init__(id,creacion,estado,tipo,nombre, prioridad,hora)
        self.racha = racha
        self.dias = dias
    
    def mostrar_informacion(self):
        print(f"| Fecha Creación: {self.fecha_creacion} | Nombre: {self.nombre} | Estado: {self.estado} | Hora: {self.hora} | Prioridad: {self.prioridad} | Racha: {self.racha} | \n | Dias tarea: {self.dias} |\n")

    
    def a_diccionario(self):
        dicc = super().a_diccionario()
        dicc["racha"] = self.racha
        dicc["dias"] = self.dias
        return dicc
