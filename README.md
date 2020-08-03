# SCCC_XXXX: Satisfiability Modulo Theories Solver using Local Consistency Techniques for the Sudoku Puzzles
Authors: Alejandro Fernández Gil, Mariam Gómez Sánchez and Carlos Castro

# Abstract:
In this work, we solve some benchmark of Sudoku
puzzles. The resolution tool and techniques used to solve it were
Z3 SMT solver with Constraint Programming techniques based
on Local Consistency (LC). The SMT solvers can be used to
generate satisfiability assignments to variables and LC plays
an important role in constraint satisfaction because it finds
inconsistencies in the values of the domains of the variables,
reducing the search space. We propose a collaborative approach
to solve Sudoku, consisting of an LC based procedure, being
able of reducing the domains of the problem variables, to later
be solved by a procedure modeled and implemented in Z3. The
computational results demonstrate the advantage of using LC
techniques as part of Z3
