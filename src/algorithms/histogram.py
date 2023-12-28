from src.image import Image
from src.algorithms.utils.adjust_image_by_mode import adjust_image_by_mode


def calculate_texture_features(image: Image, window_size=3):
    if image.mode != 'grayscale':
        image.to_grayscale()

    width, height = image.size

    texture_feature_map = [[0] * width for _ in range(height)]

    # Iterate over the image
    for y in range(height):
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
            texture_feature_map[y][x] = contrast

    new_image = Image(pixels=[[(value, value, value) for value in row] for row in texture_feature_map], mode='grayscale')
    adjust_image_by_mode(new_image)

    return new_image


