from multiprocessing.pool import Pool as _Pool
from time import time


class Pool(_Pool):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._start = 0.0
        self._end = 0.0
        self.name = name

    def map(self, *args, **kwargs):
        self._start = time()
        result = super().map(*args, **kwargs)
        self._end = time()
        return result

    def __exit__(self, *args, **kwargs):
        with open(f"timings_{self.name}.csv", "a") as f:
            f.write(f"{self._processes};{self._end - self._start}\n".replace(".", ","))
        super().__exit__(*args, **kwargs)
