from datetime import datetime
class Tarea:
    def __init__(self, nombre, prioridad):
        self.fecha_creacion = datetime.now().strftime("%d/%m/%Y")
        self.nombre = nombre
        self.estado = "Pendiente"
        self.hora = None
        self.prioridad = prioridad
        self.tipo = "Unica"
    
    def mostrar_informacion(self):
        print(f"|Fecha Creación: {self.fecha_creacion} | Nombre: {self.nombre} | Estado: {self.estado} | Hora: {self.hora} | Prioridad: {self.prioridad} |\n")

    def a_diccionario(self):
        return {
            "creacion": self.fecha_creacion,
            "nombre": self.nombre,
            "estado": self.estado,
            "hora": self.hora,
            "prioridad": self.prioridad,
            "tipo": self.tipo
        }
class TareaRutina(Tarea):
    def __init__(self, nombre, prioridad):
        super().__init__(nombre, prioridad)
        self.tipo = "Rutina"
        self.racha = 0
        self.dias = ["lunes","martes","miércoles","jueves","viernes","sabado","domingo"]
    
    def mostrar_informacion(self):
        print(f"| Fecha Creación: {self.fecha_creacion} | Nombre: {self.nombre} | Estado: {self.estado} | Hora: {self.hora} | Prioridad: {self.prioridad} | Racha: {self.racha} | \n | Dias tarea: {self.dias} |\n")

    
    def a_diccionario(self):
        dicc = super().a_diccionario()
        dicc["racha"] = self.racha
        dicc["dias"] = self.dias
        return dicc
