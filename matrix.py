######################################################################
# Author: Malachi Holden
# Username: holdenm
#
# Final Project
#
# This code defines the matrix module.
# ######################################################################
# Acknowledgements:
#
# Original code written by Malachi Holden
# Ideas taken from T11
# Computation techniques from Mathematics Stack Exchange
# licensed under a Creative Commons
# Attribution-Noncommercial-Share Alike 3.0 United States License.
####################################################################################

class Matrix:
    def __init__(self, entries):
        """Creates a matrix. Entries is a list of lists, giving the entries for the matrix."""
        if type(entries) != list:
            raise Exception("Entries must be in list of lists format.")
        for i in range(len(entries)):
            if type(entries[i]) != list:
                raise Exception("Entries must be in list of lists format.")
            elif len(entries[i]) != len(entries[0]):  #raises an error message if the rows aren't all the same length
                raise Exception("Each row must be the same length.")
            for j in range(len(entries[i])):
                if type(entries[i][j]) not in [int, float, str]:
                    raise Exception("Matrix entries must be floats, integers, or strings.")
                elif type(entries[i][j]) != str:
                    entries[i][j] = round(entries[i][j], 5)
        self.rows = [item[:] for item in entries]  #creates the set of rows
        self.cols = [[entries[j][i] for j in range(len(entries))] for i in range(len(entries[0]))]
        #Creates the set of columns^

    def get_num_rows(self):
        return len(self.rows)

    def get_num_cols(self):
        return len(self.cols)

    def get_widest_per_col(self):
        """Gets the length of the longest entry of each column"""
        widest_elements = [0 for item in self.cols]
        for j in range(len(self.cols)):
            for i in range(len(self.cols[j])):
                if len(str(self.cols[j][i])) > widest_elements[j]:
                    widest_elements[j] = len(str(self.cols[j][i]))
        return widest_elements


    def __str__(self):
        """Sets the matrix class to print matrices in the traditional chart format."""
        ws = self.get_widest_per_col()
        layout = []
        for i in range(self.get_num_cols()):  #Sets up the formatting so each column is wide enough
            layout.append("{0:^" + str(ws[i]+2) + "}")

        string = ""
        for i in range(len(self.rows)): #starts each row with a '|', adds on each element, ends with a '|'
            string += "|"
            for j in range(len(self.rows[i])):
                string += layout[j].format(self.rows[i][j])
            string += "|\n"
        return string


    def transpose(self):
        """Performs a matrix transpose operation"""
        newrows = [column[:] for column in self.cols]  #changes the rows to the columns
        newcols = [row[:] for row in self.rows]  #changes the columns to the rows
        (self.rows, self.cols) = (newrows, newcols)
        return self


    def swaprow(self, rowa, rowb):
        """Swaps rowa and rowb of a matrix. This is an elementary row operation."""
        if rowa not in range(len(self.rows)) or rowb not in range(len(self.rows)):
            raise Exception("Needs an integer from 0 to " + str(len(self.rows)) + " for row index.")
        newrows = [row[:] for row in self.rows]
        newrows[rowa] = self.rows[rowb]
        newrows[rowb] = self.rows[rowa]
        self.rows = newrows
        self.cols = [[newrows[j][i] for j in range(len(newrows))] for i in range(len(newrows[0]))]
        return self


    def scal_mul_row(self, scal, row):
        """Multiplies a row by a scalar. Only works if the row is of numbers."""
        if row not in range(len(self.rows)):
            raise Exception("Needs an integer from 0 to " + str(len(self.rows)) + " for row index.")
        if type(scal) not in [int, float]:
            raise Exception("Scalar multiplication only works on numbers.")
        for item in self.rows[row]:
            if type(item) not in [int, float]:  #raises an error if there's a non-numerical entry in the row
                raise Exception("Scalar multiplication only works on numbers.")
        newrows = [row[:] for row in self.rows]
        newrows[row] = [scal*item for item in self.rows[row]]
        self.rows = newrows
        self.cols = [[newrows[j][i] for j in range(len(newrows))] for i in range(len(newrows[0]))]
        return self


    def add_rows(self, rowa, rowb):
        """Adds rowa to rowb and replaces rowb with the result"""
        if rowa not in range(len(self.rows)) or rowb not in range(len(self.rows)):
            raise Exception("Needs an integer from 0 to " + str(len(self.rows)) + " for row index.")
        for item in self.rows[rowa] + self.rows[rowb]:
            if type(item) not in [int, float]:  #raises an error if there's a non-numerical entry in either row
                raise Exception("Addition only works on numbers.")
        newrows = [row[:] for row in self.rows]
        newrows[rowb] = [self.rows[rowa][i] + self.rows[rowb][i] for i in range(len(self.cols))]
        self.rows = newrows
        self.cols = [[newrows[j][i] for j in range(len(self.rows))] for i in range(len(self.rows[0]))]
        return self


    def rref(self):
        """Performs Gaussian elimination to turn matrix into reduced row echelon form."""
        for row in self.rows:
            for item in row:
                if type(item) not in [int, float]:  #raises an error if there's a non-numerical entry in any entry
                    raise Exception("Reduced Row Echelon Form only works on numbers.")
        (i, j) = (0, 0)  #Starts at the top left corner of the matrix
        while i <= len(self.rows)-1 and j <= len(self.cols):  #Stops the loop when it hits the edge of the matrix
            if self.rows[i][j] == 0:  #if entry i,j is 0...
                value = False
                for entry in range(i, len(self.cols[j])):
                    if self.rows[entry][j] != 0:  #...search the column for a non-zero entry
                        value = True
                        self.swaprow(i, entry)  #swap the non-zero row for the ith row
                if not value:  #if no non-zero entry exists in that column, shift to the next column
                    if j < len(self.cols)-1:  #or stop the traversal if that's the last column
                        j += 1
                    else:
                        break
            else:
                for i2 in range(len(self.rows)):  #if entry i,j is non-zero, use elementary row operations
                    if i2 != i and self.rows[i2][j] != 0:  #to make all the other entries of the column 0
                        self.scal_mul_row(-self.rows[i2][j]/self.rows[i][j], i)
                        self.add_rows(i, i2)

                self.scal_mul_row(1/(self.rows[i][j]), i)  #then make i,j into 1
                (i, j) = (i + 1, j + 1)  #shift diagonally and start the process over
        for i in range(len(self.rows)):
            for j in range(len(self.rows[0])):
                self.rows[i][j] = round(self.rows[i][j], 5)
        self.cols = [[self.rows[j][i] for j in range(len(self.rows))] for i in range(len(self.rows[0]))]

        return self

    def __eq__(self, other):
        """Tests if other is equal to self. Equal means the two matrices have the same entries."""
        if type(other) != Matrix or len(self.rows) != len(other.rows) or len(self.cols) != len(other.cols):
            return False
        for i in range(len(self.rows)):
            for j in range(len(self.cols)):
                if self.rows[i][j] != other.rows[i][j]:
                    return False
        return True

    def __add__(self, other):
        """Adds the two matrices with standard matrix addition."""
        if type(other) != Matrix:
            raise Exception("Matrix addition only works on matrices.")  #raises an error if it's not a matrix
        if len(self.rows) != len(other.rows) or len(self.cols) != len(other.cols):
            raise Exception("Matrix addition only works on equally dimensioned matrices.")
        sum_rows = [[0 for j in self.cols] for i in self.rows]  #initializes the sum to be the all zeros matrix
        for i in range(len(self.rows)):
            for j in range(len(self.cols)):  #traverses the whole matrix, adds self's entry to other's entry,
                #and sets the sum_matrix to the result.
                if type(other.rows[i][j]) not in [int, float]:
                    raise Exception("Matrix entries must be numbers to for addition to work.")
                sum_rows[i][j] = self.rows[i][j] + other.rows[i][j]
        sum_matrix = Matrix(sum_rows)
        return sum_matrix


    def __mul__(self, other):
        """Multiplies the two matrices with standard matrix multiplication."""
        if type(other) not in [Matrix, int, float]:
            raise Exception("Matrix multiplication only works on matrices, and scalar multiplication on scalars.")
        if type(other) in [int, float]:
            for i in range(len(self.rows)):
                self.scal_mul_row(other, i)
            return self
        if len(self.cols) != len(other.rows):
            raise Exception("Number of rows in first matrix must equal number of rows in second matrix.")
        product_rows = [[1 for j in other.cols] for i in self.rows]  #initializes the product to be the all ones
        #matrix.
        for i in range(len(product_rows)):
            for j in range(len(product_rows[i])):  #note that this algorithm traverses the product matrix,
                #not self or other.
                summation = 0
                for entry in range(len(self.cols)): #to find entry i j of the product, traverse the ith row and
                    #jth column of self and other respectively, multiply the respective entries, and sum them
                    #together.
                    summation += self.rows[i][entry]*other.cols[j][entry]
                product_rows[i][j] = summation
        for i in range(len(product_rows)):
            for j in range(len(product_rows[i])):
                product_rows[i][j] = round(product_rows[i][j], 5)
        product_matrix = Matrix(product_rows)
        return product_matrix


    def det(self):
        """Finds the determinant of self. Gets self into reduced row echelon form, recording the change
        in the determinant at each use of elementary row operations. Then multiplies down the diagonal to
        find the determinant."""
        if len(self.rows) != len(self.cols):
            raise Exception("Determinant only works on square matrices.")
        for row in self.rows:
            for item in row:
                if type(item) not in [int, float]:  #raises an error if there's a non-numerical entry in any entry
                    raise Exception("Determinant only works on numbers.")
        coefficient = 1  #this will get formed into the determinant
        (i, j) = (0, 0)  #Starts at the top left corner of the matrix
        messy_matrix = Matrix(self.rows)  #creates a new matrix to mess with
        while i <= len(self.rows)-1 and j <= len(self.cols):  #Stops the loop when it hits the edge of the matrix
            if messy_matrix.rows[i][j] == 0:  #if entry i,j is 0...
                value = False
                for entry in range(i, len(messy_matrix.cols[j])):
                    if messy_matrix.rows[entry][j] != 0:  #...search the column for a non-zero entry
                        value = True
                        messy_matrix.swaprow(i, entry)  #swap the non-zero row for the ith row
                        coefficient *= -1
                if not value:  #if no non-zero entry exists in that column, shift to the next column
                    if j < len(messy_matrix.cols)-1:  #or stop the traversal if that's the last column
                        j += 1
                    else:
                        break
            else:
                for i2 in range(len(messy_matrix.rows)):  #if entry i,j is non-zero, use elementary row operations
                    if i2 != i and messy_matrix.rows[i2][j] != 0:  #to make all the other entries of the column 0
                        c0 = (-messy_matrix.rows[i2][j])/(messy_matrix.rows[i][j])
                        coefficient *= c0
                        messy_matrix.scal_mul_row(c0, i)
                        messy_matrix.add_rows(i, i2)

                c1 = 1/(messy_matrix.rows[i][j])
                coefficient *= c1
                messy_matrix.scal_mul_row(c1, i)  #then make i,j into 1
                (i, j) = (i + 1, j + 1)  #shift diagonally and start the process over
        coefficient = 1/(coefficient)
        determinant = 1
        for entry in range(len(messy_matrix.rows)):
            determinant *= messy_matrix.rows[entry][entry]
        determinant *= coefficient
        return round(determinant, 5)


    def invert(self):
        """Performs an inversion on self."""
        if len(self.rows) != len(self.cols):
            raise Exception("Inverse only works on square matrices.")
        for row in self.rows:
            for item in row:
                if type(item) not in [int, float]:  #raises an error if there's a non-numerical entry in any entry
                    raise Exception("Inversion only works on numbers.")
        if self.det() == 0:
            raise Exception("Inverse only works if determinant is non-zero.")
        n = len(self.rows)
        adjoined_rows = [[0 for i in range(2*n)] for j in range(n)]
        for i in range(n):
            adjoined_rows[i][i+n] = 1
            for j in range(n):
                adjoined_rows[i][j] = self.rows[i][j]
        adjoined_matrix = Matrix(adjoined_rows)
        adjoined_matrix.rref()
        inverted_rows = [[adjoined_matrix.rows[i][j+n] for j in range(n)] for i in range(n)]
        final_matrix = Matrix(inverted_rows)
        self.rows = [row[:] for row in final_matrix.rows]
        self.cols = [col[:] for col in final_matrix.cols]
        for i in range(len(self.rows)):
            for j in range(len(self.rows[0])):
                self.rows[i][j] = round(self.rows[i][j], 5)
        self.cols = [[self.rows[j][i] for j in range(len(self.rows))] for i in range(len(self.rows[0]))]
        return self


    def scal(self, scalar):
        if type(scalar) not in [int, float]:
            raise Exception("Scalar multiplication only works on numbers.")
        for i in range(len(self.rows)):
            self.scal_mul_row(scalar, i)
        return self


    def magnitude(self):
        """Gives the magnitude of a vector represented as a column matrix."""
        if len(self.cols) != 1:
            raise Exception("Magnitude only works on column vectors.")
        summation = 0
        for row in self.rows:
            summation += (row[0])**2
        return summation**(0.5)

def identity(n):
    """Gives the identity matrix of n rows and n columns."""
    if type(n) != int:
        raise Exception("n must be a positive integer.")
    elif n <= 0:
        raise Exception("n must be a positive integer.")
    identity_rows = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        identity_rows[i][i] = 1
    identity_matrix = Matrix(identity_rows)
    return identity_matrix

def zero(n, m):
    """Gives the all zeros matrix of n rows and m columns."""
    if type(n) != int or type(m) != int:
        raise Exception("n and m must be positive integers.")
    elif n <= 0 or m <= 0:
        raise Exception("n must be a positive integer.")
    zero_rows = [[0 for j in range(m)] for i in range(n)]
    zeros_matrix = Matrix(zero_rows)
    x = 4
    return zeros_matrix
