def to_yuv(r, g, b) -> tuple[int, int, int]:
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
    cr = 0.5 * r - 0.4187 * g - 0.0813 * b + 128

    return int(y), int(cb), int(cr)


def row_to_yuv(row: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    return list(map(lambda pixel: to_yuv(*pixel), row))
