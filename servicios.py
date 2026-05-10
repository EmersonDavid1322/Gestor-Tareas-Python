from datetime import datetime
import tkinter.messagebox as messagebox
from clases import TareaRutina,Tarea
from storage import guardar_datos,cargar_datos

print("Versión 1.2 servicios")

def validar_tarea_id(id,tareas,tareas_rutina):
    for t in tareas + tareas_rutina:
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

def agregar_tarea(nombre,tipo,prioridad,tiempo,dias): 
        tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
        
        id_tarea = generar_id(tareas,tareas_rutina)

        if tipo == "Tarea":
            tarea_datos = Tarea(id_tarea,nombre,prioridad,tiempo)
        else:
            tarea_datos = TareaRutina(id_tarea,nombre,prioridad,tiempo,dias)

        tarea_añadir = validar_tarea_nombre(tarea_datos.nombre,tareas,tareas_rutina)

        if tarea_añadir is None:
            if tarea_datos.tipo == "Rutina":
                tareas_rutina.append(tarea_datos)
                historial.append("Se añadió la tarea rutinaria: " + tarea_datos.nombre)
                guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
                messagebox.showinfo("Añadir Tareas",f"Tarea rutina agregada {tarea_datos.nombre} correctamente")
                return
            else:
                tareas.append(tarea_datos)
                historial.append("Se añadió la tarea unica: " + tarea_datos.nombre)
                guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
                messagebox.showinfo("Añadir Tareas",f"Tarea agregada {tarea_datos.nombre} correctamente")
                return
        else:
            if tarea_datos.tipo == "Rutina":
                respuesta = messagebox.askyesno("Tarea Duplicada", f"La tarea '{nombre}' ya existe. ¿Deseas duplicarla?")
                tareas_rutina.append(tarea_datos)
                historial.append("Se añadió tarea rutina duplicada: " + tarea_datos.nombre)
                guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
                messagebox.showinfo("Añadir Tareas",f"Tarea agregada {tarea_datos.nombre} correctamente")
                return
            else:
                respuesta = messagebox.askyesno("Tarea Duplicada", f"La tarea '{nombre}' ya existe. ¿Deseas duplicarla?")
                if respuesta:
                    tareas.append(tarea_datos)
                    historial.append("Se añadió tarea duplicada: " + tarea_datos.nombre)
                    guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
                    messagebox.showinfo("Añadir Tareas",f"Tarea agregada {tarea_datos.nombre} correctamente")
                    return
                else:
                    return
                
def completar(id):
        tareas, historial, puntos_v, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
        marcar_tarea = validar_tarea_id(id,tareas,tareas_rutina)

        if marcar_tarea.tipo == "Unica":
            if marcar_tarea.estado == "Completada":
                messagebox.showwarning("Completar",f"La tarea {marcar_tarea.nombre} ya a sido marcada")
            else:
                marcar_tarea.estado = "Completada"
                messagebox.showinfo("Completar","¡Felicidades! Has completado la tarea, sigue asi")
                historial.append("Tarea completada: " + marcar_tarea.nombre)
                if marcar_tarea.prioridad == "Alta":
                    puntaje = 15
                    puntos_v += puntaje
                elif marcar_tarea.prioridad == "Media":
                    puntaje = 10
                    puntos_v += puntaje
                else:
                    puntaje = 5
                    puntos_v += puntaje
                messagebox.showinfo("Completar",f"¡Felicidades! Tu puntaje de diciplina subio a: {puntaje} sigue asi")
                guardar_datos(tareas, historial, puntos_v,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
        else:
            fecha_m = datetime.now().strftime("%d/%m/%Y")

            if f"Habito completado el {str(fecha_m)}" in marcar_tarea.estado: #Usamor estado completo porque corroboramos fecha tambien al fallar
                messagebox.showwarning("Completar","Tarea ya marcada por hoy")

            else:

                marcar_tarea.estado = f"Habito completado el {fecha_m}"
                marcar_tarea.racha += 1
                if marcar_tarea.prioridad == "Alta":
                    puntaje = 15
                    puntos_v += puntaje
                elif marcar_tarea.prioridad == "Media":
                    puntaje = 10
                    puntos_v += puntaje
                else:
                    puntaje = 5
                    puntos_v += puntaje
                messagebox.showinfo("Completar","¡Felicidades! Has completado tu habito, sigue asi")
                messagebox.showinfo("Completar",f"¡Felicidades! Tu puntaje de diciplina subio a: {puntaje} sigue asi")
                felicitar_racha(marcar_tarea,marcar_tarea.racha)
                registro_cumplidos.append({
                    "Nombre": marcar_tarea.nombre,
                    "Estado": marcar_tarea.estado,
                    "Prioridad": marcar_tarea.prioridad,
                    "Racha": marcar_tarea.racha
                })
                historial.append(
                    f"Habito de {marcar_tarea.nombre} completo racha de {marcar_tarea.racha}"
                )
                guardar_datos(tareas, historial, puntos_v,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)

def fallar_tarea(id):
    fecha_m = datetime.now().strftime("%d/%m/%Y")
    tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()

    tarea_f = validar_tarea_id(id, tareas,tareas_rutina)

    if tarea_f.estado == "Pendiente" or "Fallida" in tarea_f.estado:
        messagebox.showerror("Fallar","Esta tarea no se a completado o ya ha sido marcada como fallida")
        return
    
    tarea_f.racha = 0
    tarea_f.estado = f"Fallida {fecha_m}"
    messagebox.showinfo("Fallar","Lo importante no es cuantas veces caes, sino la fuerza que te hace volver a levantarte")
    historial.append(f"Se a fallado la tarea '{tarea_f.nombre}' el '{fecha_m}'")
    registro_cumplidos.append({
                    "Nombre": tarea_f.nombre,
                    "Estado": tarea_f.estado,
                    "Prioridad": tarea_f.prioridad,
                    "Racha": tarea_f.racha
                })
    guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
    return

def eliminar_tarea(id_tarea,idx,r,msg):
        tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()

        tarea_eliminar = validar_tarea_id(id_tarea,tareas,tareas_rutina)

        if msg:
            confirmacion = messagebox.askyesno("Elimnar","¿Desea eliminar esta tarea?")
        else:
            confirmacion = True
        
        if confirmacion:
            if r:
                print(r)
                tareas_rutina.pop(idx)
                historial.append(f"Se eliminio el habito '{tarea_eliminar.nombre}'")
            else:
                print(r)
                tareas.pop(idx)
                historial.append(f"Se eliminio la tarea '{tarea_eliminar.nombre}'")
        
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)

def mostrar_info_tarea(id, r):
        tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
        t = validar_tarea_id(id,tareas,tareas_rutina)

        texto_info = (
            f"📅 Creada: {t.fecha_creacion}\n"
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