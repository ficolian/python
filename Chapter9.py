from tkinter import * 

from tkinter.ttk import *

global fahrenheit
global celcius

def FahrenheitToCelsius():
   global fahrenheit
   temp = fahrenheit.get()
   tempCelcius =(float(temp)-32)*5/9
   celcius.delete(0, 'end')
   celcius.insert(0, tempCelcius)

def CelsiusToFahrenheit():
   # global celcius
   # temp = celcius.get()
   # convertTemp = float(temp)
   # fahrenheit.configure(text='convertTemp')
   global celcius
   temp = celcius.get()
   Fahrenheit = 9/5 *float(temp)+32
   fahrenheit.delete(0,'end')
   fahrenheit.insert(0, Fahrenheit)

# creating main tkinter window/toplevel
master= Tk()

# master = Frame(tk, borderwidth=10)
master.title("Temprature Converter")

# this will create a label widget
l1 = Label(master, text = "Fahrenheit")

l2 = Label(master, text = "Celcius")

# grid method to arrange labels in respective
# rows and columns as specified
l1.grid(row = 0, column = 0, sticky = W, pady = 3, padx = 5)
l2.grid(row = 0, column = 1, sticky = W, pady = 2, padx = 5)

# entry widgets, used to take entry from user

celcius = Entry(master)
fahrenheit = Entry(master)
celcius.insert(0, 0.0)
fahrenheit.insert(0, 32.0)

# this will arrange entry widgets
fahrenheit.grid(row = 1, column = 0 , pady = 2,padx =10)
celcius.grid(row = 1, column = 1, pady = 3, padx =10)

b1 = Button(master, text = ">>>>" , command= FahrenheitToCelsius)
b2 = Button(master, text = "<<<<", command= CelsiusToFahrenheit)

b1. grid(row = 2, column = 0, pady = 3)
b2.grid(row = 2, column = 1, pady = 2)

# infinite loop which can be terminated by keyboard
# or mouse interrupt
mainloop()



