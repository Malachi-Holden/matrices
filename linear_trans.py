######################################################################
# Author: Malachi Holden
# Username: holdenm
#
# Final Project
#
# This code visually represents linear transformations using turtles.
# ######################################################################
# Acknowledgements:
#
# Original code written by Malachi Holden
# Ideas from 3blue1brown youtube channel
# Information on Tkinter class from effbot.org/tkinterbook/
# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

import turtle
import matrix as matrix
from tkinter import *


class Lintrans:
    def __init__(self, master):
        frame = Frame(master)
        frame.grid()
        message = Label(master, text="Wait a minute while\nthe vectors load.")
        message.grid(row=0, column=0)
        self.vector_list = []
        for i in range(-10, 11):
            for j in range(-10, 11):
                vector = matrix.Matrix([[10*i], [10*j]])
                self.vector_list.append(vector)
        self.turtle_list = []
        for vector in self.vector_list:
            singleton = turtle.Turtle(shape="circle",visible=False)
            singleton.shapesize(0.2)
            self.turtle_list.append(singleton)
            singleton.penup()
            singleton.speed(0)
        for i in range(len(self.vector_list)):
            self.turtle_list[i].goto(self.vector_list[i].rows[0][0], self.vector_list[i].rows[1][0])
            self.turtle_list[i].showturtle()
        message.config(text="")
        self.label = Label(master, text="Type a matrix and click transform.\nOr click end to end the program.")
        self.label.grid(row=0, column=0, columnspan=4)
        self.entry1 = Entry(master, width=4)
        self.entry1.grid(row=1, column=0)

        self.entry2 = Entry(master, width=4)
        self.entry2.grid(row=1, column=1)

        self.entry3 = Entry(master, width=4)
        self.entry3.grid(row=2, column=0)

        self.entry4 = Entry(master, width=4)
        self.entry4.grid(row=2, column=1)

        self.transform = Button(master, text="Transform", command=self.transformer)
        self.transform.grid(row=1, column=2, columnspan=2)

        self.reset = Button(master, text="Reset", command=self.reseter)
        self.reset.grid(row=2, column=2)

        self.end = Button(master, text="End", command=frame.quit)
        self.end.grid(row=2, column=3)

    def transformer(self):
        if not(isvalid(self.entry1.get()) and isvalid(self.entry2.get()) and isvalid(self.entry3.get())
               and isvalid(self.entry4.get())):
            newroot = Tk()
            A = Invalid(newroot)
            newroot.mainloop()
        else:
            if self.entry1.get() == "":
                a = 0
            else:
                a = float(self.entry1.get())
            if self.entry2.get() == "":
                b = 0
            else:
                b = float(self.entry2.get())
            if self.entry3.get() == "":
                c = 0
            else:
                c = float(self.entry3.get())
            if self.entry4.get() == "":
                d = 0
            else:
                d = float(self.entry4.get())
            multiplier = matrix.Matrix([[a, b], [c, d]])
            for index in range(len(self.vector_list)):
                self.vector_list[index] = multiplier*self.vector_list[index]
                self.turtle_list[index].goto(self.vector_list[index].rows[0][0], self.vector_list[index].rows[1][0])

    def reseter(self):
        coordinatelist = []
        for i in range(-10, 11):
            for j in range(-10, 11):
                    coordinatelist.append((10*i, 10*j))
        for index in range(len(self.vector_list)):
            self.vector_list[index] = matrix.Matrix([[coordinatelist[index][0]], [coordinatelist[index][1]]])
            self.turtle_list[index].goto(self.vector_list[index].rows[0][0], self.vector_list[index].rows[1][0])


def isvalid(str_input):
    """Boolean determining if a string str_input is a number, either a float or integer."""
    if str_input == "":
        return True
    if str_input[0] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "."]:
        return False
    dot_count = 0
    for ch in str_input[1:]:
        if ch == ".":
            dot_count += 1
        if dot_count == 2:
            return False
        if ch not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
            return False
    return True


class Invalid:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        label = Label(master, text="That is invalid input.\nPlease try something else.")
        label.pack()


def main():
    wn = turtle.Screen()
    root = Tk()
    L = Lintrans(root)
    root.mainloop()
    wn.bye()

if __name__ == "__main__":
    main()
