import sys
from cp import getInstance
from models import smt_model, cp_smt_model

name = "test/" + str(sys.argv[1])
#name = "test/s12c.txt"
matrix, c_row, c_cols = getInstance(name)
#constraint = reduce_domain(matrix, c_row, c_cols)

#print (constraint)
print ("Z3-----")
smt_model(matrix, name.replace(".txt",""))
print ("\n\nZ3-----CP")
cp_smt_model(matrix, name.replace(".txt",""))








