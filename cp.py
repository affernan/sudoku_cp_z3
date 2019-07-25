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


def cuadrante(xi, yj):
    if (yj >= 0 and yj <= 2) and (xi >=0 and xi <= 2):
        return 0,3,0,3
    elif (yj >= 3 and yj <= 5) and (xi >= 0 and xi <= 2):
        return 0,3,3,6
    elif (yj >= 6 and yj <= 8) and (xi >= 0 and xi <= 2):
        return 0,3,6,9

    elif (yj >= 0 and yj <= 2) and (xi >= 3 and xi <= 5):
        return 3,6,0,3
    elif (yj >= 3 and yj <= 5) and (xi >= 3 and xi <= 5):
        return 3,6,3,6
    elif (yj >= 6 and yj <= 8) and (xi >= 3 and xi <= 5):
        return 3,6,6,9

    elif (yj >= 0 and yj <= 2) and (xi >= 6 and xi <= 8):
        return 6,9,0,3
    elif (yj >= 3 and yj <= 5) and (xi >= 6 and xi <= 9):
        return 6,9,3,6
    elif (yj >= 6 and yj <= 8) and (xi >= 6 and xi <= 9):
        return 6,9,6,9

def block(matrix, xi, yj):
    f1_start, f1_end, f2_start, f2_end = cuadrante(xi, yj)
    lista=[]
    for i in range(f1_start, f1_end):
        for j in range(f2_start, f2_end):
            if i!=xi or j!=yj:
                if matrix[i][j]!=0:
                    lista.append(matrix[i][j])

    return lista








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


def reduce_domainA(matrix, c_row, c_cols, X):

    ContraintDomain = []

    domain_list = []
    row_candidates =[]
    cols_candidates =[]
    candidates = []

    lista=[]
    lista2 = []
    lista3=[]

    solos = []
    Todo1=[]
    for i in range(0, c_row):
        for j in range(0, c_cols):
            if matrix[i][j] == 0:

                row_candidates = getNumberRowsCols (i, matrix[i])
                cols_candidates = column(matrix, j)
                blocke = block(matrix, i, j)

                candidates = set(row_candidates) | set(cols_candidates) | set(blocke)
                domain_list = newDomain(candidates)

                Todo1.append( (i,j, domain_list) )
                if len(domain_list) == 1:
                    solos.append( (i,j, domain_list) )
                #ContraintDomain.append( OrFormat(i, j, domain_list, c_row, X)[0] )
            else:
                Todo1.append((i, j, [matrix[i][j]]))
                solos.append((i, j, [matrix[i][j]]))
                #lista.append( X[i][j]==int(matrix[i][j]) ) #+= "X[" + str(i) +"][" + str(j) +"]==" + str(matrix[i][j]) + ","


    #lista2.append(And(lista))


    #ContraintDomain += ")"
    #ContraintDomain = ContraintDomain.replace(",)", "")
    #return ContraintDomain+lista2

    return Todo1, solos

def filas(i,j, todo1, solos, val):
    f_ini = i * 9
    f_end = i * 9 + 9

    for k in range(f_ini, f_end):
        a, b, celda = todo1[k]

        if j != b and len(celda) > 1:
            c1 = set(celda)
            c2 = set(val)
            c3 = c1 - c2

            todo1[k] = (a, b, list(c3))
            if len(c3) == 1:
                solos.append((a, b, list(c3)))
    return todo1, solos

def columnas(i,j, todo1, solos, val):
    f_ini = j

    for k in range(f_ini, 81, 9):
        a, b, celda = todo1[k]

        if j != a and len(celda) > 1:
            c1 = set(celda)
            c2 = set(val)
            c3 = c1 - c2

            todo1[k] = (a, b, list(c3))
            if len(c3) == 1:
                solos.append((a, b, list(c3)))
    return todo1, solos



def cuadrado(i,j, todo1, solos, val):
    f1_ini, f1_end, f2_ini, f2_end = cuadrante(i,j)

    for ii in range(f1_ini, f1_end):
        for jj in range(f2_ini, f2_end):
            k = ii*9 + jj
            a, b, celda = todo1[k]

            if val[0] in celda:
                if (i != a or j!=b) and len(celda) > 1:
                    c1 = set(celda)
                    c2 = set(val)
                    c3 = c1 - c2

                    todo1[k] = (a, b, list(c3))
                    if len(c3) == 1:
                        solos.append((a, b, list(c3)))
    return todo1, solos


def Convert(todo1,X):

    aux=[]

    final_or = []

    for l in todo1:
        if len(l[2])==1:
            x,y, value = l
            aux.append( X[x][y]==value[0])
        else:
            orr = []
            for ll in l[2]:
                orr.append(X[l[0]][l[1]] == ll)
            final_or.append( Or(orr) )

    A=[]
    A.append(And(aux))

    return A+ final_or



def reduce_domainB(matrix, c_row, c_cols, X):
    #todo1, solos = reduce_domainA(matrix, c_row, c_cols,X)
    todo1=[]
    solos=[]
    for i in range(0,9):
        for j in range(0, 9):
            if matrix[i][j]!=0:
                todo1.append( (i,j, [matrix[i][j]]) )
                solos.append( (i,j, [matrix[i][j]]) )
            else:
                todo1.append((i, j, [1,2,3,4,5,6,7,8,9]))


    while len(solos)>0:

        i, j, domain = solos[0]
        val = list(domain)

        todo1, solos = filas(i,j, todo1, solos, val)
        todo1, solos = columnas(i, j, todo1, solos, val)
        todo1, solos = cuadrado(i, j, todo1, solos, val)

        del solos[0]

    all = Convert(todo1,X)

    return all



