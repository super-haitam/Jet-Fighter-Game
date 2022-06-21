import random

WIDTH, HEIGHT = 600, 600

# Colors
GREY = tuple(80 for _ in range(3))
DARK_GREY = tuple(60 for _ in range(3))
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

random_color = lambda a, b: tuple(random.randint(a, b) for _ in range(3))
