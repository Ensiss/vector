class Mat:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[0 for x in range(width)] for y in range(height)]
        self.type = "Mat"

    def get(x, y):
        return self.data[y][x]

    def set(x, y, val):
        self.data[y][x] = val
