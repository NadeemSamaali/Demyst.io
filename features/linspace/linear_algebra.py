class matrix :
    # Checking if all the rows of the list are of equal lengths before building the matrix
    def __init__(self, entries) :
        self.entries = entries
        for i in range(len(self.entries) - 1) :
            if len(self.entries[i]) != len(self.entries[i+1]) :
                raise ValueError("Cannot build a matrix")
        if len(self.entries) == len(self.entries[0]) :
            self.__class__ = s_matrix
        if len(self.entries[0]) == 1 :
            self.__class__ = vector

    # Print the matrix with orgnanized rows and columns
    def print(self) :
        print()
        k = []
        maxlength = 0
        # Identifying the number with the largest amount of characters in each column
        for a in range(len(self.entries[0])) :
            for b in range(len(self.entries)) :
                length = len(list(f"{self.entries[b][a]:.2f}"))
                if length > maxlength :
                    maxlength = length
                    if self.entries[b][a] < 0 :
                        maxlength -= 1
                length = 0
            k.append(maxlength)
            maxlength = 0
        # Printing the matrix in determinant form with alligned columns
        for i in range(len(self.entries)) :
            print(" ", end="")
            for j in range(len(self.entries[0])) :
                if self.entries[i][j] < 0 :
                    print("", end = "")
                    print(f'{"{:.2f}".format(self.entries[i][j])}', end = " ")
                    for a in range(k[j] - len(list(f"{self.entries[i][j]:.2f}")) + 1) :
                        print(" ", end = "")
                else :
                    print(" ", end = "")
                    print(f'{"{:.2f}".format(self.entries[i][j])}', end = " ")
                    for a in range(k[j] - len(list(f"{self.entries[i][j]:.2f}"))) :
                        print(" ", end = "")      
            print()
        print()
    # Function performing matrix multiplication between two matrices M1 and M2
    def multiply(self, m) :
        if len(self.entries[0]) != len(m.entries) :
            raise ValueError("These two matrices aren't multiplicable | len(M1[0]) != len(M2)")
        m0 = [[0]*len(m.entries[0]) for _ in range(len(self.entries))]

        for i in range(len(self.entries)) :
            for j in range(len(m.entries[0])) :
                sum = 0
                for k in range(len(self.entries[0])) :
                    sum += self.entries[i][k]*m.entries[k][j]
                m0[i][j] = sum
        return matrix(m0)
    # Function to store rows of a matrix in ascending order of leading zeros
    def _m_sort(self):
        def count_leading_zeros(row):
            count = 0
            for element in row:
                if element == 0:
                    count += 1
                else:
                    break
            return count
        sorted_matrix = sorted(self.entries, key=count_leading_zeros)
        return matrix(sorted_matrix)
    # Scalar product
    def times(self, k) :
        M = [[k*self.entries[i][j] for j in range(len(self.entries[0]))] for i in range(len(self.entries))]
        return s_matrix(M) if len(self.entries) == len(self.entries[0]) else matrix(M)
    # Outputs transpose of a matrix
    def transpose(self) :
        M = [[self.entries[i][j] for i in range(len(self.entries))] for j in range(len(self.entries[0]))]
        return s_matrix(M) if len(self.entries) == len(self.entries[0]) else matrix(M)
    # Function performing row addition
    def __rowsub(self, row1, row2) :
        for i in range(len(self.entries[row1])) :
            self.entries[row2][i] -= self.entries[row1][i]
    # Function performing row scalar multiplication      
    def __rowtimes(self, row, k) :
        for i in range(len(self.entries[row])) :
            self.entries[row][i] *= k
    
    # Function reducing an arbitrary matrix into its reduced row echelon form   
    def reduce(self) : 
        m = [[self.entries[i][j] for j in range(len(self.entries[0]))] for i in range(len(self.entries))]
        M = matrix(m)
        M = M._m_sort()
        a = M.entries
        for i in range(len(a)) :
            for j in range(len(a[0])) :
                if a[i][j] != 0 :
                    M.__rowtimes(i, 1/a[i][j])
                    for k in range(len(a)) :
                        if k != i and a[k][j] != 0 :
                            M.__rowtimes(i, a[k][j]/a[i][j])
                            M.__rowsub(i, k)
                    M.__rowtimes(i, 1/a[i][j])
                    break
                else :
                    pass
        return M
# Square matrix class exteneding from the matrix class
class s_matrix(matrix) :
    def __init__(self, entries) :
        self.entries = entries
        # Checking to see if the matrix is square
        for rows in self.entries :
            if len(rows) != len(self.entries) :
                raise ValueError("Cannot build a square matrix")
    # Function outputting the amounts of permutations needeed to obtain a sorted matrix
    def __permutations(self) :
        k = 0.0
        self.k = k
        I = self.entries
        F = self._m_sort().entries
        for i in range(len(I[0])) :
            if I[i] != F[i] :
                for j in range(i+1, len(I[0])) :
                    if I[j] == F[i] :
                        k += 1
                        break
        return k
    # Function to check if a matrix needs to be sorted 
    def __needsSort(self) :
        s = self._m_sort()
        if s.entries == self.entries :
            return False
        else :
            return True
    # Function finding the determinant of a matrix by reducing it to upper triangular form 
    def determinant(self) :
        M = [[self.entries[i][j] for j in range(len(self.entries[0]))] for i in range(len(self.entries))]
        m = matrix(M)
        det = 1.0 ; permuations = 0 ; k = []
        if m.__needsSort() :
            permuations += m.__permutations()
            m = m._m_sort()
        for i in range(len(m.entries)) :
            for j in range(i, len(m.entries)) :
                if m.entries[i][j] != 0 :
                    for a in range(i+1, len(m.entries)) :
                        if m.entries[a][j] != 0 :
                            k.append(m.entries[i][j]/m.entries[a][j])
                            for b in range(len(m.entries)) :
                                m.entries[a][b] *= k[len(k) - 1]
                                if float(f"{m.entries[a][b]:.9f}") == -0.0 :
                                    m.entries[a][b] = 0
                            for c in range(len(m.entries)) :
                                m.entries[a][c] -= m.entries[i][c]
                                if float(f"{m.entries[a][c]:.9f}") == -0.0 :
                                    m.entries[a][c] = 0
                if m.__needsSort() :
                    permuations += m.__permutations()
                    m = m._m_sort()
                break
        for x in range(len(k)) :
            det *= 1/k[x]
        for y in range(len(m.entries[0])) :
            det *= m.entries[y][y]
        det *= (-1)**permuations
        return det
    # Function outputing the cofactor matrix of a square matrix
    def cofactor(self) :
        M = [[0]*(len(self.entries)) for _ in range(len(self.entries))]
        subM = [[0]*(len(self.entries)-1) for _ in range(len(self.entries)-1)]
        mStore = []
        a = 0; b = 0; c = 0
        for i in range(len(self.entries)) :
            for j in range(len(self.entries)) :
                for k in range(len(self.entries)) :
                    for l in range(len(self.entries)) :
                        if k != i and l != j :
                            subM[a][b] = self.entries[k][l]
                            b+=1
                            if b == len(self.entries) - 1 :
                                a += 1 ; b = 0
                            if a == len(self.entries) - 1 :
                                a = 0 ; b = 0
                mStore.append(subM)
                M[i][j] = (-1)**(i+j)*s_matrix(mStore[c]).determinant()
                if float(f"{M[i][j]:.9f}") == -0.0  :
                    M[i][j] = 0
            c += 1
        return s_matrix(M)
    # Function calculates the inverse matrix of an invertible matrix
    def inverse(self) :
        if self.determinant() == 0 :
            raise ValueError('This matrix is not invertible')
        return self.cofactor().transpose().times(1/self.determinant())

# Vector data type extending from matrix
class vector(matrix) :
    def __init__(self, entries) :
        self.entries = [[float(entries[i])] for i in range(len(entries))]
    # Vector sum
    def add(self, v) :
        if len(self.entries) != len(v.entries) : 
            raise ValueError("Vectors need to be of the same length to be summed")
        sum = [self.entries[i][0] + v.entries[i][0] for i in range(len(self.entries))]
        return vector(sum)
    # Dot product of two vectors
    def dot(self, v) :
        if len(self.entries) != len(v.entries) : 
            raise ValueError("Vectors need to be of the same length to calculate dot product")
        sum = 0.0
        for i in range(len(self.entries)) :
            sum += self.entries[i][0] * v.entries[i][0]
        return sum
    def cross(self, v) :
        if len(self.entries) != 3 or len(v.entries) != 3 :
            raise ValueError("Cross produce can only be performed on three dimensional vectors")
        M = [[1,-1,1]] + [[n[0] for n in self.entries]] + [[m[0] for m in v.entries]]
        cList, C, v0 = [],[[0,0],[0,0]],[[0],[0],[0]]
        for h in range(3) :
            for i in range(3) :
                for j in range(3) :
                    if i != 0 and j != h :
                        cList.append(M[i][j])
            c = 0
            for a in range(2) :
                for b in range(2) :
                    C[a][b] = cList[c]
                    c+=1
            v0[h][0] = M[0][h]*s_matrix(C).determinant()
            if v0[h][0] == -0 :
                v0[h][0] = 0
            cList.clear()
        return vector([v0[0][0], v0[1][0], v0[2][0]])
    # Function to find the orthogonal projection of v1 onto v2
    def projection(self, v) :
        a2 = 0.0
        if len(self.entries) != len(v.entries) :
            raise ValueError("Make sure both vectors are of the same dimension")
        v0 = [0 for _ in range(len(self.entries))] ; k = self.dot(v)
        for i in range(len(self.entries)) : 
            a2 += v.entries[i][0]**2
        for j in range(len(self.entries)) :
            v0[j] = (k/a2)*v.entries[j][0]
        return vector(v0)