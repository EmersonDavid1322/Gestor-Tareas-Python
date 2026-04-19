from storage import guardar_datos
from datetime import datetime


def menu_f():
    print("\t Gestor de tareas\t ")
    print("1) Agregar tarea \t         2) Ver tareas")
    print("3) Buscar tarea \t         4) Editar tarea")
    print("5) Marcas tarea completa \t 6) Ver tareas pendientes")
    print("7) Ver tareas completas \t 8) Historial")
    print("9) Elimar tarea  \t         10) Estadisticas")
    print("11) Introducir  o editar WEBHOOK_URL \t 12) salir ")
    while True:
        try:
            opcion = int(input("Introduzca una opción deseada: "))
            return opcion
        except ValueError:
            print("Caracter no valido")



def validar_tarea(nombre,tareas,tareas_rutina):
    for t in tareas + tareas_rutina:
        if t["Nombre"] == nombre:
            return t


def agregar_tarea(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook):
    print("Ha seleccionado agregar tarea")
    tarea_datos = datos_tarea()
    tarea_añadir = validar_tarea(tarea_datos["Nombre"],tareas,tareas_rutina)

    if tarea_añadir is None:
        if tarea_datos["Tipo"] == "Rutina":
            tareas_rutina.append(tarea_datos)
            historial.append("Se añadió la tarea rutinaria: " + str(tarea_datos))
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook)
            print("Tarea agregada correctamente")
            return
        else:
            tareas.append(tarea_datos)
            historial.append("Se añadió la tarea unica: " + str(tarea_datos))
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook)
            print("Tarea agregada correctamente")
            return
    else:
        if tarea_añadir["Tipo"] == "Rutina":
            print(f"La tarea '{tarea_añadir["Nombre"]}' ya ha sido añadida anteriormente, las tareas tipo rutina no se pueden duplicar")
            return
        else:
            duplicada = input("Esta tarea ya existe, ¿desea duplicarla? (S/N): ").lower()
            if duplicada in ("s", "si"):
                tareas.append(tarea_datos)
                historial.append("Se añadió tarea duplicada: " + str(tarea_datos))
                guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook)
                print("Tarea duplicada añadida")
                return
            else:
                print("No se añadió la tarea")
                return
            

def datos_tarea():
    nombre = input("Ingrese el nombre de la tarea: ").title()
    tarea = {"Nombre": nombre, "Estado": "Pendiente"}
    while True:
        try:
            tipo_tarea = int(input(" 1)Unica \n 2)Rutina \n Tipo de tarea: "))
            if tipo_tarea == 1:
                tarea["Tipo"] = "Unica"
            elif tipo_tarea == 2:
                tarea["Tipo"] = "Rutina"
                tarea["Racha"] = 0
            else:
                print("Introduzca un digito valido")
                continue
            break
        except ValueError:
            print("Valor no valido")
    while True:
        confimacion = input("¿Desea añadir una hora a la tarea? (S/N) ").lower()
        if confimacion in ("s","si"):
            hora = input('Introduzca la hora en formato "HH:MM": ')
            if  len(hora) == 5 and hora[2] == ":": 
                partes = hora.split(":")
                if partes[0].isdigit() and partes[1].isdigit():
                    tarea["Hora"] = hora
                    break
                else:
                    print('Hora incorrecta, por favor ingrese en formato "HH:MM" ')
            else:
                print('Hora incorrecta, por favor ingrese en formato "HH:MM" ')
        else:
            tarea["Hora"] = None
            break
    while True:
        prioridad = input('Ingrese la prioridad de la tarea (Alta/Media/Baja): ').title()
        if prioridad == "Alta":
            tarea["Prioridad"] = "Alta"
            break
        elif prioridad == "Media":
            tarea["Prioridad"] = "Media"
            break
        elif prioridad == "Baja":
            tarea["Prioridad"] = "Baja"
            break
        else:
            print("Opción no valida")
    return tarea

def ver_tareas_registros(tareas,tareas_rutina,registro_cumplidos):
    while True:
        try:
            confirmacion = int(input("1) ver tareas y habitos activos \n2) Ver registro de habitos \n seleccione una opción: "))
            break
        except ValueError:
            print("Seleccione una opción valida")
    if confirmacion == 1:
        print("Ha seleccionado ver tareas y habitos activos:")
        if len(tareas) == 0:
            print("No hay tareas unicas")
        else:
            print("\tTareas completos\t")
            for prioridad in ["Alta", "Media", "Baja"]:
                for t in tareas:
                    if t["Prioridad"] == prioridad:
                        print(f"Nombre: {t ['Nombre']} | Tipo: {t ['Tipo']} | Estado: {t ['Estado']}| Prioridad: {t['Prioridad']} | Hora: {t["Hora"]}")
        if len(tareas_rutina) == 0:
            print("No hay tareas rutinarias")
        else:
            print("\tHabitos activos\t")
        for t_r in tareas_rutina:
            print(t_r)
    else:   
        print("Ha seleccionado ver registro de habitos cumplidos")
        if len(registro_cumplidos) == 0:
            print("NO hay registro de habitos cumplidos")
        else:
            for registro in registro_cumplidos:
                print(registro)

def buscar_tarea(tareas, historial,puntos,tareas_rutina,registro_cumplidos,webhook):
    print("Ha seleccionado Buscar tarea")
    nombre = input("Introduzca el nombre de la tarea: ").title()
    tareas_buscar = validar_tarea(nombre,tareas,tareas_rutina)

    if tareas_buscar is None:
        print("NO se encontro la tarea")

    else:
        print(f"Nombre: {tareas_buscar ['Nombre']} | Tipo: {tareas_buscar ['Tipo']} | Estado: {tareas_buscar ['Estado']}| Prioridad: {tareas_buscar['Prioridad']} | Hora: {tareas_buscar['Hora']}")

        confirmacion = input("¿Desea editar esta tarea? (S/N) ").lower()

        if confirmacion in ("s","si"):
            tareas.remove(tareas_buscar)
            tarea = datos_tarea()
            tareas.append(tarea)
            historial.append("Se edito la tarea: " + str(tarea))
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook)
            print("La tarea ha sido editada a: " + str(f"Nombre: {tarea['Nombre']} | Tipo: {tarea['Tipo']} | Estado: {tarea['Estado']}| Hora: {tarea['Hora']}"))

def editar_tarea(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook):
    print("Ha seleccionado Editar tarea")
    nombre = input("Introduzca el nombre de la tarea: ").title()

    tareas_editar = validar_tarea(nombre,tareas,tareas_rutina)
    if tareas_editar is None:
        print("Tarea no encontrada")
        return
    else:
        tareas.remove(tareas_editar)
        print(f"Nombre: {tareas_editar ['Nombre']} | Tipo: {tareas_editar ['Tipo']} | Estado: {tareas_editar ['Estado']}| Prioridad: {tareas_editar['Prioridad']}| Hora: {tareas_editar['Hora']}")
        editar = datos_tarea()
        tareas.append(editar)
        historial.append("Se edito la tarea: " + str(tareas_editar))
        print("La tarea ha sido editada a: " + str(f"Nombre: {editar['Nombre']} | Tipo: {editar['Tipo']} | Estado: {editar['Estado']}| Prioridad: {editar['Prioridad']}| Hora: {editar['Hora']}"))
        guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook)

def marcar_tarea_completa(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook):

    print("Ha seleccionado marcar tarea")
    nombre = input("Ingrese el nombre de la tarea: ").title()

    marcar_tarea = validar_tarea(nombre,tareas,tareas_rutina)

    if marcar_tarea is None:
        print("No se encontro la tarea")

    else:
        if marcar_tarea["Tipo"] == "Unica":
            if marcar_tarea["Estado"] == "Completada":
                print("Tarea encontrada")
                print("Esta tarea ya a sido marcada como completa")
            else:
                marcar_tarea["Estado"] = "Completada"
                print("Tarea encontrada")  
                print("¡Felicidades! Has completado la tarea, sigue asi")
                historial.append("Tarea completada: " + str(f"Nombre: {marcar_tarea['Nombre']} | Tipo: {marcar_tarea['Tipo']} | Estado: {marcar_tarea['Estado']} | Hora: {marcar_tarea["Hora"]}"))
                if marcar_tarea["Prioridad"] == "Alta":
                    puntaje = 15
                    puntos += puntaje
                elif marcar_tarea["Prioridad"] == "Media":
                    puntaje = 10
                    puntos += puntaje
                else:
                    puntaje = 5
                    puntos += puntaje
                print(f"¡Felicidades! Tu puntaje de diciplina subio a: {puntaje} sigue asi")
                print(f"¡Puntos totales: {puntos}!")
                guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook)
        else:
            fecha = datetime.now()
            fecha_m = fecha.strftime("%d/%m/%Y")
            marcar_tarea["Estado"] = f"Habito completodo el {fecha_m}"
            marcar_tarea["Racha"] += 1
            if marcar_tarea["Prioridad"] == "Alta":
                puntaje = 15
                puntos += puntaje
            elif marcar_tarea["Prioridad"] == "Media":
                puntaje = 10
                puntos += puntaje
            else:
                puntaje = 5
                puntos += puntaje
            print(f"¡Felicidades! Tu puntaje de diciplina subio a: {puntaje} sigue asi")
            print(f"¡Puntos totales: {puntos}!")
            registro_cumplidos.append({
                "Nombre": marcar_tarea["Nombre"],
                "Estado": marcar_tarea["Estado"],
                "Prioridad": marcar_tarea["Prioridad"],
                "Racha": marcar_tarea["Racha"]
            })
            historial.append(
                f"Habito de {marcar_tarea['Nombre']} completo racha de {marcar_tarea['Racha']}"
            )
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook)
    return puntos

def ver_tareas_pendiente(tareas):
    pendiente = False
    print("Ha seleccionado ver tareas completas")
    for prioridad in ["Alta", "Media", "Baja"]:
        for tarea in tareas:
            if tarea["Prioridad"] == prioridad and tarea["Estado"] == "Pendiente":
                pendiente = True
                print(f"Nombre: {tarea ['Nombre']} | Tipo: {tarea ['Tipo']} | Estado: {tarea ['Estado']}| Prioridad: {tarea['Prioridad']} | Hora: {tarea["Hora"]}")

    if not pendiente:
        print("No hay tareas Pendientes, ¡Sigue asi!")




def ver_tareas_completas(tareas,puntos):
    completada = False
    print("Ha seleccionado ver tareas completas")
    for prioridad in ["Alta", "Media", "Baja"]:
        for tarea in tareas:
            if tarea["Prioridad"] == prioridad and tarea["Estado"] == "Completada":
                completada = True
                print(tarea)
    if not completada:
        print("No hay tareas Pendientes, ¡Sigue asi!")
    print("Tu total de puntos de tareas completas es de: " + str(puntos))


def historial_f(historial):
    for m in historial:
        print("-",m)

def elimnar_tarea(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook):
    print("Ha seleccionado eliminar")
    nombre = input("Ingrese el nombre de la tarea o habito que desea eliminar: ").title()
    tareas_eliminar = validar_tarea(nombre,tareas,tareas_rutina)
    
    if tareas_eliminar is None:
        print("Tarea no encontrada")
        return

    confimacion = input("¿Seguro que desea eliminar esta tarea? (S/N): ").lower()
    if confimacion in ("s","si"):
        tareas.remove(tareas_eliminar)
        historial.append("Se elimino la tarea: " + str(f"Nombre: {tareas_eliminar['Nombre']} | Tipo: {tareas_eliminar['Tipo']} | Estado: {tareas_eliminar['Estado']}| Hora: {tareas_eliminar['Hora']}"))
        guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook)
        print("Tarea eliminada")
    else:
        print("Se cancelo la eliminación")

def estadisticas(tareas):
    print("La cantidad de tareas registradas son: ",len(tareas), "\n")

    completadas = sum(1 for t in tareas if t["Estado"] == "Completada")
    print("La cantidad de tareas Completadas son: ",completadas, "\n")

    pendientes = sum(1 for t in tareas if t["Estado"] == "Pendiente")
    print("La cantidad de tareas pendientes son: ",pendientes, "\n")
    if len(tareas) == 0:
        porcentaje_c = 0
    else:
        porcentaje_c = (completadas / len(tareas)) * 100

    if len(tareas) == 0:
        porcentaje_p = 0
    else:
        porcentaje_p = (pendientes / len(tareas)) * 100
    print(f"El porcentaje de tareas completas es de: {porcentaje_c:.2f}%")
    print(f"El porcentaje de tareas pendientes es de: {porcentaje_p:.2f}%\n")