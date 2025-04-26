import logging
import json


class AppLogger:
    def __init__(self, logger_name=__name__, level=logging.INFO):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level)

        # Formato do log estruturado como JSON
        log_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            json.dumps({
                "timestamp": "%(asctime)s",
                "level": "%(levelname)s",
                "message": "%(message)s",
                "function": "%(funcName)s",
                "file": "%(filename)s",
                "line": "%(lineno)d"
            })
        )
        log_handler.setFormatter(formatter)

        # Evita adicionar múltiplos handlers na Lambda ao reutilizar instâncias
        if not self.logger.handlers:
            self.logger.addHandler(log_handler)

    def info(self, message, extra=None):
        self.logger.info(self._format_message(message, extra))

    def warning(self, message, extra=None):
        self.logger.warning(self._format_message(message, extra))

    def error(self, message, extra=None):
        self.logger.error(self._format_message(message, extra))

    def debug(self, message, extra=None):
        self.logger.debug(self._format_message(message, extra))

    def critical(self, message, extra=None):
        self.logger.critical(self._format_message(message, extra))

    def _format_message(self, message, extra):
        if extra:
            return f"{message} | extra: {json.dumps(extra)}"
        return message


if __name__ == "__main__":
    logger = AppLogger(logger_name="MinhaLambda")

    logger.info("Lambda iniciada com sucesso")
    logger.warning("Valor inesperado recebido", {"valorRecebido": 123})
    logger.error("Falha ao acessar DynamoDB", {"idSku": "SKU12345"})
