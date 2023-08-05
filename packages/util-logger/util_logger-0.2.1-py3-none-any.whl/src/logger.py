import logging
import traceback
from termcolor import colored


class ColoredFormatter(logging.Formatter):
    LEVEL_COLORS = {
        "DEBUG": "blue",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "magenta",
    }

    def format(self, record):
        message = super().format(record)
        color = self.LEVEL_COLORS.get(record.levelname, "white")
        return colored(message, color)


class Logger:
    def __init__(self, name, level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        formatter = ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log_message(
        self, message, log_method, name=None, exc_info=None, show_fileline=False
    ):
        if name:
            message = f"{name}: {message}"

        if show_fileline:
            frame = traceback.extract_stack()[-3]
            filename = frame.filename
            lineno = frame.lineno
            message = f"{message} (File: {filename}, Line: {lineno})"

        log_method(message, exc_info=exc_info)

    def debug(self, message, name=None):
        self.log_message(message, self.logger.debug, name)

    def info(self, message, name=None):
        self.log_message(message, self.logger.info, name)

    def warning(self, message, name=None, **kwargs):
        show_fileline = kwargs.get("exc_info", False)
        self.log_message(
            message, self.logger.warning, name, show_fileline=show_fileline, **kwargs
        )

    def error(self, message, name=None, **kwargs):
        show_fileline = kwargs.get("exc_info", False)
        self.log_message(
            message, self.logger.error, name, show_fileline=show_fileline, **kwargs
        )

    def critical(self, message, name=None, **kwargs):
        show_fileline = kwargs.get("exc_info", False)
        self.log_message(
            message, self.logger.critical, name, show_fileline=show_fileline, **kwargs
        )


def main():
    logs = Logger("TestLogger")
    logs.debug("Debug message")

    logs.info("Info message")
    logs.info("Info message", "TestName")


if __name__ == "__main__":
    main()
