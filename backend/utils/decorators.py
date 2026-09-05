import time

def log_function(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Running function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIME] {func.__name__} took {end-start:.4f} seconds")
        return result
    return wrapper