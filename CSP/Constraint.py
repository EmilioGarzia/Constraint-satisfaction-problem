"""
  Constraint parent class
"""
class Constraint:
    def __init__(self, variables: list, verbose=False):
        self.variables = variables
        self.verbose = verbose

    def satisfied(self, assignment, verbose=False):
        return True

    def get_arity(self):
      return len(self.variables)

    def to_string(self):
      return True

"""
  Binary inequality constraint
"""
class BinaryInequalityConstraint(Constraint):
    def __init__(self, variable1, variable2):
        super().__init__([variable1, variable2])
        self.variable1 = variable1
        self.variable2 = variable2

    def satisfied(self, assignment):
        if self.variable1 not in assignment or self.variable2 not in assignment:
            return True
        return assignment[self.variable1] != assignment[self.variable2]

    def to_string(self):
      return f"{self.variable1} ≠ {self.variable2}"


"""
  Binary equality constraint
"""
class BinaryEqualityConstraint(Constraint):
    def __init__(self, variable1, variable2):
        super().__init__([variable1, variable2])
        self.variable1 = variable1
        self.variable2 = variable2

    def satisfied(self, assignment):
        if self.variable1 not in assignment or self.variable2 not in assignment:
            return True
        return assignment[self.variable1] == assignment[self.variable2]

    def to_string(self):
      return f"{self.variable1} = {self.variable2}"

"""
  Binary Less than constraint: A < B
"""
class BinaryLessThanConstraint(Constraint):
  def __init__(self, variable1, variable2, verbose=False):
    super().__init__([variable1, variable2])
    self.variable1 = variable1
    self.variable2 = variable2
    self.verbose = verbose

  def satisfied(self, assignment):
    if self.variable1 not in assignment or self.variable2 not in assignment:
        return True
    return assignment[self.variable1] < assignment[self.variable2]

  def to_string(self):
     return f"{self.variable1} < {self.variable2}"

"""
  Binary Less than constraint: A > B
"""
class BinaryGreaterThanConstraint(Constraint):
  def __init__(self, variable1, variable2, verbose=False):
    super().__init__([variable1, variable2])
    self.variable1 = variable1
    self.variable2 = variable2
    self.verbose = verbose

  def satisfied(self, assignment):
    # Greater than is just the opposite of less than
    return BinaryLessThanConstraint(self.variable2, self.variable1, self.verbose).satisfied(assignment)

  def to_string(self):
     return f"{self.variable1} > {self.variable2}"

"""
  N-ary inequality constraint.
  This method is less efficients respect the binary variaton, so use binary if your constraint is binary.
"""
class NaryInequalityConstraint(Constraint):
    def __init__(self, *variables):
        super().__init__(list(variables))
        self.vars = variables

    def satisfied(self, assignment):
        assigned = [assignment[var] for var in self.variables if var in assignment]
        return len(assigned) == len(set(assigned))

    def to_string(self):
      output_string = str()
      for var in self.vars:
        output_string += f'{var} ≠ '
      output_string = output_string[:-2]
      return output_string

"""
  N-ary equality constraint
  This method is less efficients respect the binary variaton, so use binary if your constraint is binary.
"""
class NaryEqualityConstraint(Constraint):
    def __init__(self, *variables):
        super().__init__(list(variables))
        self.vars = variables

    def satisfied(self, assignment):
        assigned = [assignment[var] for var in self.variables if var in assignment]
        return len(set(assigned)) == 1

    def to_string(self):
      output_string = str()
      for var in self.vars:
        output_string += f'{var} = '
      output_string = output_string[:-2]
      return output_string


"""
  N-ary Less than constraint
  This method is less efficients respect the binary variaton, so use binary if your constraint is binary.
"""
class NaryLessThanConstraint(Constraint):
    def __init__(self, *variables):
        super().__init__(list(variables))
        self.vars = variables

    def satisfied(self, assignment):
        assigned = [assignment[var] for var in self.variables if var in assignment]
        return len(assigned) == 0 or all(assigned[i] < assigned[i+1] for i in range(len(assigned)-1))

    def to_string(self):
      output_string = str()
      for var in self.vars:
        output_string += f'{var} < '
      output_string = output_string[:-2]
      return output_string

"""
  N-ary Greater than constraint
  This method is less efficients respect the binary variaton, so use binary if your constraint is binary.
"""
class NaryGreaterThanConstraint(Constraint):
    def __init__(self, *variables):
        super().__init__(list(variables))
        self.vars = variables

    def satisfied(self, assignment):
        assigned = [assignment[var] for var in self.variables if var in assignment]
        return len(assigned) == 0 or all(assigned[i] > assigned[i+1] for i in range(len(assigned)-1))

    def to_string(self):
      output_string = str()
      for var in self.vars:
        output_string += f'{var} > '
      output_string = output_string[:-2]
      return output_string
