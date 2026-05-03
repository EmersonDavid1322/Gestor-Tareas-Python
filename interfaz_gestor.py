from datetime import datetime
import customtkinter as ctk
import tkinter.messagebox as messagebox
from storage import guardar_datos,cargar_datos
from clases import Tarea,TareaRutina

def validar_tarea(nombre,tareas,tareas_rutina):
    for t in tareas + tareas_rutina:
        if t.nombre == nombre:
            return t

class ventanaGestionarTareas(ctk.CTkToplevel):
    def __init__(self,menu_principal):
        super().__init__()
        self.title("Gestior")
        self.geometry("600x400")

        self.menu_principal = menu_principal

        #TITULO
        self.titulo = ctk.CTkLabel(self, text="Gestionar Tareas", font=("Roboto", 20,"bold"))
        self.titulo.pack(pady=20)

        #crear tareas
        self.btn_crear = ctk.CTkButton(self, text="Gestión De Tareas", command= VentanaAnadirTareas)
        self.btn_crear.pack(pady=20)

        #Marcar tarea completa
        self.btn_completar = ctk.CTkButton(self, text="Marcar Tarea", command= VentanaCompletar)
        self.btn_completar.pack(pady=20)

        #ver tareas/editar/eliminar
        self.btn_tareas = ctk.CTkButton(self, text="Tareas", command= VentanaTareas)
        self.btn_tareas.pack(pady=20)

        #volver al menu
        self.btn_volver= ctk.CTkButton(self, text="Volver Menu", command= self.volver_al_menu)
        self.btn_volver.pack(pady=20)

        self.protocol("WM_DELETE_WINDOW", self.volver_al_menu)
    def volver_al_menu(self):
        self.menu_principal.deiconify()
        self.destroy()

class VentanaAnadirTareas(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Añadir Tarea")
        self.geometry("800x600")

        #TITULO
        self.titulo = ctk.CTkLabel(self, text="Nueva Tarea", font=("Roboto", 20,"bold"))
        self.titulo.pack(pady=20)

        #nombre
        self.nombre_entrada = ctk.CTkEntry(self, placeholder_text="Nombre de la tarea...",width=300)
        self.nombre_entrada.pack(pady=10)

        #PRIORIDADES
        self.label_prio = ctk.CTkLabel(self, text="Prioridad")
        self.label_prio.pack(pady=10)
        self.btn_prio = ctk.CTkSegmentedButton(self, values=["Baja","Media","Alta"])
        self.btn_prio.set("Media")
        self.btn_prio.pack(pady=10)

        #TIPO
        self.label_tipo = ctk.CTkLabel(self, text="Tipo De Tarea")
        self.label_tipo.pack(pady=10)
        self.btn_tipo = ctk.CTkSegmentedButton(self, values=["Rutina","Tarea"])
        self.btn_tipo.set("Rutina")
        self.btn_tipo.pack(pady=10)

        #HORA
        self.frame_tiempo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_tiempo.pack(pady=10)

        horas_validas = [f"{i:02d}" for i in range(24)]
        self.combo_hora = ctk.CTkOptionMenu(self.frame_tiempo, values=horas_validas, width=70)
        self.combo_hora.pack(side="left", padx=5)

        self.lbl_puntos = ctk.CTkLabel(self.frame_tiempo, text=":", font=("Roboto", 20))
        self.lbl_puntos.pack(side="left")

        minutos_validos = [f"{i:02d}" for i in range(60)]
        self.combo_minutos = ctk.CTkOptionMenu(self.frame_tiempo, values=minutos_validos, width=70)
        self.combo_minutos.pack(side="left", padx=5)

        #DIAS
        self.frame_dias = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_dias.pack(pady=10)

        self.dias_disponibles = ["lunes","martes","miércoles","jueves","viernes","sabado","domingo"]
        self.dias_selccionados = {}

        for dia in self.dias_disponibles:
            cb = ctk.CTkCheckBox(self.frame_dias, text=dia, width=45)
            cb.pack(side="left", padx=2)
            self.dias_selccionados[dia] = cb

        #ERRORES
        self.lbl_info = ctk.CTkLabel(self, text="", text_color="red")
        self.lbl_info.pack(pady=10)

        #GUARDAR
        self.btn_guardar = ctk.CTkButton(self, text="Crear Tarea", command=self.sacar_datos)
        self.btn_guardar.pack(pady=20)

    def sacar_datos(self): #sacamos la informacion de la ventana y la convertimos en datos que utilizamos
        self.nombre = self.nombre_entrada.get()
        if not self.nombre:
            self.lbl_info.configure(text="⚠️ No se puede agregar tarea sin un nombre")
            return

        self.prioridad = self.btn_prio.get()
        self.tipo = self.btn_tipo.get()
        self.hora_p = self.combo_hora.get()
        self.minutos_p = self.combo_minutos.get()
        self.tiempo = f"{self.hora_p}:{self.minutos_p}"
        self.dias = []

        for dia, check in self.dias_selccionados.items():
            if check.get() == 1:
                self.dias.append(dia)

        tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
        
        self.agregar_tarea(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)

    def agregar_tarea(self,tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal): 
        #verifica que al tarea no este repetida y se encarga de añadir la tarea a las listan en forma de objetos
        
        if self.tipo == "Tarea":
            tarea_datos = Tarea(self.nombre,self.prioridad,self.tiempo)
        else:
            tarea_datos = TareaRutina(self.nombre,self.prioridad,self.tiempo,self.dias)

        tarea_añadir = validar_tarea(tarea_datos.nombre,tareas,tareas_rutina)

        if tarea_añadir is None:
            if tarea_datos.tipo == "Rutina":
                tareas_rutina.append(tarea_datos)
                historial.append("Se añadió la tarea rutinaria: " + tarea_datos.nombre)
                guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
                self.destroy()
                messagebox.showinfo("Añadir Tareas",f"Tarea rutina agregada {tarea_datos.nombre} correctamente")
                return
            else:
                tareas.append(tarea_datos)
                historial.append("Se añadió la tarea unica: " + tarea_datos.nombre)
                guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
                self.destroy()
                messagebox.showinfo("Añadir Tareas",f"Tarea agregada {tarea_datos.nombre} correctamente")
        else:
            if tarea_datos.tipo == "Rutina":
                print(f"La tarea '{tarea_datos.nombre}' ya ha sido añadida anteriormente, las tareas tipo rutina no se pueden duplicar")
                return
            else:
                respuesta = messagebox.askyesno("Tarea Duplicada", f"La tarea '{self.nombre}' ya existe. ¿Deseas duplicarla?",parent=self)
                if respuesta:
                    tareas.append(tarea_datos)
                    historial.append("Se añadió tarea duplicada: " + tarea_datos.nombre)
                    guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
                    self.destroy()
                    messagebox.showinfo("Añadir Tareas",f"Tarea agregada {tarea_datos.nombre} correctamente")
                    return
                else:
                    self.lbl_info.configure(text="Cambia el nombre para evitar duplicados")

class VentanaCompletar(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Marcar Tareas")
        self.geometry("800x600")

        #TITULO
        self.titulo = ctk.CTkLabel(self, text="Completar", font=("Roboto", 20,"bold"))
        self.titulo.pack(pady=20)

        #Nombre tarea
        self.nombre_entrada = ctk.CTkEntry(self, placeholder_text="Nombre de la tarea...",width=300)
        self.nombre_entrada.pack(pady=10)

        #completar
        self.btn_completar = ctk.CTkButton(self, text="Completar", command=self.completar)
        self.btn_completar.pack(pady=10)

        #Mensaje
        self.mensaje = ctk.CTkLabel(self, text="", text_color="green")
        self.mensaje.pack(pady=10)


        #Mensaje informativo
        self.info = ctk.CTkLabel(self, text="", text_color="red")
        self.info.pack(pady=10)

    def completar(self):
        tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
        nombre = self.nombre_entrada.get()
        marcar_tarea = validar_tarea(nombre,tareas,tareas_rutina)

        if marcar_tarea is None:
            self.info.configure(text="Tarea no encontrada")

        else:
            if marcar_tarea.tipo == "Unica":
                if marcar_tarea.estado == "Completada":
                    self.info.configure(text="Tarea no encontrada")
                    messagebox.showinfo("Completar",f"La tarea {marcar_tarea.nombre} ya a sido marcada")
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
                    self.mensaje.configure(text=f"¡Felicidades! Tu puntaje de diciplina subio a: {puntaje} sigue asi")
                    guardar_datos(tareas, historial, puntos_v,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
            else:
                tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
                fecha = datetime.now()
                fecha_m = fecha.strftime("%d/%m/%Y")
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
                self.mensaje.configure(text=f"¡Felicidades! Tu puntaje de diciplina subio a: {puntaje} sigue asi")
                messagebox.showinfo("Completar","¡Felicidades! Has completado la tarea, sigue asi")
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

class VentanaTareas(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Marcar Tareas")
        self.geometry("800x600")

        self.frame_busqueda = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_busqueda.pack(pady=10, fill="x", padx=20)

        self.entrada_busqueda = ctk.CTkEntry(self.frame_busqueda, 
                                            placeholder_text="🔍 Buscar tarea por nombre...",
                                            height=35)
        self.entrada_busqueda.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Este evento detecta cuando escribes algo
        self.entrada_busqueda.bind("<KeyRelease>", self.al_escribir)

        self.scroll_tareas = ctk.CTkScrollableFrame(self, label_text="Lista de Actividades")
        self.scroll_tareas.pack(padx=20, pady=20, fill="both", expand=True)

        self.mostrar_tareas()

    def al_escribir(self, event):
    # Cada vez que escribes, refrescamos la lista pasando el texto actual
        texto = self.entrada_busqueda.get()
        self.mostrar_tareas(filtro=texto)


    def mostrar_tareas(self,filtro=""):
        for widget in self.scroll_tareas.winfo_children():
            widget.destroy()

        tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()

        tareas_filtradas = [tarea for tarea in tareas if filtro.lower() in tarea.nombre.lower()]
        rutinas_filtradas = [rutina for rutina in tareas_rutina if filtro.lower() in rutina.nombre.lower()]

        if not tareas_filtradas and not rutinas_filtradas:
            ctk.CTkLabel(self.scroll_tareas, text="No se encontraron coincidencias 😕", font=("Roboto", 14, "italic")).pack(pady=20)

        self.creacion_seccion("-----Tareas-----", tareas_filtradas, es_rutina=False)
        self.creacion_seccion("-----Habitos-----",rutinas_filtradas, es_rutina=True)

    def creacion_seccion(self,titulo,lista,es_rutina):

        ctk.CTkLabel(self.scroll_tareas,text=titulo,font=("Roboto", 16, "bold")).pack(pady=10)

        for i, tarea in enumerate(lista):
            color = "#1f538d" if not es_rutina else "#2d7d52"
            fila = ctk.CTkFrame(self.scroll_tareas,border_width=2, border_color=color)
            fila.pack(fill="x", pady=5, padx=5)

            #informacion de la tarea
            info_ta = f"| {tarea.nombre} | {tarea.prioridad} | {tarea.hora} |".title()
            info_lbl = ctk.CTkLabel(fila, text=info_ta, font=("Roboto", 12))
            info_lbl.pack(side="left", padx=15, pady=10)

            #eliminar tarea
            boton_elimnar = ctk.CTkButton(fila,text="x", width=30, fg_color="#922b21", hover_color="#641e16",
                                            command=lambda idx=i, r=es_rutina, msg=True: self.eliminar_tarea(idx,r,msg))
            boton_elimnar.pack(side="right", padx=10)

            #editar tarea
            boton_editar = ctk.CTkButton(fila,text="Editar", width=50,
                                        command=lambda r=es_rutina, idx=i,msg=False: self.editar_tarea(idx,r,msg))
            boton_editar.pack(side="right", padx=10)
            
            #mostar informacion completa de la tarea
            boton_info = ctk.CTkButton(fila, text="!",width=30,
                                        command=lambda t=tarea, r=es_rutina: self.mostrar_info_tarea(t,r))
            boton_info.pack(side="right", padx=10)
            
    def eliminar_tarea(self,idx,r,msg):
        if msg:
            confirmacion = messagebox.askyesno("Elimnar","¿Desea eliminar esta tarea?")
        else:
            confirmacion = True
        
        if confirmacion:
            tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
            if r:
                print(r)
                tareas_rutina.pop(idx)
            else:
                print(r)
                tareas.pop(idx)
        
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
            self.mostrar_tareas()

    def editar_tarea(self,idx,r,msg):
        confirmacion = messagebox.askyesno("Editar","¿Desea editar esta tarea?")
        if confirmacion:
            self.eliminar_tarea(idx,r,msg)
            VentanaAnadirTareas()
        
        self.mostrar_tareas()

    def mostrar_info_tarea(self, t, r):
        texto_info = (
            f"📅 Creada: {t.fecha_creacion}\n"
            f"📝 Nombre: {t.nombre}\n"
            f"🏷️ Tipo: {t.tipo}\n"
            f"🔥 Prioridad: {t.prioridad}\n"
            f"📊 Estado: {t.estado}\n"
            f"⏰ Hora: {t.hora}"
        )
        
        if r:
            texto_info += f"\n🔥 Racha: {t.racha}"
            # Convertimos la lista de días ['lunes', 'martes'] en "lunes, martes"
            dias_str = ", ".join(t.dias)
            texto_info += f"\n🗓️ Días: {dias_str}"

        messagebox.showinfo(f"Detalles de {t.nombre}", texto_info)