from datetime import datetime
class Tarea:
    def __init__(self, nombre, prioridad,hora):
        self.fecha_creacion = datetime.now().strftime("%d/%m/%Y")
        self.nombre = nombre
        self.estado = "Pendiente"
        self.hora = hora
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
    def __init__(self, nombre, prioridad,hora,dias):
        super().__init__(nombre, prioridad,hora)
        self.tipo = "Rutina"
        self.racha = 0
        self.dias = dias
    
    def mostrar_informacion(self):
        print(f"| Fecha Creación: {self.fecha_creacion} | Nombre: {self.nombre} | Estado: {self.estado} | Hora: {self.hora} | Prioridad: {self.prioridad} | Racha: {self.racha} | \n | Dias tarea: {self.dias} |\n")

    
    def a_diccionario(self):
        dicc = super().a_diccionario()
        dicc["racha"] = self.racha
        dicc["dias"] = self.dias
        return dicc
