from CSP.CSP import CSP
from CSP.Domain import Domain
from CSP.Constraint import BinaryInequalityConstraint

problem = CSP()

domain = Domain("days", ["Monday", "Tuesday", "Wednesday"])
problem.add_domains(domain)

# Variables
A = problem.add_variable("A", "days")
B = problem.add_variable("B", "days")
C = problem.add_variable("C", "days")
D = problem.add_variable("D", "days")
E = problem.add_variable("E", "days")
F = problem.add_variable("F", "days")
G = problem.add_variable("G", "days")

# Variables problem
problem.add_variable(variable="A",domain_label="days")
problem.add_variable(variable="B",domain_label="days")
problem.add_variable(variable="C",domain_label="days")
problem.add_variable(variable="D",domain_label="days")
problem.add_variable(variable="E",domain_label="days")
problem.add_variable(variable="F",domain_label="days")
problem.add_variable(variable="G",domain_label="days")

# Contraints problem
problem.add_constraints(
    BinaryInequalityConstraint("A", "B"),
    BinaryInequalityConstraint("A", "C"),
    BinaryInequalityConstraint("B", "C"),
    BinaryInequalityConstraint("B", "D"),
    BinaryInequalityConstraint("B", "E"),
    BinaryInequalityConstraint("C", "E"),
    BinaryInequalityConstraint("C", "F"),
    BinaryInequalityConstraint("D", "E"),
    BinaryInequalityConstraint("E", "F"),
    BinaryInequalityConstraint("E", "G"),
    BinaryInequalityConstraint("F", "G"),
)

# Plot a graph which contains the topology of the problem
#problem.plot_graph_problem()

solution = problem.backtracking_search()
for variable in solution:
    print(f'{variable}: {solution[variable]}')