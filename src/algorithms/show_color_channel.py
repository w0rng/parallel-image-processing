def pixel_color(ch1, ch2, ch3, select_chans: list[int]) -> tuple[int, int, int]:
    return (
        ch1 if 0 in select_chans else 0,
        ch2 if 1 in select_chans else 0,
        ch3 if 2 in select_chans else 0,
    )

def row_pixel_color(
    row: list[tuple[int, int, int]], select_chans: list[int]
) -> list[tuple[int, int, int]]:
    """Отбрасывает все каналы, кроме указанного"""
    return list(map(lambda pixel: pixel_color(*pixel, select_chans), row))

def matrix_pixel_color(
    matrix: list[list[tuple[int, int, int]]],
    select_chans: list[int]
) -> list[list[tuple[int, int, int]]]:
    return list(map(lambda row: row_pixel_color(row, select_chans), matrix))