import sqlite3
import os
import json
import sys
from datetime import datetime
import tkinter.messagebox as messagebox
from clases import Tarea,TareaRutina

if getattr(sys, 'frozen', False):
    ruta_base = os.path.dirname(sys.executable)
else:
    ruta_base = os.path.dirname(os.path.abspath(__file__))

CARPETA_DATA = os.path.join(ruta_base, "data")
os.makedirs(CARPETA_DATA, exist_ok=True)

def crear_tablas():
    conexion = sqlite3.connect("data/gestor.db")
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        creacion TEXT NOT NULL,
        nombre TEXT NOT NULL,
        estado TEXT DEFAULT 'pendiente',
        hora TEXT,
        prioridad TEXT NOT NULL,
        tipo TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rutinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        creacion TEXT NOT NULL,
        nombre TEXT NOT NULL,
        estado TEXT DEFAULT 'pendiente',
        hora TEXT,
        prioridad TEXT NOT NULL,
        tipo TEXT NOT NULL,
        racha INTEGER,
        dias TEXT
    )
    """)

    conexion.commit()
    conexion.close()

    conexion = sqlite3.connect("data/historial.db")
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarea TEXT NOT NULL,
        accion TEXT NOT NULL,
        fecha TEXT NOT NULL 
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS papelera (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        creacion TEXT NOT NULL,
        nombre TEXT NOT NULL,
        estado TEXT DEFAULT 'pendiente',
        hora TEXT,
        prioridad TEXT NOT NULL,
        tipo TEXT NOT NULL,
        racha INTEGER,
        dias TEXT,
        accion TEXT NOT NULL
    )
    """)

    conexion.commit()
    conexion.close()

    conexion = sqlite3.connect("data/registro.db")
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarea TEXT NOT NULL,
        accion TEXT NOT NULL,
        fecha TEXT NOT NULL
    )
    """)
    conexion.commit()
    conexion.close()


def guardar_tareas(tipo,tarea):
    conexion = sqlite3.connect("data/gestor.db")
    cursor = conexion.cursor()

    if tipo == "Unica":
        cursor.execute("""
        INSERT INTO tareas
        (creacion, nombre, estado, hora, prioridad, tipo)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            tarea.creacion,
            tarea.nombre,
            tarea.estado,
            tarea.hora,
            tarea.prioridad,
            tarea.tipo
        ))
        conexion.commit()
        conexion.close()

        accion = "Se agrego una Tarea Unica"
        guardar_historial(tarea,accion)

    else:
        cursor.execute("""
        INSERT INTO rutinas
        (creacion, nombre, estado, hora, prioridad, tipo, racha, dias)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tarea.creacion,
            tarea.nombre,
            tarea.estado,
            tarea.hora,
            tarea.prioridad,
            tarea.tipo,
            tarea.racha,
            json.dumps(tarea.dias,ensure_ascii=False)
        ))
        conexion.commit()
        conexion.close()

        accion = "Se agrego una Tarea Rutina"
        guardar_historial(tarea,accion)

def guardar_historial(tarea,accion):
    fecha = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    tarea_historial = f"| {tarea.creacion} | {tarea.nombre} | {tarea.tipo} |{tarea.estado} |{tarea.hora} | {tarea.prioridad} |"
    
    conexion = sqlite3.connect("data/historial.db")
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO historial 
    (tarea,accion,fecha)
    VALUES (?,?,?)
    """, (
        (tarea_historial,accion,fecha)
    ))
    conexion.commit()
    conexion.close()

def guardar_papelera(tarea):
    conexion = sqlite3.connect("data/historial.db")
    cursor = conexion.cursor()

    accion_r = "Se elimino"

    if tarea.tipo == "Rutina":
        cursor.execute("""
        INSERT INTO papelera
        (creacion, nombre, estado, hora, prioridad, tipo, racha, dias, accion)  
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
            tarea.creacion,
            tarea.nombre,
            tarea.estado,
            tarea.hora,
            tarea.prioridad,
            tarea.tipo,
            tarea.racha,
            json.dumps(tarea.dias,ensure_ascii=False),
            accion_r
        ))
    
    else:
        cursor.execute("""
        INSERT INTO papelera
        (creacion, nombre, estado, hora, prioridad, tipo, accion)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            tarea.creacion,
            tarea.nombre,
            tarea.estado,
            tarea.hora,
            tarea.prioridad,
            tarea.tipo,
            accion_r
        ))
    conexion.commit()
    conexion.close()

def guardar_registros(tarea,estado,accion):
    fecha = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    tarea_tegistro = f"| {tarea.creacion} | {tarea.nombre} | {tarea.tipo} | {estado} | {tarea.hora} | {tarea.prioridad} |"

    conexion = sqlite3.connect("data/registro.db")
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO registro 
    (tarea,accion,fecha)
    VALUES (?,?,?)
    """, (
        (tarea_tegistro,accion,fecha)
    ))
    conexion.commit()
    conexion.close()


def cargar_tareas():
    conexion = sqlite3.connect("data/gestor.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id, creacion, nombre, estado, hora, prioridad, tipo
    FROM tareas
    """)
    filas = cursor.fetchall()

    tareas = []

    for fila in filas:
        tarea = Tarea(
            id=fila[0],
            creacion=fila[1],
            nombre=fila[2],
            estado=fila[3],
            hora=fila[4],
            prioridad=fila[5],
            tipo=fila[6]
        )
        tareas.append(tarea)
    
    cursor.execute("""
    SELECT id, creacion, nombre, estado, hora, prioridad, tipo, racha, dias
    FROM rutinas
    """)
    filas_rutina = cursor.fetchall()

    rutinas = []

    for fila in filas_rutina:
        rutina = TareaRutina(
            id=fila[0],
            creacion=fila[1],
            nombre=fila[2],
            estado=fila[3],
            hora=fila[4],
            prioridad=fila[5],
            tipo=fila[6],
            racha=fila[7],
            dias=json.loads(fila[8])
        )
        rutinas.append(rutina)

    conexion.close()

    return tareas, rutinas

def cargar_historial():
    conexion = sqlite3.connect("data/historial.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT tarea, accion, fecha
        from historial
    """)

    filas_historial = cursor.fetchall()


    cursor.execute("""
    SELECT id, creacion, nombre, estado, tipo, accion
        from papelera
    """)

    filas_papelera = cursor.fetchall()

    historial = []

    for fila in filas_historial:
        historial.append(fila)
    
    for fila in filas_papelera:
        historial.append(fila)

    conexion.close()

    return historial

def cargar_registros():
    conexion = sqlite3.connect("data/registro.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id, tarea, accion, fecha
        from registro
    """)

    filas_historial = cursor.fetchall()

    registros = []

    for fila in filas_historial:
        registros.append(fila)
    
    conexion.close()

    return registros

def estado_tarea(estado,racha,tarea):
    conexion = sqlite3.connect("data/gestor.db")
    cursor = conexion.cursor()

    if tarea.tipo == "Unica":

        id_tarea = tarea.id

        cursor.execute("""
        UPDATE tareas
        SET estado = ?
        WHERE id = ?
        """, (estado, id_tarea))

        conexion.commit()
        conexion.close()

        accion = "Se completo la Tarea Unica"
        guardar_registros(tarea,estado,accion)

    else:
        id_tarea = tarea.id

        cursor.execute("""
            UPDATE rutinas
            SET estado = ?,
                racha = ?
            WHERE id = ?
            """, (estado, racha, id_tarea))

        conexion.commit()
        conexion.close()

        if "Habito completado" in estado:
            accion = f"Se completo la Tarea Rutina, Racha: {racha}"
        elif "Fallida" in estado:
            accion = f"Se fallo la Tarea Rutina"

        guardar_registros(tarea,estado,accion)


def eliminar_tarea_sql(tarea):
    conexion = sqlite3.connect("data/gestor.db")
    cursor = conexion.cursor()

    if tarea.tipo == "Unica":
        cursor.execute("""
        DELETE FROM tareas
        WHERE id = ?
        """, (tarea.id,))

        conexion.commit()
        conexion.close()

        guardar_papelera(tarea)
    
    else:
        cursor.execute("""
        DELETE FROM rutinas
        WHERE id = ?
        """, (tarea.id,))

        conexion.commit()
        conexion.close()

        guardar_papelera(tarea)

def resturar_tarea(id_r):
    conexion = sqlite3.connect("data/historial.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM papelera WHERE id = ?", (id_r,))

    tarea = cursor.fetchone()

    conexion.close()

    tipo = tarea[6]

    if tipo == "Rutina":
        restauar = TareaRutina(
            id=tarea[0],
            creacion=tarea[1],
            nombre=tarea[2],
            estado=tarea[3],
            hora=tarea[4],
            prioridad=tarea[5],
            tipo=tarea[6],
            racha=tarea[7],
            dias=tarea[8]
        )

    else:
        restauar = Tarea(
            id=tarea[0],
            creacion=tarea[1],
            nombre=tarea[2],
            estado=tarea[3],
            hora=tarea[4],
            prioridad=tarea[5],
            tipo=tarea[6]
        )

    guardar_tareas(tipo=tipo,tarea=restauar)

    conexion = sqlite3.connect("data/historial.db")
    cursor = conexion.cursor()
    print(id_r)
    cursor.execute("""
        DELETE FROM papelera
        WHERE id = ?
        """, (id_r,))

    conexion.commit()
    conexion.close()

    messagebox.showinfo("Restaurar","Se a restaurado correctamente la tarrea")

    return

def limpiar_tareas():
    conexion = sqlite3.connect("data/gestor.db")
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM tareas WHERE estado = ?", ('Completada',))

    conexion.commit()
    conexion.close()