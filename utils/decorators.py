import time
from functools import wraps
from typing import Callable, Any

def log_execution_time(func: Callable) -> Callable:
  @wraps(func)
  def wrapper(*args: Any, **kwargs: Any) -> Any:
    start_time: float = time.perf_counter()

    try: return func(*args, **kwargs)

    finally:
      end_time: float = time.perf_counter()
      duration: float = end_time - start_time

      print(
        f"{func.__name__} completed in "
        f"{duration:.4f} seconds"
      )
  
  return wrapper