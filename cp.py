from z3 import *

def getInstance(name):
    file = open(name, "r")
    matrix=[]
    c_cols=0
    for row in file:
        row = list(map(int,row.strip().split()))

        if len(row)>0:
            c_row = len(row)
            matrix.append(tuple(row))
            c_cols+=1

    return tuple(matrix), c_row, c_cols

def column(matrix, j):
    cols=[]
    for x in matrix:
        if x[j]>0:
            cols.append(x[j])

    return cols

def getNumberRowsCols(pos, row):
    candidates=[]
    for i in range(0, len(row)):
        if i != pos and row[i] > 0:
            candidates.append(row[i])
    return candidates

def newDomain(candidates):
    numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    return list(numbers - candidates)

def OrFormat(i, j, domain_list, lon, X):
    # s.add(Or(X[2][1] == 6, X[2][1] == 5, X[2][1] == 7))
    strr=""
    lista=[]
    lista2 = []
    for k in range(0, len(domain_list)):
        d = domain_list[k]
        strr += "X[" + str(i) +"][" + str(j) +"]==" + str(d) + ","
        lista.append(X[i][j]==int(d))

    fin = strr +")"
    fin = fin.replace(",)" , "")

    lista2.append( Or( lista ) )

    return lista2


def reduce_domain(matrix, c_row, c_cols, X):

    ContraintDomain = []

    domain_list = []
    row_candidates =[]
    cols_candidates =[]
    candidates = []

    lista=[]
    lista2 = []

    for i in range(0, c_row):
        for j in range(0, c_cols):
            if matrix[i][j] == 0:
                row_candidates = getNumberRowsCols (i, matrix[i])
                cols_candidates = column(matrix, j)
                candidates = set(row_candidates) | set(cols_candidates)
                domain_list = newDomain(candidates)

                ContraintDomain.append( OrFormat(i, j, domain_list, c_row, X)[0] )
            else:
                lista.append( X[i][j]==int(matrix[i][j]) ) #+= "X[" + str(i) +"][" + str(j) +"]==" + str(matrix[i][j]) + ","


    lista2.append(And(lista))


    #ContraintDomain += ")"
    #ContraintDomain = ContraintDomain.replace(",)", "")
    return ContraintDomain+lista2










