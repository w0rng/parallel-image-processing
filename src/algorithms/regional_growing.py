from dataclasses import dataclass

from image import Image

from algorithms.utils.safe_get import safe_get_from_matrix
from algorithms.utils.markers_to_image import markers_to_image


def regional_growing(image: Image, delta: int) -> Image:
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
    state_by_markers: dict[int, MarkerState] = dict()

    curr_marker = 0
    for y in range(height):
        print(y)
        for x in range(width):
            curr_p = image.pixels[y][x][0]

            top_marker = safe_get_from_matrix(markers, y - 1, x)
            left_marker = safe_get_from_matrix(markers, y, x - 1)

            left_marker_state: MarkerState | None = state_by_markers.get(left_marker)
            top_marker_state: MarkerState | None = state_by_markers.get(top_marker)

            left_diff = None
            top_diff = None
            if left_marker_state is not None:
                left_diff = abs(left_marker_state.average - curr_p)
            if top_marker_state is not None:
                top_diff = abs(top_marker_state.average - curr_p)

            def optional_greater(lhs, rhs) -> bool:
                if not lhs:
                    return True
                return lhs > rhs

            # Если не подходит ни к одной области, то создаем новую область
            if optional_greater(left_diff, delta) and optional_greater(top_diff, delta):
                curr_marker += 1
                markers[y][x] = curr_marker
                state_by_markers[curr_marker] = MarkerState(1, curr_p)
                continue

            # XOR
            # Если подходит только к одной области, то добавляем к ней
            if (left_diff is not None and left_diff <= delta) and (top_diff is None or top_diff > delta):
                left_marker_state.count += 1
                left_marker_state.summ += curr_p
                state_by_markers[left_marker] = left_marker_state
                markers[y][x] = left_marker
                continue

            if (top_diff is not None and top_diff <= delta) and (left_diff is None or left_diff > delta):
                top_marker_state.count += 1
                top_marker_state.summ += curr_p
                state_by_markers[top_marker] = top_marker_state
                markers[y][x] = top_marker
                continue

            # <= and <= (последний кейс)

            # Если области отличаются меньше чем на дельту, то сливаем их
            if abs(left_marker_state.average - top_marker_state.average) <= delta:
                # left_marker меняет все маркеры top_marker на свои
                for m_y in range(y + 1):
                    for m_x in range(x + 1):
                        if markers[m_y][m_x] == top_marker:
                            markers[m_y][m_x] = left_marker
                left_marker_state.count += top_marker_state.count
                left_marker_state.summ += top_marker_state.summ
                state_by_markers[left_marker] = left_marker_state
                markers[y][x] = left_marker
                continue

            if left_diff < top_diff:
                left_marker_state.count += 1
                left_marker_state.summ += curr_p
                state_by_markers[left_marker] = left_marker_state
                markers[y][x] = left_marker
            else:
                top_marker_state.count += 1
                top_marker_state.summ += curr_p
                state_by_markers[top_marker] = top_marker_state
                markers[y][x] = top_marker

    return markers_to_image(markers)

@dataclass
class MarkerState:
    count: int
    summ: float

    @property
    def average(self) -> float:
        return self.summ / self.count
