from datetime import datetime
from babel.dates import get_day_names
class Tarea:
    def __init__(self,id,creacion,estado,tipo,nombre, prioridad,hora):
        self.id = id
        self.creacion = creacion
        self.nombre = nombre
        self.estado = estado
        self.hora = hora
        self.prioridad = prioridad
        self.tipo = tipo

    def __str__(self):
        return f"| {self.nombre.title()} | {self.prioridad.title()} | {self.estado.title()} | {self.hora} |"
    
    def info_completa(self):
        return (
            f"📅 Creada: {self.creacion}\n"
            f"📝 ID: {self.id}\n"
            f"📝 Nombre: {self.nombre}\n"
            f"🏷️ Tipo: {self.tipo}\n"
            f"🔥 Prioridad: {self.prioridad}\n"
            f"📊 Estado: {self.estado}\n"
            f"⏰ Hora: {self.hora}"
        )

    def _calcular_puntaje(self):
        if self.prioridad == "Alta":
            puntaje = 15
        elif self.prioridad == "Media":
            puntaje = 10
        else:
            puntaje = 5
        return puntaje


    def completar(self):
        if self.estado == "Completada":
            return False, 0
        
        self.estado = "Completada"
        puntaje = self._calcular_puntaje()
        
        return True, puntaje
    
    def disponible_hoy(self):
        return None
    
    def pendiente_hoy(self):
        if self.estado == "Pendiente":
            return True

    def mensaje_extra(self):
        return None

class TareaRutina(Tarea):
    def __init__(self,id,creacion,estado,tipo,racha,nombre, prioridad,hora,dias):
        super().__init__(id,creacion,estado,tipo,nombre, prioridad,hora)
        self.racha = racha
        self.dias = dias

    def __str__(self):
        fecha_m = datetime.now().strftime("%d/%m/%Y")
        hoy = datetime.now()
        nombres_dias = get_day_names('wide', locale='es')
        dia_hoy = nombres_dias[hoy.weekday()].lower()
        
        if self.estado == f"Habito completado el {fecha_m}":
            estado = "Completada hoy"
            return f"| {self.nombre.title()} | {self.prioridad.title()} | {estado} | {self.hora} |"
        elif self.estado == "Pendiente" or "Fallida" in self.estado:
            estado = self.estado
            return f"| {self.nombre.title()} | {self.prioridad.title()} | {estado} | {self.hora} |"
        else:
            estado = "Libre por hoy"

        for dia in self.dias:
            if dia == dia_hoy:
                mensaje = f"Pendiente Hoy {dia_hoy}"
                estado = mensaje

        return f"| {self.nombre.title()} | {self.prioridad.title()} | {estado} | {self.hora} |"

    def info_completa(self):
        texto_base = super().info_completa()
        dias_str = ", ".join(self.dias)
        return texto_base + f"\n🔥 Racha: {self.racha}\n🗓️ Días: {dias_str}"

    def completar(self):
        fecha_m = datetime.now().strftime("%d/%m/%Y")
        if self.estado == f"Habito completado el {fecha_m}":
            return False, 0
        
        self.estado = f"Habito completado el {fecha_m}"
        self.racha += 1
        puntaje = self._calcular_puntaje()

        return True, puntaje
    
    def fallar(self):
        fecha_m = datetime.now().strftime("%d/%m/%Y")
        if self.estado == "Pendiente" or "Fallida" in self.estado:
            return False
        
        self.estado = f"Fallida {fecha_m}"
        self.racha = 0
        return True
    
    def disponible_hoy(self):
        ahora = datetime.now()
        dia_hoy = ahora.strftime('%A')

        for dia in self.dias:
            if dia == dia_hoy:
                return True
            
    def pendiente_hoy(self):
        fecha_m = datetime.now().strftime("%d/%m/%Y")
        if self.estado != f"Habito completado el {fecha_m}" and self.disponible_hoy():
            return True

    def mensaje_extra(self):
        mensaje = None
        if self.racha == 3:
             mensaje = f"¡Felicidades por tu racha de 3 dias en el habtito de *{self.nombre}* ¡SIgue asi! 🔥"
        elif self.racha == 7:
            mensaje = f"¡Felicidades por tu racha de una semana! en el habtito de *{self.nombre}* ¡SIgue asi! 🔥"
        elif self.racha == 30:
             mensaje = f"¡Felicidades por tu racha de un mes! en el habtito de *{self.nombre}* ¡SIgue asi! 🔥"

        return mensaje