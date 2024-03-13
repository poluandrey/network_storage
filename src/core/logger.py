import logging.config
from src.core.config import settings

logging.config.fileConfig(settings.LOGGER_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger('app')
