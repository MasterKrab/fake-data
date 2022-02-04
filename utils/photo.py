from samila import GenerativeImage, Projection
from mimesis import Text
import random
import math


def f1(x, y):
    result = random.uniform(-1, 1) * x ** 2 - math.sin(y ** 2) + abs(y - x)
    return result


def f2(x, y):
    result = random.uniform(-1, 1) * y ** 3 - math.cos(x ** 2) + 2 * x
    return result


text = Text('en')

PROJECTIONS = (Projection.RECTILINEAR, Projection.POLAR, Projection.AITOFF, Projection.HAMMER, Projection.LAMBERT, Projection.MOLLWEIDE)

BACKGROUND_COLORS = ("black", "white")


def create_image(filename):
    file_path = f"images/{filename}.png"

    g = GenerativeImage(f1, f2)
    g.generate()

    g.plot(color=text.hex_color(), bgcolor=random.choice(BACKGROUND_COLORS), projection=random.choice(PROJECTIONS))
    g.save_image(file_adr=file_path)
