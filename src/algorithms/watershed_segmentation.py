from collections import deque

import numpy as np


def watershed_segmentation(image, water_level):
    image = np.array(image)
    height, width, _ = image.shape

    markers = np.zeros((height, width), dtype=int)  # Изменение инициализации на нули
    visited = np.zeros((height, width), dtype=bool)

    queue = deque()

    def get_neighbors(y, x):
        neighbors = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        return [(ny, nx) for ny, nx in neighbors if 0 <= ny < height and 0 <= nx < width]

    intensity_map = {}
    for y in range(height):
        for x in range(width):
            intensity_val = sum(image[y][x])
            if intensity_val in intensity_map:
                intensity_map[intensity_val].append((y, x))
            else:
                intensity_map[intensity_val] = [(y, x)]

    label = 1  # Начинаем с 1, чтобы пиксели с меткой 0 были теми, что ниже уровня воды
    for intensity_val in sorted(intensity_map.keys()):
        if intensity_val < water_level:
            continue
        intensity_pixels = intensity_map[intensity_val]
        for pixel in intensity_pixels:
            y, x = pixel
            if not visited[y][x]:
                visited[y][x] = True
                markers[y][x] = label
                queue.append((y, x))

                while queue:
                    current_y, current_x = queue.popleft()
                    for ny, nx in get_neighbors(current_y, current_x):
                        if not visited[ny][nx] and sum(image[ny][nx]) >= water_level:
                            visited[ny][nx] = True
                            markers[ny][nx] = label
                            queue.append((ny, nx))
        label += 1

    return markers
