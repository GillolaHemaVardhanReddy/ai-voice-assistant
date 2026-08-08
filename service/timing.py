import time


def timed(fxn):
    def func(*args, **kwargs):
        t0 = time.perf_counter()
        ans = fxn(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        print(f"Function {fxn.__name__} took {elapsed:.4f} seconds to execute.")
        return ans
    return func