from compiler.ast import flatten

class Mat:
    def __init__(self, height, width = 1):
        self.width = width
        self.height = height
        self.data = [[0 for x in range(width)] for y in range(height)]
        self.type = "Mat"

    def __str__(self):
        m = max([len(str(i)) for i in flatten(self.data)])
        line = ""
        for y in xrange(self.height):
            line += "|"
            for x in xrange(self.width):
                n = self.get(x, y)
                diff = (m - len(str(n))) >> 1
                s = ' ' * diff + str(n) + ' ' * diff
                if m - len(str(n)) > (diff << 1):
                    s += ' '
                line += ' ' + s
            line += " |\n"
        return line

    def get(self, x, y):
        return self.data[y][x]

    def set(self, x, y, val):
        self.data[y][x] = val
