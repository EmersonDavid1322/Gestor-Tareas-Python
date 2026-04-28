from storage import guardar_datos
from datetime import datetime
from clases import TareaRutina, Tarea

def menu_f():
    print("1) Gestionar Tareas")
    print("2) Historial")
    print("3) Estadisticas")
    print("4) Configuraciones")
    print("5) Salir")
    while True:
        try:
            opcion = int(input("Introduzca una opción deseada: "))
            return opcion
        except ValueError:
            print("Caracter no valido")



def validar_tarea(nombre,tareas,tareas_rutina):
    for t in tareas + tareas_rutina:
        if t.nombre == nombre:
            return t


def agregar_tarea(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase):
    print("Ha seleccionado agregar tarea")
    tarea_datos = datos_tarea()
    tarea_añadir = validar_tarea(tarea_datos.nombre,tareas,tareas_rutina)

    if tarea_añadir is None:
        if tarea_datos.tipo == "Rutina":
            tareas_rutina.append(tarea_datos)
            historial.append("Se añadió la tarea rutinaria: " + tarea_datos.nombre)
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase)
            print("Tarea rutina agregada correctamente")
            return
        else:
            tareas.append(tarea_datos)
            historial.append("Se añadió la tarea unica: " + tarea_datos.nombre)
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase)
            print("Tarea agregada correctamente")
    else:
        if tarea_datos.tipo == "Rutina":
            print(f"La tarea '{tarea_datos.nombre}' ya ha sido añadida anteriormente, las tareas tipo rutina no se pueden duplicar")
            return
        else:
            duplicada = input("Esta tarea ya existe, ¿desea duplicarla? (S/N): ").lower()
            if duplicada in ("s", "si"):
                tareas.append(tarea_datos)
                historial.append("Se añadió tarea duplicada: " + tarea_datos.nombre)
                guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase)
                print("Tarea duplicada añadida")
                return
            else:
                print("No se añadió la tarea")


def datos_tarea():
    nombre = input("Ingrese el nombre de la tarea: ").title()
    while True:
        prioridad = input('Ingrese la prioridad de la tarea (Alta/Media/Baja): ').title()
        if prioridad == "Alta":
            tarea_prioridad = "Alta"
            break
        elif prioridad == "Media":
            tarea_prioridad  = "Media"
            break
        elif prioridad == "Baja":
            tarea_prioridad  = "Baja"
            break
        else:
            print("Opción no valida")
    while True:
        try:
            tipo_tarea = int(input(" 1)Unica \n 2)Rutina \n Tipo de tarea: "))
            if tipo_tarea == 1:
                tarea_añadir = Tarea(nombre,tarea_prioridad )
            elif tipo_tarea == 2:
                tarea_añadir = TareaRutina(nombre,tarea_prioridad)
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
                    tarea_añadir.hora = hora
                    break
                else:
                    print('Hora incorrecta, por favor ingrese en formato "HH:MM" ')
            else:
                print('Hora incorrecta, por favor ingrese en formato "HH:MM" ')
        else:
            break
    while True:
        confimacion = input("\n (Por defecto todos los dias)\n¿Desea modificar los dias de esta tarea? (S/N): ").lower()
        if confimacion in ("s","si"):

            dias_validos = ["lunes","martes","miércoles","jueves","viernes","sabado","domingo"]
            dias_verficados = []

            entrada = input("(Separe cada dia con una ',')\nIntroduzca los dias que desea: ").strip().lower().split(",")
            for dia in entrada:
                if dia in dias_validos:
                    dias_verficados.append(dia)
                else:
                    print(f"¡Cuidado! '{dia}' no existe y sera ignorado\n")
        else:
            print("Se mantuvo la configuración por defecto")
        print(f"Dias agregados para esta tarea: {dias_verficados}")
        tarea_añadir.dias = dias_verficados
        break
    return tarea_añadir

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
                    if t.prioridad == prioridad:
                        t.mostrar_informacion()
        if len(tareas_rutina) == 0:
            print("No hay tareas rutinarias")
        else:
            print("\tHabitos activos\t")
        for t_r in tareas_rutina:
            t_r.mostrar_informacion()
    else:   
        print("Ha seleccionado ver registro de habitos cumplidos")
        if len(registro_cumplidos) == 0:
            print("NO hay registro de habitos cumplidos")
        else:
            for registro in registro_cumplidos:
                print(registro)

def buscar_tarea(tareas, historial,puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase):
    print("Ha seleccionado Buscar tarea")
    nombre = input("Introduzca el nombre de la tarea: ").title()
    tareas_buscar = validar_tarea(nombre,tareas,tareas_rutina)

    if tareas_buscar is None:
        print("NO se encontro la tarea")

    else:
        tareas_buscar.mostrar_informacion()
        confirmacion = input("¿Desea editar esta tarea? (S/N) ").lower()

        if confirmacion in ("s","si"):
            if tareas_buscar.tipo == "Rutina":
                tareas_rutina.remove(tareas_buscar)
                tarea = datos_tarea()
                tareas_rutina.append(tarea)
            else:
                tareas.remove(tareas_buscar)
                tarea = datos_tarea()
                tareas.append(tarea)
            historial.append("Se edito la tarea: " + tarea.nombre)
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase)
            print("La tarea a sido editada")
            tarea.mostrar_informacion()

def editar_tarea(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase):
    print("Ha seleccionado Editar tarea")
    nombre = input("Introduzca el nombre de la tarea: ").title()

    tareas_editar = validar_tarea(nombre,tareas,tareas_rutina)
    if tareas_editar is None:
        print("Tarea no encontrada")
        return
    else:
        if tareas_editar.tipo == "Rutina":
            tareas_rutina.remove(tareas_editar)
            tarea = datos_tarea()
            tareas_rutina.append(tarea)
        else:
            tareas.remove(tareas_editar)
            tarea = datos_tarea()
            tareas.append(tarea)
        historial.append("Se edito la tarea: " + tarea.nombre)
        guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase)
        print("La tarea a sido editada")
        tarea.mostrar_informacion()

def marcar_tarea_completa(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase):

    print("Ha seleccionado marcar tarea")
    nombre = input("Ingrese el nombre de la tarea: ").title()

    marcar_tarea = validar_tarea(nombre,tareas,tareas_rutina)

    if marcar_tarea is None:
        print("No se encontro la tarea")

    else:
        if marcar_tarea.tipo == "Unica":
            if marcar_tarea.estado == "Completada":
                print("Tarea encontrada")
                print("Esta tarea ya a sido marcada como completa")
            else:
                marcar_tarea.estado = "Completada"
                print("Tarea encontrada")  
                print("¡Felicidades! Has completado la tarea, sigue asi")
                historial.append("Tarea completada: " + marcar_tarea.nombre)
                if marcar_tarea.prioridad == "Alta":
                    puntaje = 15
                    puntos += puntaje
                elif marcar_tarea.prioridad == "Media":
                    puntaje = 10
                    puntos += puntaje
                else:
                    puntaje = 5
                    puntos += puntaje
                print(f"¡Felicidades! Tu puntaje de diciplina subio a: {puntaje} sigue asi")
                print(f"¡Puntos totales: {puntos}!")
                guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase)
        else:
            fecha = datetime.now()
            fecha_m = fecha.strftime("%d/%m/%Y")
            marcar_tarea.estado = f"Habito completado el {fecha_m}"
            marcar_tarea.racha += 1
            if marcar_tarea.prioridad == "Alta":
                puntaje = 15
                puntos += puntaje
            elif marcar_tarea.prioridad == "Media":
                puntaje = 10
                puntos += puntaje
            else:
                puntaje = 5
                puntos += puntaje
            print(f"¡Felicidades! Tu puntaje de diciplina subio a: {puntaje} sigue asi")
            print(f"¡Puntos totales: {puntos}!")
            registro_cumplidos.append({
                "Nombre": marcar_tarea.nombre,
                "Estado": marcar_tarea.estado,
                "Prioridad": marcar_tarea.prioridad,
                "Racha": marcar_tarea.racha
            })
            historial.append(
                f"Habito de {marcar_tarea.nombre} completo racha de {marcar_tarea.racha}"
            )
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase)
    return puntos

def ver_tareas_pendiente(tareas):
    pendiente = False
    print("Ha seleccionado ver tareas pendientes")
    for prioridad in ["Alta", "Media", "Baja"]:
        for tarea in tareas:
            if tarea.prioridad == prioridad and tarea.estado == "Pendiente":
                pendiente = True
                tarea.mostrar_informacion()
    if not pendiente:
        print("No hay tareas Pendientes, ¡Sigue asi!")




def ver_tareas_completas(tareas,puntos):
    completada = False
    print("Ha seleccionado ver tareas completas")
    for prioridad in ["Alta", "Media", "Baja"]:
        for tarea in tareas:
            if tarea.prioridad == prioridad and tarea.estado == "Completada":
                completada = True
                tarea.mostrar_informacion()
    if not completada:
        print("No hay tareas Pendientes, ¡Sigue asi!")
    print("Tu total de puntos de tareas completas es de: " + str(puntos))


def historial_f(historial):
    if len(historial) == 0:
        print("No hay movimientos registrado\n")
    else:
        for m in historial:
            print("-",m,"\n")

def elimnar_tarea(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase):
    print("Ha seleccionado eliminar")
    nombre = input("Ingrese el nombre de la tarea o habito que desea eliminar: ").title()
    tareas_eliminar = validar_tarea(nombre,tareas,tareas_rutina)
    
    if tareas_eliminar is None:
        print("Tarea no encontrada")
        return

    confimacion = input("¿Seguro que desea eliminar esta tarea? (S/N): ").lower()
    if confimacion in ("s","si"):
        if tareas_eliminar.tipo == "Rutina":
            tareas_rutina.remove(tareas_eliminar)
        else:
            tareas.remove(tareas_eliminar)
        historial.append("Se elimino la tarea: " + str(f"Nombre: {tareas_eliminar.nombre} | Tipo: {tareas_eliminar.tipo} | Estado: {tareas_eliminar.estado}| Hora: {tareas_eliminar.hora}"))

        guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase)

        print("Tarea eliminada")
    else:
        print("Se cancelo la eliminación")

def estadisticas(tareas):
    print("La cantidad de tareas registradas son: ",len(tareas), "\n")

    completadas = sum(1 for t in tareas if t.estado == "Completada")
    print("La cantidad de tareas Completadas son: ",completadas, "\n")

    pendientes = sum(1 for t in tareas if t.estado == "Pendiente")
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