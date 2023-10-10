from image import Image
from random import sample


def random_coordinates_set_by_percent(image: Image, percent: float) -> set[tuple[int, int]]:
    assert 0 <= percent <= 1, "percent must be [0, 1]"

    width, height = image.size
    pixels_count = width * height
    needed_pixels_count = int(pixels_count * percent)

    return set(sample([(i, j) for i in range(width) for j in range(height)], k=needed_pixels_count))


if __name__ == '__main__':
    image = Image.load('../../assets/example.jpeg')
    res = random_coordinates_set_by_percent(image, 0.5)
    print(res)
    print(image.size, image.size[0] * image.size[1])