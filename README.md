# Gestor de Disciplina

Aplicación de escritorio para Linux que combina gestión de tareas, seguimiento de hábitos y notificaciones automáticas. Incluye integración con Discord para recibir recordatorios y estadísticas desde cualquier lugar.

## Características

### Gestión de Tareas
- Crea tareas únicas con nombre, prioridad y hora de recordatorio
- Crea rutinas/hábitos con días de la semana específicos
- Sistema de rachas para mantener la consistencia en los hábitos
- Sistema de puntos por completar tareas según su prioridad
- Papelera con opción de restaurar tareas eliminadas
- Búsqueda de tareas por nombre en tiempo real

### Notificaciones
- Daemon de notificaciones que corre en segundo plano con systemd
- Notificaciones del sistema con sonido personalizado
- Evaluación diaria a las 20:00 con resumen de tareas pendientes
- Frases motivadoras configurables que acompañan cada recordatorio

### Bot de Discord
- Consulta tus tareas desde Discord con `!tareas hoy` o `!tareas todas`
- Marca hábitos como completados con `!hecho [número]`
- Registra fallos de hábitos con `!fallo [número]`
- Consulta estadísticas con `!estadisticas`
- Muestra tu mejor racha activa con `!racha`
- Envía frases motivadoras aleatorias con `!frase`

### Historial y Estadísticas
- Historial completo de todas las acciones realizadas
- Registro detallado de hábitos completados y fallidos
- Estadísticas con porcentaje de completado y barra de progreso visual
- Sistema de rangos basado en puntos acumulados

### Configuración
- Webhook de Discord para alertas automáticas
- Token y canal del bot de Discord configurables
- Lista de frases motivadoras personalizable
- Activar o desactivar el envío de frases

## Tecnologías

- **Python** — Lenguaje principal
- **CustomTkinter** — Interfaz gráfica moderna
- **SQLite** — Persistencia de datos con tres bases de datos separadas
- **discord.py** — Bot de Discord
- **plyer** — Notificaciones del sistema
- **systemd** — Servicios en segundo plano
- **PyInstaller** — Compilación a ejecutable

## Arquitectura

```
└── Gestor-Tareas-Python
    ├── assets
    │   ├── dota2-notification.mp3
    │   └── icono.png
    ├── scripts
    │   ├── installer.sh
    │   └── systemd.sh
    ├── src
    │   ├── base_sql.py
    │   ├── clases.py
    │   ├── config_logs.py
    │   ├── config.py
    │   ├── interfaz_gestor.py
    │   ├── recordatorio.py
    │   ├── servicios.py
    │   └── storage.py
    ├── .gitignore
    ├── discord_bot.py
    ├── interfaz.py
    ├── notificaciones.py
    ├── README.md
    └── requirements.txt
```

## Instalación

```bash
git clone https://github.com/EmersonDavid1322/Gestor-Tareas-Python
cd gestor-disciplina
bash scripts/installer.sh
```

El instalador compila los tres ejecutables con PyInstaller, los copia a `~/apps/gestor/` y configura los servicios de systemd automáticamente.

## Servicios en segundo plano

El proyecto instala dos servicios que arrancan con el sistema:

- **notificador** — Servicio de usuario que envía notificaciones del sistema
- **bot_disciplina** — Servicio del sistema que mantiene el bot de Discord activo

## Uso

Ejecuta la interfaz principal:

```bash
~/apps/gestor/GestorDisciplina
```

O accede desde Discord usando los comandos del bot mientras la interfaz corre en segundo plano.

## Base de datos

El proyecto usa tres bases de datos SQLite separadas:

- `gestor.db` — Tareas y rutinas activas
- `historial.db` — Historial de acciones y papelera
- `registro.db` — Registro de hábitos completados y fallidos
