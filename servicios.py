from datetime import datetime
import tkinter.messagebox as messagebox
from clases import TareaRutina,Tarea
from storage import guardar_datos,cargar_datos
from base_sql import guardar_tareas, cargar_tareas,estado_tarea,eliminar_tarea_sql

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

def generar_id(tareas, tareas_rutina):
    todos = tareas + tareas_rutina
    if not todos:
        return 1
    return max(t.id for t in todos) + 1

def agregar_tarea(tipo,nombre,prioridad,tiempo,dias): 
        tareas, tareas_rutina = cargar_tareas()
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

        tarea_añadir = validar_tarea_nombre(tarea_datos.nombre,tareas,tareas_rutina)

        if tarea_añadir is None:
            if tarea_datos.tipo == "Rutina":
                tareas_rutina.append(tarea_datos)
                guardar_tareas(tarea_datos.tipo,tarea_datos)
                messagebox.showinfo("Añadir Tareas",f"Tarea rutina agregada {tarea_datos.nombre} correctamente")
                return
            else:
                tareas.append(tarea_datos)
                guardar_tareas(tarea_datos.tipo,tarea_datos)
                messagebox.showinfo("Añadir Tareas",f"Tarea agregada {tarea_datos.nombre} correctamente")
                return
        else:
            if tarea_datos.tipo == "Rutina":
                respuesta = messagebox.askyesno("Tarea Duplicada", f"La tarea '{nombre}' ya existe. ¿Deseas duplicarla?")
                if respuesta:
                    tareas_rutina.append(tarea_datos)
                    guardar_tareas(tarea_datos.tipo,tarea_datos)
                    messagebox.showinfo("Añadir Tareas",f"Tarea agregada {tarea_datos.nombre} correctamente")
                return
            else:
                respuesta = messagebox.askyesno("Tarea Duplicada", f"La tarea '{nombre}' ya existe. ¿Deseas duplicarla?")
                if respuesta:
                    tareas.append(tarea_datos)
                    guardar_tareas(tarea_datos.tipo,tarea_datos)
                    messagebox.showinfo("Añadir Tareas",f"Tarea agregada {tarea_datos.nombre} correctamente")
                return

def completar(id,tipo):
        puntos_v, webhook, lista_frases, usar_frase, token, canal = cargar_datos()
        tareas, tareas_rutina = cargar_tareas()

        marcar_tarea = validar_tarea_id(id,tipo,tareas,tareas_rutina)

        completado, puntaje = marcar_tarea.completar()
        
        if completado:
            puntos_v += puntaje

            estado_tarea(marcar_tarea)
            messagebox.showinfo("Completar","¡Felicidades! Has completado una tarea, sigue asi")
            messagebox.showinfo("Completar",f"¡Felicidades! Tu puntaje de diciplina subio con: {puntaje} sigue asi")
            
            mensaje = marcar_tarea.mensaje_extra()
            if mensaje is not None:
                messagebox.showinfo("Racha", mensaje)

            guardar_datos(puntos_v,webhook,lista_frases,usar_frase,token,canal)
        else:
            messagebox.showwarning("Completar","Tarea ya marcada")

def fallar_tarea(id,tipo):
    fecha_m = datetime.now().strftime("%d/%m/%Y")
    tareas, tareas_rutina = cargar_tareas()

    tarea_f = validar_tarea_id(id,tipo,tareas,tareas_rutina)

    fallar = tarea_f.fallar()

    if fallar:
        estado_tarea(tarea_f)
        messagebox.showinfo("Fallar","Lo importante no es cuantas veces caes, sino la fuerza que te hace volver a levantarte")
    else:
        messagebox.showerror("Fallar","Esta tarea no se a completado o ya ha sido marcada como fallida")


def eliminar_tarea(id_tarea,r,msg,tipo):
        tareas, tareas_rutina = cargar_tareas()

        tarea_eliminar = validar_tarea_id(id_tarea,tipo,tareas,tareas_rutina)

        if msg:
            confirmacion = messagebox.askyesno("Elimnar","¿Desea eliminar esta tarea?")
        else:
            confirmacion = True
        
        if confirmacion:
            if r:
                eliminar_tarea_sql(tarea_eliminar)
            else:
                eliminar_tarea_sql(tarea_eliminar)

def mostrar_info_tarea(id, r,tipo):
        tareas, tareas_rutina = cargar_tareas()
        t = validar_tarea_id(id,tipo,tareas,tareas_rutina)

        texto_info = (
            f"📅 Creada: {t.creacion}\n"
            f"📝 ID: {t.id}"
            f"📝 Nombre: {t.nombre}\n"
            f"🏷️ Tipo: {t.tipo}\n"
            f"🔥 Prioridad: {t.prioridad}\n"
            f"📊 Estado: {t.estado}\n"
            f"⏰ Hora: {t.hora}"
        )
        
        if r:
            texto_info += f"\n🔥 Racha: {t.racha}"
            dias_str = ", ".join(t.dias)
            texto_info += f"\n🗓️ Días: {dias_str}"

        messagebox.showinfo(f"Detalles de {t.nombre}", texto_info)

def felicitar_racha(tarea,racha):
    if racha == 3:
        messagebox.showinfo("Felicidades",f"Felicidades por tu racha de 3 dias en el habtito de *{tarea.nombre}*, ¡SIgue asi! 🔥")
    elif racha == 7:
        messagebox.showinfo("Felicidades",f"¡Felicidades por tu racha de una semana! en el habtito de *{tarea.nombre}*, ¡SIgue asi! 🔥")
    elif racha == 30:
        messagebox.showinfo("Felicidades",f"¡Felicidades por tu racha de un mes! en el habtito de *{tarea.nombre}*, ¡SIgue asi! 🔥")