from image import Image

from algorithms.utils.safe_get import safe_get_from_matrix
from algorithms.utils.markers_to_image import markers_to_image


def regional_sprawl(image: Image, delta: int) -> Image:
    """
    Заметки со слов Зотина:
    - строим матрицу яркости (грейскейл) и по ней уже бегаем
    - строим матрицу коэффициентов
    - сравниваем с верхним и левым
    - Для каждой области храним количество элементов и сумма
    - инкрементить секторы
    - для каждого сектора маппим рандомный ргб цвет
    """

    if image.mode != 'grayscale':
        image = image.to_grayscale()

    width, height = image.size

    markers = [[0] * width for _ in range(height)]
    count_and_summ_by_markers: dict[int, tuple[int, float]] = dict()

    def update_count_and_summ_by_markers_if_needed(marker: int, pixel: int) -> bool:
        if (marker is None) or (marker not in count_and_summ_by_markers):
            return False
        count, summ = count_and_summ_by_markers[marker]
        average = summ / count
        if abs(pixel - average) > delta:
            return False
        count_and_summ_by_markers[marker] = (count + 1, summ + pixel)
        return True

    curr_marker = 0
    for y in range(height):
        for x in range(width):
            curr_p = image.pixels[y][x][0]

            top_marker = safe_get_from_matrix(markers, y - 1, x)
            was_updated_with_top_marker = update_count_and_summ_by_markers_if_needed(top_marker, curr_p)
            if was_updated_with_top_marker:
                markers[y][x] = top_marker
                continue

            left_marker = safe_get_from_matrix(markers, y, x - 1)
            was_updated_with_left_marker = update_count_and_summ_by_markers_if_needed(left_marker, curr_p)
            if was_updated_with_left_marker:
                markers[y][x] = left_marker
                continue

            curr_marker += 1
            markers[y][x] = curr_marker
            count_and_summ_by_markers[curr_marker] = (1, curr_p)

    return markers_to_image(markers)