from functools import wraps
import time


def timer_execution():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            resultado = func(*args, **kwargs)
            end_time = time.time()
            print(f"Tempo de execução da função {func.__name__}: {end_time - start_time} segundos")
            return resultado
        return wrapper
    return decorator
