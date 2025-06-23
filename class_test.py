"""
  This script tries some method from CSP class
"""

from CSP.CSP import CSP
from CSP.Domain import Domain
from CSP.Constraint import *

# Domains definition
palette = Domain(domain_label="palette", domain_entities=["red", "blue", "yellow"])
numbers = Domain(domain_label="numbers", domain_entities=[1,4,2,5,6,5,2,3])

# Remove duplicates from a domain
numbers.drop_duplicates()

# Problem instantiation
problem = CSP(verbose=True)

# Adding variables
problem.add_variable("A")
problem.add_variable("B")
problem.add_variable("C")

# Adding domains to the problem
problem.add_domains(palette)
problem.add_domains(numbers)

# Variable's domain setting
problem.assign_domain_to_variable("A", "numbers")
problem.assign_domain_to_variable("B", "numbers")
problem.assign_domain_to_variable("C", "numbers")

# Values setting
problem.assign_value_to_variable("A", 3)
problem.assign_value_to_variable("B", 1)
problem.assign_value_to_variable("C", 5)

# Problem's constraints
problem.add_constraints(
    BinaryInequalityConstraint("A", "B"),
    BinaryLessThanConstraint("A", "C"),
    NaryGreaterThanConstraint("A", "B", "C"),
    NaryGreatEqualConstraint("A","B","C")
)

# Constraint satisfiability
assignment = {
    "A": problem.variables["A"]["value"],
    "B": problem.variables["B"]["value"],
    "C": problem.variables["C"]["value"],
}

#------------------------------ OUTPUT EXAMPLES ----------------------------#

# Constraints printing
print("\nVerify constraints:")
for constraint in problem.constraints:
    print(f"{constraint.to_string()} → {constraint.satisfied(assignment)}")

# Variables printing
print("\nvariables")
for var in problem.variables:
    print(f"{var} → {problem.variables[var]}")

# Domain entities printing
print(f'\nDomain: {problem.get_domain("numbers").domain_label}')
for entity in problem.get_domain("numbers").domain_entities:
    print(f"{entity}")