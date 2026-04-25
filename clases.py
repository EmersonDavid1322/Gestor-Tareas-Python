class Tarea:
    def __init__(self, nombre, prioridad):
        self.nombre = nombre
        self.estado = "Pendiente"
        self.hora = None
        self.prioridad = prioridad
        self.tipo = "Unica"
    
    def mostrar_informacion(self):
        print(f"Nombre: {self.nombre} Estado: {self.estado} Hora: {self.hora} Prioridad: {self.prioridad}")

    def a_diccionario(self):
        return {
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
    
    def a_diccionario(self):
        dicc = super().a_diccionario()
        dicc["racha"] = self.racha
        return dicc