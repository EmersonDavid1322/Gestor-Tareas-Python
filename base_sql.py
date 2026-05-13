import sqlite3
import os
import json
import sys
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
        accion TEXT NOT NULL
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

def guardar_historial(accion):
    conexion = sqlite3.connect("data/historial.db")
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO historial 
    (accion)
    VALUES (?)
    """, (
        (accion,)
    ))
    conexion.commit()
    conexion.close()

def guardar_registros(accion):
    conexion = sqlite3.connect("data/registro.db")
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO registro 
    (accion)
    VALUES (?)
    """, (
        (accion,)
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
    SELECT id, accion
        from historial
    """)

    filas_historial = cursor.fetchall()

    historial = []

    for fila in filas_historial:
        historial.append(fila)
    
    conexion.close()

    return historial

def cargar_registros():
    conexion = sqlite3.connect("data/registro.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id, accion
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
    
    else:
        cursor.execute("""
        DELETE FROM rutinas
        WHERE id = ?
        """, (tarea.id,))

        conexion.commit()
        conexion.close()

