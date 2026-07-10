import customtkinter as ctk
import tkinter.messagebox as messagebox
from src.base_sql import limpiar_tareas
from src.servicios import tarea_existe ,agregar_tarea, completar, fallar_tarea, eliminar_tarea, filtro_todas, filtro_hoy, filtro_pendientes_hoy
print("Version 1.6 Interfaz")

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
        self.btn_crear = ctk.CTkButton(self, text="Añadir Tarea", command= VentanaAnadirTareas)
        self.btn_crear.pack(pady=20)

        #ver tareas/editar/eliminar/completar/filtros
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

        self.dias_disponibles = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]
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
        
        existe = tarea_existe(self.nombre)
        continuar = True

        if existe:
            continuar = messagebox.askyesno("Duplicada", "Ya existe una tarea con este nombre\n¿Desea agregarla igualmente?")

        if continuar:
            resultado = agregar_tarea(self.tipo,self.nombre, self.prioridad, self.tiempo, self.dias)
            if resultado.exito:
                messagebox.showinfo("Agregar Tarea", resultado.mensaje)
        self.destroy()

class VentanaTareas(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Marcar Tareas")
        self.geometry("800x600")

        frame_btn_up = ctk.CTkFrame(self,border_width=2, border_color="#1f538d", width=50, height=50)
        frame_btn_up.pack_propagate(False)
        frame_btn_up.pack(fill="x", pady=5, padx=5)

        self.btn_limpiar = ctk.CTkButton(frame_btn_up, text="Limpiar", width=30, fg_color="#2C2697",
                                            command= lambda: self.actualizar_limpieza())
        self.btn_limpiar.pack(side="left",padx=10)

        self.btn_ord_hoy = ctk.CTkButton(frame_btn_up, text="Habitos Hoy", width=30, fg_color="#2C2697",
                                        command= lambda: self.mostrar_tareas(filtro=filtro_hoy))
        self.btn_ord_hoy.pack(side="right", padx=10)

        self.btn_pend_hoy = ctk.CTkButton(frame_btn_up, text="Pendientes hoy", width=30, fg_color="#2C2697",
                                        command= lambda: self.mostrar_tareas(filtro=filtro_pendientes_hoy))
        self.btn_pend_hoy.pack(side="right", padx=10)

        self.btn_ord_todo = ctk.CTkButton(frame_btn_up, text="Todas las tareas", width=30, fg_color="#2C2697",
                                        command= lambda: self.mostrar_tareas(filtro=filtro_todas))
        self.btn_ord_todo.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.scroll_tareas = ctk.CTkScrollableFrame(self, label_text="Lista de Actividades")
        self.scroll_tareas.pack(padx=20, pady=20, fill="both", expand=True)

        self.mostrar_tareas(filtro=filtro_pendientes_hoy)

    def mostrar_tareas(self, filtro):
        for widget in self.scroll_tareas.winfo_children():
            widget.destroy()

        tareas, tareas_rutina = filtro()

        if tareas is not None:
            self.creacion_seccion("-----Tareas-----", tareas, es_rutina=False)
        if tareas_rutina is not None:
            self.creacion_seccion("-----Habitos-----",tareas_rutina, es_rutina=True)

    def creacion_seccion(self,titulo,lista,es_rutina):
        ctk.CTkLabel(self.scroll_tareas,text=titulo,font=("Roboto", 16, "bold")).pack(pady=10)

        for i, tarea in enumerate(lista):
            color = "#1f538d" if not es_rutina else "#2d7d52"
            fila = ctk.CTkFrame(self.scroll_tareas,border_width=2, border_color=color)
            fila.pack(fill="x", pady=5, padx=5)

            #informacion de la tarea
            info_ta = tarea
            info_lbl = ctk.CTkLabel(fila, text=info_ta, font=("Roboto", 12))
            info_lbl.pack(side="left", padx=15, pady=10)

            #eliminar tarea
            boton_elimnar = ctk.CTkButton(fila,text="x", width=30, fg_color="#922b21", hover_color="#641e16",
                                            command=lambda id_tarea = tarea.id,tipo=tarea.tipo : self.actualizar_eliminar(id_tarea,tipo))
            boton_elimnar.pack(side="right", padx=10)

            #editar tarea
            boton_editar = ctk.CTkButton(fila,text="Editar", width=50,
                                        command=lambda id_tarea = tarea.id, r=es_rutina, idx=i,msg=False, tipo=tarea.tipo: self.editar_tarea(id_tarea,r,msg,tipo))
            boton_editar.pack(side="right", padx=10)

            #completar
            boton_compl= ctk.CTkButton(fila, text="Completar",width=30,fg_color="#2B2FA5",
                                        command=lambda id_tarea=tarea.id, tipo=tarea.tipo: self.actualizar_completar(id_tarea,tipo))
            boton_compl.pack(side="right", padx=10)

            #Fallar
            if tarea.tipo == "Rutina":
                boton_elimnar = ctk.CTkButton(fila,text="Falle", width=30, fg_color="#922b21", hover_color="#641e16",
                                                command=lambda id_tarea = tarea.id, tipo=tarea.tipo : self.actualizar_fallar(id_tarea,tipo))
                boton_elimnar.pack(side="right", padx=10)
            
            #mostar informacion completa de la tarea
            boton_info = ctk.CTkButton(fila, text="!",width=30,fg_color="#29A55B",
                                        command=lambda tarea_i=tarea: self.mostrar_info_tarea(tarea_i))
            boton_info.pack(side="right", padx=10)
    
    def mostrar_info_tarea(self,tarea):
        texto = tarea.info_completa()
        messagebox.showinfo(f"Detalles de {tarea.nombre}", texto)

    def actualizar_limpieza(self):
        limpiar_tareas()
        self.mostrar_tareas(filtro=filtro_pendientes_hoy)

    def actualizar_fallar(self,id_tarea,tipo):
        resultado = fallar_tarea(id_tarea,tipo)
        if resultado.exito:
            messagebox.showinfo("Fallar", resultado.mensaje)
            self.mostrar_tareas(filtro=filtro_pendientes_hoy)
        else:
            messagebox.showwarning("Error Fallar", resultado.mensaje)
    
    def actualizar_completar(self,id_tarea,tipo):
        resultado = completar(id_tarea,tipo)
        if resultado.exito:
            messagebox.showinfo("Completar", resultado.mensaje)
            if resultado.mensaje_racha is not None: 
                messagebox.showinfo("Racha", resultado.mensaje_racha)
            self.mostrar_tareas(filtro=filtro_pendientes_hoy)
        else:
            messagebox.showwarning("Error completar", resultado.mensaje)
    
    def actualizar_eliminar(self,id_tarea,tipo):
        confirmacion = messagebox.askyesno("Eliminar", "¿Desea eliminar esta tarea?")

        if confirmacion:
            resultado = eliminar_tarea(id_tarea,tipo)
            if resultado.exito:
                messagebox.showinfo("Eliminar", resultado.mensaje)
                self.mostrar_tareas(filtro=filtro_pendientes_hoy)
            else:
                messagebox.showwarning("Eliminar", resultado.mensaje)

    def editar_tarea(self,id_tarea,tipo):
        confirmacion = messagebox.askyesno("Editar","¿Desea editar esta tarea?")
        if confirmacion:
            eliminar_tarea(id_tarea,tipo)
            VentanaAnadirTareas()
            self.mostrar_tareas(filtro=filtro_pendientes_hoy)