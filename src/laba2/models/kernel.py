from dataclasses import dataclass


@dataclass
class Kernel:
    coefficients: list[list[float]]

    def __init__(self, height: int, width: int, coef: int):
        self.coefficients = [[1 / coef] * width] * height

    @property
    def size(self) -> tuple[int, int]:
        return len(self.coefficients[0]), len(self.coefficients)
