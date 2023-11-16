from copy import deepcopy

from image import Image


def dilation(image: Image, mask: list[list[bool]]) -> Image:
    return _generic_dilation_erosion(
        image,
        mask,
        initial_value=0,
        swap_condition_func=lambda old_value, new_value: new_value > old_value
    )


def erosion(image: Image, mask: list[list[bool]]) -> Image:
    return _generic_dilation_erosion(
        image,
        mask,
        initial_value=255,
        swap_condition_func=lambda old_value, new_value: new_value < old_value
    )


def _generic_dilation_erosion(
        image: Image,
        mask: list[list[bool]],
        initial_value: int, # либо 0 (в случае расширения) либо 255 (в случае сужения)
        swap_condition_func # функция с 2 аргументами (old_value, new_value), возвращает подходит ли новое значение
) -> Image:
    if image.mode != "grayscale":
        return image

    width, height = image.size
    mask_half_height = len(mask) // 2
    mask_half_width = len(mask[0]) // 2

    new_image = deepcopy(image)

    for y in range(height):
        for x in range(width):

            def find_value() -> int:
                value = initial_value
                for dy in range(-mask_half_height, mask_half_height + 1):
                    for dx in range(-mask_half_width, mask_half_width + 1):
                        curr_y = y + dy
                        curr_x = x + dx
                        if not (0 <= curr_y < height and 0 <= curr_x < width):
                            continue

                        # тут будут приходить значения (-2 -1 0 1 2), а нам надо обращаться к матрице
                        # т е преобразовать в (0 1 2 3 4 5)
                        mask_y = dy + mask_half_height
                        mask_x = dx + mask_half_width

                        if not mask[mask_y][mask_x]:
                            continue

                        curr_value = image.pixels[curr_y][curr_x][0]
                        if swap_condition_func(value, curr_value):
                            value = curr_value
                            # если убрать эту строку (преждевременный выход из 2 циклов)
                            # то это уже будет "классический вариант"
                            # а сейчас это "ускоренный вариант"!!!!!
                            return value
                return value

            res_value = find_value()
            new_image.pixels[y][x] = (res_value, res_value, res_value)

    return new_image
