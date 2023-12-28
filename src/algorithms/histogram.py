from src.image import Image, pixel
from src.algorithms.utils.adjust_image_by_mode import adjust_image_by_mode
from src.utils import Pool
import math


def calculate_texture_features(image: Image, window_size=5):
    if image.mode != 'grayscale':
        image.to_grayscale()

    width, height = image.size

    res_contrast = []
    for count in range(4, 5):
        with Pool("histogram_contrast", count) as pool:
            res_contrast = pool.map(
                _tmp_contrast_histogram_row,
                [(image, y, window_size)
                 for y in range(height)]
            )

    res_uniformity = []
    for count in range(4, 5):
        with Pool("histogram_uniformity", count) as pool:
            res_uniformity = pool.map(
                _tmp_uniformity_histogram_row,
                [(image, y, window_size)
                 for y in range(height)]
            )

    res_entropy = []
    for count in range(4, 5):
        with Pool("histogram_entropy", count) as pool:
            res_entropy = pool.map(
                _tmp_entropy_histogram_row,
                [(image, y, window_size)
                 for y in range(height)]
            )

    res_energy = []
    for count in range(4, 5):
        with Pool("histogram_energy", count) as pool:
            res_energy = pool.map(
                _tmp_energy_histogram_row,
                [(image, y, window_size)
                 for y in range(height)]
            )

    contrast_map = Image(pixels=res_contrast, mode='grayscale')
    uniformity_map = Image(pixels=res_uniformity, mode='grayscale')
    entropy_map = Image(pixels=res_entropy, mode='grayscale')
    energy_map = Image(pixels=res_energy, mode='grayscale')

    print('energy', res_energy)

    adjust_image_by_mode(contrast_map)
    adjust_image_by_mode(uniformity_map)
    adjust_image_by_mode(entropy_map)
    adjust_image_by_mode(energy_map)

    contrast_map.show()
    uniformity_map.show()
    entropy_map.show()
    energy_map.show()


def _tmp_contrast_histogram_row(args):
    return contrast_histogram_row(*args)


def _tmp_uniformity_histogram_row(args):
    return uniformity_histogram_row(*args)


def _tmp_entropy_histogram_row(args):
    return entropy_histogram_row(*args)


def _tmp_energy_histogram_row(args):
    return energy_histogram_row(*args)


def contrast_histogram_row(image: Image, y: int, window_size: int) -> [pixel]:
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


def uniformity_histogram_row(image: Image, y: int, window_size: int) -> [pixel]:
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
        mean_probability = sum(probability_histogram) / 256.0

        # Calculate texture features (you can add more features based on your requirements)
        uniformity = sum(prob ** 2 for prob in probability_histogram)
        # uniformity = sum((float(prob) - mean_probability) ** 2 for prob in probability_histogram)

        # Update texture feature map with the calculated feature
        row.append((uniformity * 255, uniformity * 255, uniformity * 255))

    return row


def entropy_histogram_row(image: Image, y: int, window_size: int) -> [pixel]:
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
        entropy = -sum(prob * (0 if prob == 0 else math.log2(prob)) for prob in probability_histogram)

        # Update texture feature map with the calculated feature
        row.append((abs(entropy) * 63, abs(entropy) * 63, abs(entropy) * 63))

    return row


def energy_histogram_row(image: Image, y: int, window_size: int) -> [pixel]:
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
        energy = math.sqrt(sum(prob ** 2 for prob in probability_histogram))
        # Update texture feature map with the calculated feature
        row.append((energy * 255, energy * 255, energy * 255))

    return row
