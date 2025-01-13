from constants.log_levels import LogLevel
import logging

def log_in_console(msg: str, level: LogLevel):
    logging.basicConfig(level=logging.INFO)
    if level == LogLevel.DEBUG:
        logging.debug(msg)
    elif level == LogLevel.INFO:
        logging.info(msg)
    elif level == LogLevel.WARNING:
        logging.warning(msg)
    elif level == LogLevel.ERROR:
        logging.error(msg)
    elif level == LogLevel.CRITICAL:
        logging.critical(msg)
        
def get_user_response(msg: str) -> bool:
    return input(msg).lower().strip() == 'yes'
        