import math
from turtle import Turtle


class Shape(object):

    # Represents a shape with color and a turtle
    def __init__(self, turtle, color):
        self.turtle = turtle
        self.color = color

    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color


class Line(Shape):

    # Represent Line Segment

    def __init__(self, x1, y1, x2, y2, turtle, color):
        Shape.__init__(self, turtle, color)

        self.x1 = x1

        self.x2 = x2

        self.y1 = y1

        self.y2 = y2
        self.color = color

    def draw(self):
        # Draw Lines
        # (r, g, b) = self.color

        self.turtle.up()

        self.turtle.goto(self.x1, self.y1)

        self.turtle.pencolor(self.color)

        self.turtle.down()

        self.turtle.goto(self.x2, self.y2)


class Circle(Shape):

    # Represent Circle

    def __init__(self, x, y, radius, turtle, color):
        Shape.__init__(self, turtle, color)

        self.x = x

        self.y = y

        self.radius = radius
        self.color = color

    def draw(self):
        amount = 2.0 * math.pi * self.radius / 120

        self.turtle.up()

        self.turtle.goto(self.x + self.radius, self.y)

        self.turtle.setheading(90)

        self.turtle.down()

        self.turtle.pencolor(self.color)

        for count in range(120):
            self.turtle.left(3)

            self.turtle.forward(amount)


class Rectangle(Shape):

    # Represent rectangle

    def __init__(self, x, y, width, height, turtle, color):
        Shape.__init__(self, turtle, color)

        self.x = x

        self.y = y

        self.width = width

        self.height = height
        self.color = color

    def draw(self):
        # Draw Rectangle


        self.turtle.up()

        self.turtle.goto(self.x, self.y)

        self.turtle.setheading(0)

        self.turtle.down()

        # self.turtle.pencolor(r, g, b)
        self.turtle.pencolor(self.color)

        self.turtle.forward(self.width)

        self.turtle.left(90)

        self.turtle.forward(self.height)

        self.turtle.left(90)

        self.turtle.forward(self.width)

        self.turtle.left(90)

        self.turtle.forward(self.height)


def main():
    t = Turtle()
    x = 0
    y = 0
    x = True
    color = 'black'
    stickColor = 'black'
    while x:
        roof = Line(-200, 80, 0, 160, t, color)  # roof
        roof.draw()
        roof = Line(0, 160, 200, 80, t, color)  # roof
        roof.draw()

        roof = Line(-200, 80, 200, 80, t, color)  # roof
        roof.draw()
        man = Circle(0, 120, 40, t, color)  # Man
        man.draw()
        
        door = Rectangle(-120, -100, 90, 120, t, color)  # door
        door.draw()
        
        house = Rectangle(-180, -100, 360, 180, t,  color)  # house
        house.draw()

        house = Rectangle(-220, -150, 440, 10, t,  color)  # house
        house.draw()
        
       
       
        #x=False

main()