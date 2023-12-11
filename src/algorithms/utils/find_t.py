def find_t(array: list[int]) -> int:
    # ШАГ 1: Выбрать порог T равным середине диапазона яркостей
    min_intensity = 0
    max_intensity = len(array) - 1
    threshold = int((min_intensity + max_intensity) // 2)

    while True:
        # ШАГ 2: Вычислить среднюю яркость для двух групп пикселей (< T и > T)
        m1 = sum(i * array[i] for i in range(threshold)) / sum(array[:threshold]) if sum(
            array[:threshold]) > 0 else 0
        m2 = sum(i * array[i] for i in range(threshold, len(array))) / sum(array[threshold:]) if sum(
            array[threshold:]) > 0 else 0

        # ШАГ 3: Пересчитать порог T = (m1 + m2) / 2
        new_threshold = int((m1 + m2) // 2)

        # ШАГ 4: Проверить, изменился ли порог, если нет, то выйти из цикла
        if new_threshold == threshold:
            break

        threshold = new_threshold

    return threshold