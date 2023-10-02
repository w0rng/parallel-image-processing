from algorithms.yuv_convert import row_to_yuv
from image import Image
from utils import Pool


def main(count):
    image = Image.load("assets/example.jpeg")
    with Pool("yuv", count) as pool:
        result = pool.map(row_to_yuv, image.pixels)
    Image(result).show()


if __name__ == "__main__":
    for i in range(1, 5):
        main(i)
