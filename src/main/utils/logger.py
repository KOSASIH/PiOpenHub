import logging
import os
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, name, log_file='app.log', level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create a directory for logs if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Create a file handler that logs messages to a file
        file_handler = RotatingFileHandler(
            os.path.join('logs', log_file), maxBytes=10 * 1024 * 1024, backupCount=5
        )
        file_handler.setLevel(level)

        # Create a console handler for logging to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Create a formatter and set it for both handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

# Example usage
if __name__ == "__main__":
    log = Logger(__name__)
    log.info("This is an info message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
    log.critical("This is a critical message.")
