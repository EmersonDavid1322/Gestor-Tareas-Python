# Gestor de Tareas (Python)

Gestor de Tareas es una aplicación de escritorio en Python para crear y gestionar tareas puntuales y rutinas/hábitos. Incluye persistencia local con SQLite, interfaz gráfica con customtkinter, notificaciones locales y envío de recordatorios a través de un webhook o un bot de Discord.

Características principales
- Tareas únicas y rutinas (hábitos) con prioridad, hora y estado.
- Registro de historial y papelera (recuperación de tareas eliminadas).
- Estadísticas simples (completadas / pendientes, barra de progreso de puntos).
- Notificaciones locales (sonidos) y envío de recordatorios a Discord vía webhook o bot.
- Scripts para instalación y despliegue como servicio (installer.sh / systemd.sh).

Stack
- Lenguaje: Python
- GUI: customtkinter (Tkinter)
- Persistencia: sqlite3 (archivos en data/)
- Dependencias destacadas: customtkinter, discord.py, requests, plyer

Requisitos
- Python 3.8+ recomendado
- pip
- Sistema con soporte para GUI (Windows / Linux / macOS)

Instalación rápida
```bash
git clone https://github.com/EmersonDavid1322/Gestor-Tareas-Python.git
cd Gestor-Tareas-Python
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Ejecutar la aplicación
```bash
python interfaz.py
```
Esto abre la ventana principal (Menu) donde puedes gestionar tareas, ver historial, registros y configuraciones.

Configuración
- Webhook de Discord: Abre Configuraciones → introduce tu webhook y pruébalo. El webhook se usa para enviar recordatorios.
- Bot de Discord (opcional): Puedes introducir token y ID de canal si quieres usar integración mediante bot.
- Frases motivacionales: Puedes activar/desactivar y añadir frases desde la ventana de Configuraciones.

Archivos importantes
- interfaz.py — Punto de entrada y ventanas principales (Menu, Historial, Registro, Estadísticas).
- interfaz_gestor.py — Ventanas y lógica para crear/editar/borrar tareas y rutinas.
- base_sql.py — CRUD y manejo de las bases de datos SQLite (data/gestor.db, historial.db, registro.db).
- storage.py — Guardado y carga de configuraciones (puntos, webhook, frases, token, canal).
- Recordatorio.py — Script que revisa rutinas según la hora y envía notificaciones al webhook.
- discord_bot.py — Implementación del cliente de Discord (si se usa el bot en lugar del webhook).
- notificaciones.py — Manejo de notificaciones locales (sonidos/plyer).
- installer.sh, systemd.sh — Scripts de utilidad para instalación/despliegue como servicio.
- requirements.txt — Dependencias pip.
- noti/ — Recursos (ej. archivo mp3 para notificación).

Ejecución como servicio (Linux)
- Revisa systemd.sh e installer.sh antes de usarlos (adapta rutas y usuarios).
- Los scripts intentan copiar archivos y crear unidades systemd; ejecútalos con sudo cuando estés listo:

```bash
sudo bash installer.sh
# o
sudo bash systemd.sh
```

Buenas prácticas y notas
- Nunca subas tokens o datos sensibles al repositorio.
- Si compartes tu proyecto, elimina o enmascara cualquier token de Discord o webhook de ejemplo en archivos de configuración.
- Si la aplicación se congela al abrir la GUI, asegúrate de que todas las dependencias estén instaladas y que el intérprete de Python tenga permisos de escritura en la carpeta del repositorio (se crean archivos en data/).

Sugerencias futuras / mejoras
- Añadir tests unitarios para las funciones de base_sql.py.
- Refactorizar las clases en clases.py para usar keyword args y facilitar la creación desde filas de DB.
- Mejorar validaciones y manejo de errores (por ejemplo, comprobar esquemas para datos cargados desde JSON/DB).
- Añadir un instalador multiplataforma o empaquetado (PyInstaller) para distribuir binarios.

Contribuir
Si quieres mejorar el proyecto, puedes abrir issues o pull requests. Un buen primer PR sería añadir un README (este archivo), un archivo LICENSE (por ejemplo MIT) y mejorar las instrucciones de instalación.

Licencia
- Recomendado: agregar un archivo LICENSE (por ejemplo MIT) si deseas que otros usen o contribuyan libremente.

Contacto
- Autor: EmersonDavid1322 (repositorio original)

---

Si quieres, puedo:
- Añadir imágenes/capturas de pantalla al README.
- Crear un archivo LICENSE (MIT) y añadirlo al repo.
- Refactorizar pequeñas partes del código (por ejemplo, clases.py o crear tests).
