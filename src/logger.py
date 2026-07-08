from loguru import logger
import sys
import os

if getattr(sys, 'frozen', False):
    ruta_base = os.path.dirname(sys.executable)
    CARPETA_LOGS = os.path.join(ruta_base, "logs")
else:
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    CARPETA_LOGS = os.path.join(os.path.dirname(ruta_base), "logs")
os.makedirs(CARPETA_LOGS, exist_ok=True)

logs = os.path.join(CARPETA_LOGS, "logs_gestor.log")

logger.remove()

logger.add(
    sys.stdout, 
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    colorize=True
)

logger.add(
    logs,     
    rotation="10 MB",           
    retention="5 days",         
    compression="zip",          
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
)

def crear_log(tipo,mensaje):
    if tipo == "INFO":
        logger.info(mensaje)
    elif tipo == "WARNING":
        logger.warning(mensaje)
    elif tipo == "ERROR":
        logger.error(mensaje)
    else:
        logger.critical(mensaje)
