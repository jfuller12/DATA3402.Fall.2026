
class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]

    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]

    def v_line(self, x, y, h, **kargs):
        for i in range(y, y + h):
            self.set_pixel(i, x, **kargs)

    def h_line(self, x, y, w, **kargs):
        for i in range(x, x + w):
            self.set_pixel(y, i, **kargs)

    def line(self, x1, y1, x2, y2, **kargs):
        slope = (x2 - x1) / (y2 - y1)

        for y in range(y1, y2):
            x = x1 + int(slope * (y - y1))
            self.set_pixel(y, x, **kargs)

    def display(self):
        print("\n".join(["".join(row) for row in self.data]))


class Base:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_perimeter_points(self):
        raise NotImplementedError

    def is_inside(self, x, y):
        raise NotImplementedError

    def overlaps(self, other):
        points = self.get_perimeter_points()

        for point in points:
            if other.is_inside(point[0], point[1]):
                return True

        return False

    def paint(self, canvas):
        raise NotImplementedError


class Rectangle(Base):
    def __init__(self, length, width, x, y):
        super().__init__(x, y)
        self.__length = length
        self.__width = width

    def area(self):
        return self.__length * self.__width

    def perimeter(self):
        return 2 * (self.__length + self.__width)

    def get_length(self):
        return self.__length

    def get_width(self):
        return self.__width

    def get_perimeter_points(self):
        x = self.get_x()
        y = self.get_y()

        return [
            (x, y),
            (x + self.__length, y),
            (x + self.__length, y + self.__width),
            (x, y + self.__width)
        ]

    def is_inside(self, x, y):
        if x >= self.get_x() and x <= self.get_x() + self.__length:
            if y >= self.get_y() and y <= self.get_y() + self.__width:
                return True

        return False

    def paint(self, canvas):
        x = self.get_x()
        y = self.get_y()

        canvas.h_line(x, y, self.__length, char='*')
        canvas.h_line(x, y + self.__width, self.__length, char='*')
        canvas.v_line(x, y, self.__width, char='*')
        canvas.v_line(x + self.__length, y, self.__width, char='*')

    def __repr__(self):
        return "Rectangle(" + str(self.__length) + "," + str(self.__width) + "," + str(self.get_x()) + "," + str(self.get_y()) + ")"


class Circle(Base):
    def __init__(self, radius, x, y):
        super().__init__(x, y)
        self.__radius = radius

    def area(self):
        return 3.14 * self.__radius * self.__radius

    def perimeter(self):
        return 2 * 3.14 * self.__radius

    def get_radius(self):
        return self.__radius

    def get_perimeter_points(self):
        x = self.get_x()
        y = self.get_y()
        r = self.__radius

        return [
            (x + r, y),
            (x - r, y),
            (x, y + r),
            (x, y - r)
        ]

    def is_inside(self, x, y):
        distance_x = x - self.get_x()
        distance_y = y - self.get_y()

        distance = distance_x * distance_x + distance_y * distance_y

        if distance <= self.__radius * self.__radius:
            return True

        return False

    def paint(self, canvas):
        x = self.get_x()
        y = self.get_y()
        r = self.__radius

        canvas.set_pixel(y - r, x, char='*')

        canvas.set_pixel(y - 1, x - r + 1, char='*')
        canvas.set_pixel(y - 1, x + r - 1, char='*')

        canvas.set_pixel(y, x - r, char='*')
        canvas.set_pixel(y, x + r, char='*')

        canvas.set_pixel(y + 1, x - r + 1, char='*')
        canvas.set_pixel(y + 1, x + r - 1, char='*')

        canvas.set_pixel(y + r, x, char='*')

    def __repr__(self):
        return "Circle(" + str(self.__radius) + "," + str(self.get_x()) + "," + str(self.get_y()) + ")"


class Triangle(Base):
    def __init__(self, base, height, side1, side2, side3, x, y):
        super().__init__(x, y)
        self.__base = base
        self.__height = height
        self.__side1 = side1
        self.__side2 = side2
        self.__side3 = side3

    def area(self):
        return 0.5 * self.__base * self.__height

    def perimeter(self):
        return self.__side1 + self.__side2 + self.__side3

    def get_base(self):
        return self.__base

    def get_height(self):
        return self.__height

    def get_side1(self):
        return self.__side1

    def get_side2(self):
        return self.__side2

    def get_side3(self):
        return self.__side3

    def get_perimeter_points(self):
        x = self.get_x()
        y = self.get_y()

        return [
            (x, y),
            (x + self.__base, y),
            (x + self.__base // 2, y + self.__height)
        ]

    def is_inside(self, x, y):
        if x < self.get_x() or x > self.get_x() + self.__base:
            return False

        if y < self.get_y() or y > self.get_y() + self.__height:
            return False

        return True

    def paint(self, canvas):
        x = self.get_x()
        y = self.get_y()

        canvas.h_line(x, y, self.__base, char='*')

        canvas.line(
            x,
            y,
            x + self.__base // 2,
            y + self.__height,
            char='*'
        )

        canvas.line(
            x + self.__base,
            y,
            x + self.__base // 2,
            y + self.__height,
            char='*'
        )

    def __repr__(self):
        return "Triangle(" + str(self.__base) + "," + str(self.__height) + "," + str(self.__side1) + "," + str(self.__side2) + "," + str(self.__side3) + "," + str(self.get_x()) + "," + str(self.get_y()) + ")"


class CompoundShape(Base):
    def __init__(self, shapes):
        super().__init__(0, 0)
        self.__shapes = shapes

    def paint(self, canvas):
        for shape in self.__shapes:
            shape.paint(canvas)
