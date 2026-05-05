import customtkinter as ctk
import subprocess
import os
import sys
from storage import cargar_datos
from config import VentanaConfiguraciones
from interfaz_gestor import ventanaGestionarTareas

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()

def iniciar_bot_discord():
    bot_path = os.path.join(BASE_DIR, "bot_disciplina")

    resultado = subprocess.run(["pgrep", "-f", "bot_disciplina"], capture_output=True)

    if resultado.returncode == 0:
        print("✅ El bot ya está activo.")
    else:
        if os.path.exists(bot_path):
            subprocess.Popen(
                [bot_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            print("🤖 Bot lanzado.")
        else:
            print(f"⚠️ No se encontró: {bot_path}")

def lanzar_vigilante():
    noti_path = os.path.join(BASE_DIR, "notificador")

    resultado = subprocess.run(["pgrep", "-f", "notificador"], capture_output=True)

    if resultado.returncode == 0:
        print("✅ Vigilante ya activo.")
    else:
        if os.path.exists(noti_path):
            subprocess.Popen([noti_path])
            print("🔔 Vigilante lanzado.")
        else:
            print(f"⚠️ No se encontró: {noti_path}")

if __name__ == "__main__":
    iniciar_bot_discord()
    lanzar_vigilante()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VentanaMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Menu")
        self.geometry("600x400")

        #TITULO
        self.titulo = ctk.CTkLabel(self, text="Menu", font=("Roboto", 20,"bold"))
        self.titulo.pack(pady=20)

        #Gestionar Tareas
        self.btn_gestor = ctk.CTkButton(self, text="Gestionar Tareas", command=self.añadir_tarea)
        self.btn_gestor.pack(pady=20)

        #Estadisticas
        self.btn_estadisticas = ctk.CTkButton(self, text="Estadisticas", command=VentanaEstadisticas)
        self.btn_estadisticas.pack(pady=20)

        #Historial
        self.btn_historial = ctk.CTkButton(self, text="Historial", command=VentanaHistorial)
        self.btn_historial.pack(pady=20)

        #Configuraciones
        self.btn_gestor = ctk.CTkButton(self, text="Configuraciones", command=VentanaConfiguraciones)
        self.btn_gestor.pack(pady=20)



    def añadir_tarea(self):
        self.withdraw() # El menú se esconde
        ventana_hija = ventanaGestionarTareas(self)

class VentanaHistorial(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Historial")
        self.geometry("600x400")

        #TITULO
        self.titulo = ctk.CTkLabel(self, text="Histrial De Acciones", font=("Roboto", 20,"bold"))
        self.titulo.pack(pady=20)

        self.scroll_historial = ctk.CTkScrollableFrame(self, width=550, height=350)
        self.scroll_historial.pack(padx=20, pady=10, fill="both", expand=True)

        self.cargar_historial_visual()
    
    def cargar_historial_visual(self):
        tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()

        historial_reciente = historial[::-1]

        for i, entrada in enumerate(historial_reciente):
            # Calculamos el número real (si hay 10 items, el primero arriba es el 10)
            numero = len(historial) - i
            
            # Creamos una fila para cada registro
            fila = ctk.CTkFrame(self.scroll_historial, fg_color="transparent")
            fila.pack(fill="x", pady=2)

            # Texto del número (con color diferente para que resalte)
            lbl_num = ctk.CTkLabel(fila, text=f"[{numero:03d}]", font=("Consolas", 12), text_color="#5dade2")
            lbl_num.pack(side="left", padx=5)

            # El mensaje del historial
            lbl_texto = ctk.CTkLabel(fila, text=entrada, font=("Roboto", 12))
            lbl_texto.pack(side="left", padx=5)
            
            # Una línea sutil de separación
            separador = ctk.CTkFrame(self.scroll_historial, height=1, fg_color="#34495e")
            separador.pack(fill="x", padx=10, pady=2)


class VentanaEstadisticas(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Estadisticas")
        self.geometry("600x500")

        #TITULO
        self.titulo = ctk.CTkLabel(self, text="Estadisticas", font=("Roboto", 20,"bold"))
        self.titulo.pack(pady=20)

        self.estadisticas()

    def estadisticas(self):
        tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()

        lista_r = tareas_rutina
        lista_u = tareas
        lista_general = tareas + tareas_rutina

        #Cantidad completadas
        completadas_rutina = sum(1 for t in lista_r if t.estado != "Pendiente")

        self.lbl_completas_r = ctk.CTkLabel(self, text=f"La cantidad de habitos completados es de {completadas_rutina}", text_color="green")
        self.lbl_completas_r.pack(pady=20)

        completadas_tareas = sum(1 for t in lista_u if t.estado != "Pendiente")

        self.lbl_completas_t = ctk.CTkLabel(self, text=f"La cantidad de tareas completadas son de {completadas_tareas}", text_color="green")
        self.lbl_completas_t.pack(pady=10)

        completadas = completadas_tareas + completadas_rutina

        #Cantidad pendientes
        pendientes_rutina = sum(1 for t in lista_r if t.estado == "Pendiente")

        self.lbl_pendientes_r = ctk.CTkLabel(self, text=f"La cantidad de habitos pendientes es de {pendientes_rutina}", text_color="green")
        self.lbl_pendientes_r.pack(pady=20)

        pendientes_tareas = sum(1 for t in lista_u if t.estado == "Pendiente")

        self.lbl_pendientes_t = ctk.CTkLabel(self, text=f"La cantidad de tareas pendientes son de {pendientes_tareas}", text_color="red")
        self.lbl_pendientes_t.pack(pady=10)

        pendientes = pendientes_tareas + pendientes_rutina

        if len(lista_general) == 0:
            porcentaje_c = 0
        else:
            porcentaje_c = (completadas / len(lista_general)) * 100

        if len(lista_general) == 0:
            porcentaje_p = 0
        else:
            porcentaje_p = (pendientes / len(lista_general)) * 100

        self.lbl_porcentajes_completas = ctk.CTkLabel(self,text=f"El porcentaje de tareas y habitos completados es de: {porcentaje_c}%",text_color="green")
        self.lbl_porcentajes_completas.pack(pady=10)

        self.lbl_porcentajes_pendientes = ctk.CTkLabel(self,text=f"El porcentaje de tareas y habitos pendientes es de: {porcentaje_p}%",text_color="red")
        self.lbl_porcentajes_pendientes.pack(pady=10)

        self.mostrar_progreso(puntos)
    
    def mostrar_progreso(self, puntos_actuales):
        # Definimos la meta (ejemplo: 100 puntos para subir de rango)
        meta_puntos = 100
        
        # Calculamos el porcentaje (debe ser entre 0.0 y 1.0)
        porcentaje = puntos_actuales / meta_puntos
        
        # Si te pasas de 100, la barra se queda al máximo (1.0)
        if porcentaje > 1.0: porcentaje = 1.0

        # Título del Rango
        rango = "Novato" if puntos_actuales < 100 else "Guerrero"
        self.lbl_rango = ctk.CTkLabel(self, text=f"Rango: {rango}", font=("Roboto", 18, "bold"))
        self.lbl_rango.pack(pady=5)

        # LA BARRA
        self.barra_progreso = ctk.CTkProgressBar(self, width=400, height=20)
        self.barra_progreso.set(porcentaje) # Aquí le damos el valor
        self.barra_progreso.pack(pady=10)
        
        # Texto debajo de la barra
        self.lbl_puntos = ctk.CTkLabel(self, text=f"{puntos_actuales} / {meta_puntos} XP")
        self.lbl_puntos.pack()


ventana = VentanaMenu()
ventana.mainloop()