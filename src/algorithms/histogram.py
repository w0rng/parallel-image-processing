from src.image import Image, pixel
from src.algorithms.utils.adjust_image_by_mode import adjust_image_by_mode
from src.utils import Pool


def calculate_texture_features(image: Image, window_size=3):
    if image.mode != 'grayscale':
        image.to_grayscale()

    width, height = image.size

    res = []
    for count in range(1, 5):
        with Pool("histogram", count) as pool:
            res = pool.map(
                _tmp_histogram_row,
                [(image, y, window_size)
                 for y in range(height)]
            )

    new_image = Image(pixels=res, mode='grayscale')
    adjust_image_by_mode(new_image)

    return new_image


def _tmp_histogram_row(args):
    return histogram_row(*args)


def histogram_row(image: Image, y: int, window_size: int) -> [pixel]:
    width, height = image.size

    row = []
    for x in range(width):
        # Calculate local neighborhood histogram
        histogram = [0] * 256
        for i in range(max(0, y - window_size // 2), min(height, y + window_size // 2 + 1)):
            for j in range(max(0, x - window_size // 2), min(width, x + window_size // 2 + 1)):
                pixel_value = image.pixels[i][j][0]
                histogram[pixel_value] += 1

        # Calculate probability histogram
        probability_histogram = [count / float(window_size ** 2) for count in histogram]

        # Calculate average brightness
        average_brightness = sum(value * prob for value, prob in enumerate(probability_histogram))

        # Calculate texture features (you can add more features based on your requirements)
        contrast = sum(((i - average_brightness) ** 2) * prob for i, prob in enumerate(probability_histogram))

        # Update texture feature map with the calculated feature
        row.append((contrast, contrast, contrast))

    return row
