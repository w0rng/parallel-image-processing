from image import Image
from .delta import delta
from .mse import mse
from .msad import msad
from .psnr import psnr
from prettytable import PrettyTable

results = []


def calc(name: str, time: float, noise_image: Image, filtered_image: Image):
    delta_ = delta(noise_image, filtered_image)
    mse_ = mse(filtered_image, noise_image)
    msad_ = msad(filtered_image, noise_image)
    psnr_ = psnr(filtered_image, noise_image)

    table = PrettyTable()
    table.field_names = ["Name", "Time", "Delta", "MSE", "MSAD", "PSNR"]
    results.append([name, f"{time:.2f}", f"{delta_:.2f}", f"{mse_:.2f}", f"{msad_:.2f}", f"{psnr_:.2f}"])
    for row in results:
        table.add_row(row)

    with open("metrics.txt", "w") as file:
        file.write(table.get_string())

