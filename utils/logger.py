import logging

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(message)s')

def log(message, level='info'):
    levels = {
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
        'red': logging.ERROR  # Custom level for 'red' (could be used for specific logging formatting)
    }
    log_level = levels.get(level, logging.INFO)
    logging.log(log_level, message)

def log_over(message):
    """
    Print a message and overwrite it in the same line.
    """
    print(message, end='\r')
