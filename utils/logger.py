import logging
from logging.handlers import TimedRotatingFileHandler

# Configurar el logger principal
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Crear un logger específico para el framework
logger = logging.getLogger('trading_framework')
logger.setLevel(logging.DEBUG)

# Configurar un manejador para escribir logs en un archivo rotativo diariamente
file_handler = TimedRotatingFileHandler('trading_framework.log', when='midnight', interval=1, backupCount=7)  # Guarda una semana de logs
file_handler.setLevel(logging.DEBUG)

# Configurar un formateador para el archivo de logs
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Añadir el manejador al logger principal
logger.addHandler(file_handler)

# Ejemplo de uso del logger
logger.info('Logger configurado correctamente.')
