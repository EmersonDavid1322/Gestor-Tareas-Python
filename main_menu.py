from funciones import *
from config import *
from storage import cargar_datos
from sub_menus import *

tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()

def menu_principal():
    while True:
        opcion = menu_f()
        
        if opcion == 1:
            gestor_tareas()
        elif opcion == 2:
            historial_f(historial)
        elif opcion == 3:
            estadisticas(tareas)
        elif opcion == 4:
            configuracion()
        elif opcion == 5:
            confirmacion = input("Ha seleccionado salir, ¿esta seguro? (S/N): ").lower()
            if confirmacion in ("s","si"):
                print("Ha salido")
                break
            else:
                print("Volviendo al menu")
        else:
            print("Seleccione una opción valida")

if __name__ == "__main__":
    menu_principal()