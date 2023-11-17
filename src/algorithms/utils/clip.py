def clip(num: float, min: float, max: float) -> float:
    if num < min:
        return min
    if num > max:
        return max
    return num
