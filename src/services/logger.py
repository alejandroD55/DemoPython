import logging
import os

# Crea el directorio "logs" si no existe
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_filename = os.path.join(LOG_DIR, "app.log")
# Configura el logger

logging.basicConfig(
    filename =log_filename,
    filemode='a',
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
 
)


logger = logging.getLogger()
logger.handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]  

logger.debug("Logger configurado correctamente.")