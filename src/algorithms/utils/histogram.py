import PIL


def histogram(image):
    pilow_image = PIL.Image.new("RGB", image.size)
    for y, row in enumerate(image.pixels):
        for x, pixel in enumerate(row):
            pilow_image.putpixel((x, y), pixel)

    return pilow_image.histogram()[0:256]
