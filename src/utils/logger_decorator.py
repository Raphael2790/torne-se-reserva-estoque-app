from functools import wraps
from utils.app_logger import AppLogger


def log_execution(logger: AppLogger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Iniciando execução da função '{func.__name__}'")
            try:
                resultado = func(*args, **kwargs)
                logger.info(f"Execução bem-sucedida da função '{func.__name__}'")
                return resultado
            except Exception as e:
                logger.error(f"Erro na execução da função '{func.__name__}'", {"exception": str(e)})
                raise  # relança exceção após logar
        return wrapper
    return decorator
