from turtle import Turtle
from math import pi

def DrawCircle(t,x,y, radius):

    t.up()
    t.setposition(x,y)
    t.forward(radius)
    t.left(90)
    t.down()
    forDist=((2*pi*radius) /120)

    for i in range(120):
        t.left(3)
        t.forward(forDist)
    
def main(): 
    t=Turtle()
    x = 55
    y= 80
    radius = 100
    DrawCircle (t,x,y, radius)

# main()

num1 = input("Bilangan 1 :")
num2 = input("Bilangan 2 :")











