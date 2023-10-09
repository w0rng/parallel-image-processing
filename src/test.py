import matplotlib.pyplot as plt

from image import Image

image = Image.load("assets/example.jpeg")

# set seed for reproducing
data1 = [pixel[0] for row in image.pixels for pixel in row]
data2 = [pixel[1] for row in image.pixels for pixel in row]
data3 = [pixel[2] for row in image.pixels for pixel in row]

plt.figure(figsize=(8, 6))
plt.hist(data1, alpha=0.5, label="red", color="red")
plt.hist(data2, alpha=0.5, label="green", color="green")
plt.hist(data3, alpha=0.5, label="blue", color="blue")
plt.xlabel("Data", size=14)
plt.ylabel("Count", size=14)
plt.title("Multiple Histograms with Matplotlib")
plt.legend(loc="upper right")
plt.show()