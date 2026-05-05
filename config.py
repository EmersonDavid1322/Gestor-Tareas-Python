import requests
from storage import guardar_datos, cargar_datos
import customtkinter as ctk
import tkinter.messagebox as messagebox
tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VentanaConfiguraciones(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Configuraciones")
        self.geometry("750x750")

        #TITULO
        self.titulo = ctk.CTkLabel(self, text="Configuraciones", font=("Roboto", 20,"bold"))
        self.titulo.pack(pady=20)

        #mostrasr información
        self.lbl_info_webhook = ctk.CTkButton(self,text=f"¿Desea ver su informacion actual?",command=self.mostrar_info)
        self.lbl_info_webhook.pack(pady=10)

        #configurar web_H
        self.lbl_webhook = ctk.CTkLabel(self, text="Introduze tu WEBHOOK")
        self.lbl_webhook.pack(pady=10)
        self.entrada_webhook = ctk.CTkEntry(self, placeholder_text= "webhook...", placeholder_text_color="grey",width=300)
        self.entrada_webhook.pack(pady=10)
        self.btn_confirmar = ctk.CTkButton(self, text="Confirmar", command=self.web_h)
        self.btn_confirmar.pack(pady=10)

        #configurar token/canal
        self.lbl_token = ctk.CTkLabel(self, text="Introduze los datos del bot (Canal de chat/token del bot)")
        self.lbl_token.pack(pady=10)
        self.entrada_token = ctk.CTkEntry(self, placeholder_text= "Token...", placeholder_text_color="grey",width=300)
        self.entrada_token.pack(pady=10)
        self.entrada_canal = ctk.CTkEntry(self, placeholder_text= "canal...", placeholder_text_color="grey",width=300)
        self.entrada_canal.pack(pady=10)
        self.btn_token = ctk.CTkButton(self, text="Confirmar", command=self.token_bot_discord)
        self.btn_token.pack(pady=10)

        #configurar frases
        self.lbl_frases = ctk.CTkLabel(self,text="Activar/Desacivar el envio de frases")
        self.lbl_frases.pack(pady=10)
        self.switch_frases = ctk.CTkSwitch(self, text="Frases", progress_color="green", command=self.opcion_frase)
        self.switch_frases.pack(pady=10)

        #agregar frases
        self.lbl_ed_fra = ctk.CTkLabel(self,text="Añadir frases")
        self.lbl_ed_fra.pack(pady=10)
        self.entrada_frase = ctk.CTkEntry(self, placeholder_text="Frase",placeholder_text_color="grey")
        self.entrada_frase.pack(pady=10)
        self.btn_token = ctk.CTkButton(self, text="Confirmar", command=self.agregar_frase_nueva)
        self.btn_token.pack(pady=10)
        self.msg_frases = ctk.CTkLabel(self,text="",text_color="green")
        self.msg_frases.pack(pady=10)


    def mostrar_info(self):
        self.geometry("750x1000")
        tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
        self.pestañas = ctk.CTkTabview(self)
        self.pestañas.pack(expand=True, fill="both", padx=10, pady=10)

        self.pestañas.add("Información")
        self.pestañas.add("Frases")

        self.label_webhook = ctk.CTkLabel(self.pestañas.tab("Información"), text=f"Su WeebHook actual es: {webhook}",font=("Roboto", 9,"bold"))
        self.label_webhook.pack(pady=10)
        self.label_token = ctk.CTkLabel(self.pestañas.tab("Información"), text=f"Su token actual es: {token}",font=("Roboto", 9,"bold"))
        self.label_token.pack(pady=10)
        self.label_canal = ctk.CTkLabel(self.pestañas.tab("Información"), text=f"Su token actual es: {canal}",font=("Roboto", 9,"bold"))
        self.label_canal.pack(pady=10)

        frame_scroll = ctk.CTkScrollableFrame(self.pestañas.tab("Frases"), width=500, height=300)
        frame_scroll.pack(padx=10, pady=10, fill="both", expand=True)

        for frase in lista_frases:
            lbl = ctk.CTkLabel(frame_scroll, text=f"• {frase}", wraplength=400, justify="left")
            lbl.pack(pady=2, anchor="w")


    def web_h(self):
        tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()

        try:
            webhook = self.entrada_webhook.get()
            respuesta = messagebox.askyesno("Configuraciones","¿Desea probar el webhook?",parent=self)
            messagebox.showinfo("Configuraciones","Su WEBHOOK a sido agregado exitosamente",parent=self)
            if respuesta:
                requests.post(webhook, json={"content": "Su WebHook funciona correctamente"})
                messagebox.showinfo("Configuraciones","Se ha enviado un emnsaje de prueba a su WEBHOOK",parent=self)

        except requests.exceptions.MissingSchema:
            messagebox.showerror("Configuraciones","❌ URL inválida. Falta https://",parent=self)

        except requests.exceptions.InvalidURL:
            messagebox.showerror("Configuraciones","❌ URL inválida.",parent=self)

        except requests.exceptions.ConnectionError:
            messagebox.showerror("Configuraciones","❌ No se pudo conectar al weebhook.",parent=self)

        except requests.exceptions.Timeout:
            messagebox.showerror("Configuraciones","❌ Tiempo de espera agotado.",parent=self)

        except requests.exceptions.RequestException:
            messagebox.showerror("Configuraciones","❌ Error al enviar la prueba.",parent=self)

        guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
        return webhook


    def token_bot_discord(self):
        tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
        limpio_token = self.entrada_token.get().strip()
        limpio_canal = self.entrada_canal.get().strip()

        if token == "" and canal == "":
            token = limpio_token
            canal = limpio_canal
            validacion = limpio_canal.isdigit()
            if validacion:
                guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
                messagebox.showinfo("Configuraciones","Se a añadido correctamente",parent=self)
            else:
                messagebox.showerror("Configuraciones","'Canal' no debe tener letras, solo digitos",parent=self)
                return

        else:
            confirmacion = messagebox.askyesno("Configuraciones",f"Su token actualmente es {token} \nY su id canal actual es {canal} \n ¿Desea editarlo? ", parent=self)
            if confirmacion:
                validacion = limpio_canal.isdigit()
                if validacion:
                    token = limpio_token
                    canal = limpio_canal
                    guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
                    messagebox.showinfo("Configuraciones","Se a añadido correctamente",parent=self)
                else:
                    messagebox.showerror("Configuraciones","'Canal' no debe tener letras, solo digitos",parent=self)
                    return

    def opcion_frase(self):
        tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()

        estado = self.switch_frases.get()

        if estado == 1:
            usar_frase = True
            self.switch_frases.select()
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
        else:
            usar_frase = False
            self.switch_frases.deselect()
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)

    def agregar_frase_nueva(self):
        nueva_frase = self.entrada_frase.get()
        
        if nueva_frase.strip():
            lista_frases.append(nueva_frase)
            
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)

            
            self.msg_frases.configure(text=f"Frase guardada correctamente. Ahora tienes {len(lista_frases)} frases.")
        else:
            messagebox.showerror("Configuraciones","No puedes guardar una frase vacía.",parent=self)
