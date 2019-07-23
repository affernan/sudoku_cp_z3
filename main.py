from cp import getInstance, reduce_domain
from models import smt_model, cp_smt_model

name = "dataset/a/s01a.txt"
matrix, c_row, c_cols = getInstance(name)
#constraint = reduce_domain(matrix, c_row, c_cols)

#print (constraint)
smt_model(matrix)
print ("otro\n")
cp_smt_model(matrix)








