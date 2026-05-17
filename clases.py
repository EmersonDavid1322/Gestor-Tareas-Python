class Tarea:
    def __init__(self,id,creacion,estado,tipo,nombre, prioridad,hora):
        self.id = id
        self.creacion = creacion
        self.nombre = nombre
        self.estado = estado
        self.hora = hora
        self.prioridad = prioridad
        self.tipo = tipo

class TareaRutina(Tarea):
    def __init__(self,id,creacion,estado,tipo,racha,nombre, prioridad,hora,dias):
        super().__init__(id,creacion,estado,tipo,nombre, prioridad,hora)
        self.racha = racha
        self.dias = dias