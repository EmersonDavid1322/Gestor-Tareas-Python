from datetime import datetime
import tkinter.messagebox as messagebox
from src.clases import TareaRutina,Tarea
from src.storage import guardar_datos,cargar_datos
from src.base_sql import guardar_tareas, cargar_tareas,estado_tarea,eliminar_tarea_sql
from src.resultados import ResultadoOperacion ,ResultadoCompletar
print("Versión 1.3 servicios")

def validar_tarea_id(id,tipo,tareas,tareas_rutina):
    for t in tareas + tareas_rutina:
        if tipo == t.tipo:
            if t.id == id:
                return t

def validar_tarea_nombre(nombre,tareas,tareas_rutina):
    for t in tareas + tareas_rutina:
        if t.nombre == nombre:
            return t

def tarea_existe(nombre):
    tareas, tareas_rutina = cargar_tareas()
    return validar_tarea_nombre(nombre, tareas, tareas_rutina) is not None

def agregar_tarea(tipo,nombre,prioridad,tiempo,dias): 
    id_tarea = 0

    fecha = datetime.now().strftime("%d/%m/%Y")
    estado = "Pendiente"

    if tipo == "Tarea":
        tipo_t  = "Unica"
        tarea_datos = Tarea(id=id_tarea,
                            creacion=fecha,
                            estado=estado,
                            tipo=tipo_t,
                            nombre=nombre,
                            prioridad=prioridad,
                            hora=tiempo)
    else:
        tipo_t = "Rutina"
        racha = 0
        tarea_datos = TareaRutina(
                            id=id_tarea,
                            creacion=fecha,
                            estado=estado,
                            tipo=tipo,
                            racha=racha,
                            nombre=nombre,
                            prioridad=prioridad,
                            hora=tiempo,
                            dias=dias
                            )

    if tarea_datos.tipo == "Rutina":
        guardar_tareas(tarea_datos.tipo,tarea_datos)
        return ResultadoOperacion(exito=True, mensaje=f"Tarea rutina agregada {tarea_datos.nombre} correctamente")
    else:
        guardar_tareas(tarea_datos.tipo,tarea_datos)
        return ResultadoOperacion(exito=True, mensaje=f"Tarea agregada {tarea_datos.nombre} correctamente")

def completar(id,tipo):
    puntos_v, webhook, lista_frases, usar_frase, token, canal = cargar_datos()
    tareas, tareas_rutina = cargar_tareas()

    marcar_tarea = validar_tarea_id(id,tipo,tareas,tareas_rutina)
    if marcar_tarea is None:
        return ResultadoCompletar(exito=False, mensaje="No se encontro la tarea", puntaje=0)

    completado, puntaje_tarea = marcar_tarea.completar()
    
    if completado:
        puntos_v += puntaje_tarea

        estado_tarea(marcar_tarea)
        resultado = ResultadoCompletar(exito=True, mensaje="¡Felicidades! Has completado una tarea, sigue asi",
                                        puntaje=puntaje_tarea, mensaje_racha=marcar_tarea.mensaje_extra())
        guardar_datos(puntos_v,webhook,lista_frases,usar_frase,token,canal)
        return resultado
    else:
        return ResultadoCompletar(exito=False, mensaje="Tarea ya marcada", puntaje=0)

def fallar_tarea(id,tipo):
    tareas, tareas_rutina = cargar_tareas()

    tarea_f = validar_tarea_id(id,tipo,tareas,tareas_rutina)
    if tarea_f is None:
        return ResultadoOperacion(exito=False, mensaje="Tarea no encontrada")

    fallar = tarea_f.fallar()

    if fallar:
        estado_tarea(tarea_f)
        return ResultadoOperacion(exito=True,mensaje="Lo importante no es cuantas veces caes, sino la fuerza que te hace volver a levantarte")
    else:
        return ResultadoOperacion(exito=False,mensaje="Esta tarea no se a completado o ya ha sido marcada como fallida")

def eliminar_tarea(id_tarea,tipo):
    tareas, tareas_rutina = cargar_tareas()

    tarea_eliminar = validar_tarea_id(id_tarea,tipo,tareas,tareas_rutina)
    if tarea_eliminar is None:
        return ResultadoOperacion(exito=False,mensaje="Tarea no encontrada")

    eliminar_tarea_sql(tarea_eliminar)
    return ResultadoOperacion(exito=True,mensaje="Tarea eliminada correctamente")

def filtro_todas():
    tareas, habitos = cargar_tareas()
    return tareas, habitos

def filtro_hoy():
    tareas, habitos = cargar_tareas()

    filtro = []
    for tarea in habitos:
        if tarea.disponible_hoy():
            filtro.append(tarea)

    return None, filtro

def filtro_pendientes_hoy():
    tareas, habitos = cargar_tareas()
    
    tareas_pendientes, habitos_pendientes = [], []

    for tarea in tareas:
        if tarea.pendiente_hoy():
            tareas_pendientes.append(tarea)

    for habito in habitos:
        if habito.pendiente_hoy():
            habitos_pendientes.append(habito)

    return tareas_pendientes, habitos_pendientes