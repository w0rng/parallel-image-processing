def show_pixel_color(r, g, b, color: int) -> tuple[int, int, int]:
    """Отбрасывает все каналы, кроме указанного"""
    if color == 0:
        return r, 0, 0
    elif color == 1:
        return 0, g, 0
    elif color == 2:
        return 0, 0, b
    else:
        raise ValueError("Неверный номер канала")


def row_show_pixel_color(
    row: list[tuple[int, int, int]], color: int
) -> list[tuple[int, int, int]]:
    """Отбрасывает все каналы, кроме указанного"""
    return list(map(lambda pixel: show_pixel_color(*pixel, color), row))


def red_channel(row: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    return row_show_pixel_color(row, 0)


def green_channel(row: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    return row_show_pixel_color(row, 1)


def blue_channel(row: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    return row_show_pixel_color(row, 2)
