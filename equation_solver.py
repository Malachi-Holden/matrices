######################################################################
# Author: Malachi Holden
# Username: holdenm
#
# Final Project
#
# This code allows the user to solve an arbitrary system of linear equations
# ######################################################################
# Acknowledgements:
#
# Original code written by Malachi Holden
# Information on Tkinter class from effbot.org/tkinterbook/
# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

from tkinter import *
import matrix as matrix


class Question:
    def __init__(self, master):
        self.master = master
        frame = Frame(master)
        frame.grid()
        variables = Label(master, text="How many variables do you want to solve for?")
        variables.grid(row=0, column=0)
        self.answer1 = Entry(master, width=4)
        self.answer1.grid(row=0, column=1)
        equations = Label(master, text="How many equations do you want to solve for?")
        equations.grid(row=1, column=0)
        self.answer2 = Entry(master, width=4)
        self.answer2.grid(row=1, column=1)
        go = Button(master, text="Go", command=self.sendoff)
        go.grid(row=2, column=1)

    def sendoff(self):
        if not isvalid(self.answer1.get()) or not isvalid(self.answer2.get()):
            newroot = Tk()
            error = Invalid(newroot)
            newroot.mainloop()
        else:
            file = open("storagefile.txt", "w")
            a = self.answer1.get() + "\n"
            b = self.answer2.get()
            file.write(a + b)
            file.close()
            self.master.quit()


class Systems:
    def __init__(self, master, columns, rows):
        self.master = master
        frame = Frame(master)
        frame.grid()
        self.widjetlist = []
        for i in range(rows):
            widjetrow = []
            for j in range(columns):
                tag = ""
                if j == columns - 1:
                    tag = " = "
                else:
                    tag = " + "
                entry = Entry(master, width=4)
                entry.grid(row=i, column=2*j)
                label = Label(master, text="x" + str(j+1) + tag)
                label.grid(row=i, column=2*j+1)
                widjetrow.append((entry, label))
            tagon = Entry(master, width=4)
            tagon.grid(row=i, column=2*columns+2)
            widjetrow.append((tagon, ""))
            self.widjetlist.append(widjetrow)
        solve = Button(master, text="Solve", command=self.sendoff)
        solve.grid(row=rows+1, column=2*columns+2)

    def sendoff(self):
        for i in range(len(self.widjetlist)):
            for j in range(len(self.widjetlist[i])):
                if not isvalid(self.widjetlist[i][j][0].get()):
                    newroot = Tk()
                    error = Invalid(newroot)
                    newroot.mainloop()
                    return None
        file = open("storagefile.txt","w")
        file.write("")
        file.close()
        file = open("storagefile.txt", "a")
        for i in range(len(self.widjetlist)):
            for j in range(len(self.widjetlist[i])):
                if self.widjetlist[i][j][0].get() == "":
                    file.write("0 ")
                else:
                    file.write(self.widjetlist[i][j][0].get() + " ")
            file.write("\n")
        file.close()
        self.master.quit()


class Final:
    def __init__(self, master):
        self.master = master
        frame = Frame(master)
        frame.grid()
        file = open("storagefile.txt", "r")
        line = file.readline()
        entries = []
        while line:
            entryrow = line[:-2].split()
            for i in range(len(entryrow)):
                entryrow[i] = float(entryrow[i])
            entries.append(entryrow)
            line = file.readline()
        new = matrix.Matrix(entries)
        reduced = new.rref()
        Arows = [[reduced.rows[i][j] for j in range(len(reduced.rows[i])-1)] for i in range(len(reduced.rows))]
        A = matrix.Matrix(Arows)
        consistent = True
        for i in range(len(reduced.rows)):  #Check if the system is consistent...
            if reduced.rows[i][-1] != 0:
                consistent = False
                for j in range(len(reduced.cols)-1):
                    if reduced.rows[i][j] != 0:
                        consistent = True
                        break
        if not consistent:  #...if it's not:
            label = Label(master, text="This system of linear equations\n is not consistent.")
            label.grid(row=0, column=0)
        else:  #... if it is:
            all_vectors = False
            if reduced == matrix.zero(len(reduced.rows), len(reduced.cols)):
                all_vectors = True
            coefficients = []
            for i in range(len(A.rows)):
                leading = False  # tells if there's a leading 1 in the row
                coefficients_row = []
                for j in range(len(A.cols)):
                    if A.rows[i][j] == 1 and not leading:
                        leading = True
                    elif A.rows[i][j] != 0 and leading:
                        coefficients_row.append((-A.rows[i][j], j+1))
                coefficients.append((leading, coefficients_row))
            for i in range(len(coefficients)):
                if all_vectors:
                    label = Label(master, text="x" + str(i+1) + " can be any real number.")
                    label.grid(row=i, column=0)
                if not coefficients[i][0]:
                    continue
                elif coefficients[i][1] == []:
                    label = Label(master, text="x" + str(i+1) + " = " + str(reduced.rows[i][-1]))
                    label.grid(row=i, column=0)
                else:
                    stringer = "x" + str(i+1) + " = "
                    for coefficient in coefficients[i][1]:
                        stringer += str(coefficient[0]) + "*x" + str(coefficient[1]) + " + "
                    stringer += str(reduced.rows[i][-1])
                    label = Label(master, text=stringer)
                    label.grid(row=i, column=0)


class Invalid:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        label = Label(master, text="That is invalid input.\nPlease try something else.")
        label.pack()


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


def main():
    root = Tk()
    A = Question(root)
    root.mainloop()
    file = open("storagefile.txt")
    line1 = file.readline()[:-1]
    line2 = file.readline()
    file.close()
    root = Tk()
    B = Systems(root, int(line1), int(line2))
    root.mainloop()
    root = Tk()
    C = Final(root)
    root.mainloop()

if __name__ == "__main__":
    main()
