import networkx as nx
import matplotlib.pyplot as plt
from CSP.constraint import *
from CSP.domain import Domain

class CSP:
  def __init__(self, variables=None, domains=None, constraints=None, verbose=True):
      self.variables = variables if variables else {}
      self.domains = domains if domains else {}
      self.constraints = constraints if constraints else []
      self.verbose = verbose    # False = warning messages are hidden

  """
    Return a list which contains the elements of the specified domain
  """
  def get_domain(self, domain_label):
    return self.domains[domain_label]

  """
    Add a constraint to the problem's contraints list
  """
  def add_constraints(self, *constraints):
    for contraint in constraints:
      self.constraints.append(contraint)

  """
    Add a variable to the variables list
  """
  def add_variable(self, variable=str, domain_label=None, value=None):
    self.variables[variable] = {"domain":None, "value":None}
    if domain_label is not None:
      self.assign_domain_to_variable(variable,domain_label)
    if value is not None:
      self.assign_value_to_variable(variable,value)

  """
    Assig domain to a specific variable
  """
  def assign_value_to_variable(self, variable, value):
    if variable in self.variables and self.variables[variable]["domain"] is not None:
      domain_label = self.variables[variable]["domain"]
      domain = self.domains[domain_label]
      if domain.contains(value):
        self.variables[variable]["value"] = value
      else:
        if self.verbose:
          print(f"[⚠️] assign_value_to_variable({variable}, {value}): Value not in domain.")
    else:
      if self.verbose:
        print(f"[⚠️] assign_value_to_variable({variable}, {value}): Something went wrong, ensure that the inserted value there exist in the variable's domain")

  """
    Assig domain to a specific variable
  """
  def assign_domain_to_variable(self, variable, domain_label):
    if domain_label in self.domains and variable in self.variables:
      self.variables[variable]["domain"] = domain_label
    else:
      if self.verbose:
        print(f"[⚠️] assign_domain_to_variable({variable}, {domain_label}): Something went wrong, ensure that the inserted domain there exist")

  """
    Add domain to the domains problem list
  """
  def add_domains(self, domain):
    self.domains[domain.domain_label] = domain

  """
    Remove domain from the domains list
  """
  def pop_domain(self, domain_label):
    self.domains.pop(domain_label)

  """
    Remove variable from the variables list
  """
  def pop_variable(self, variable):
    self.variables.pop(variable)

  """
    Remove constraint from the constraints list
  """
  def pop_constraint(self, constraint):
    self.constraints.pop(constraint)

  """
    Unifies two domains in a new one
    replace(True) -> the new one subsitutes the old one (domain1 and domain2 will be erase)
  """
  def domains_union(self, domain1:str, domain2:str, new_domain_label:str, replace=False):
    if domain1 in self.domains and domain2 in self.domains:
      entities = self.domains[domain1].domain_entities + self.domains[domain2].domain_entities
      new_domain = Domain(new_domain_label, entities)
      self.domains[new_domain_label] = new_domain
    if replace:
      self.pop_domain(domain1)
      self.pop_domain(domain2)

  """
    Intersect two domains in a new one
    replace(True) -> the new one subsitutes the old one (domain1 and domain2 will be erase)
  """
  def domains_intersection(self, domain1, domain2, new_domain_label:str ,replace=False):
    entities = [x for x in self.domains[domain1].domain_entities if x in self.domains[domain2].domain_entities]
    self.domains[new_domain_label] = Domain(new_domain_label, entities)
    if replace:
      self.pop_domain(domain1)
      self.pop_domain(domain2)

  """
    Difference between two domains in a new one
    replace(True) -> the new one subsitutes the old one (domain1 and domain2 will be erase)
  """
  def domains_difference(self, domain1, domain2, new_domain_label:str ,replace=False):
    entities = [x for x in self.domains[domain1].domain_entities if x not in self.domains[domain2].domain_entities]
    self.domains[new_domain_label] = Domain(new_domain_label, entities)
    if replace:
      self.pop_domain(domain1)
      self.pop_domain(domain2)

  """
    REVISE(X, Y): Makes variable X arc consistent with Y
    Returns True if a revision was made (i.e., a value was removed from X's domain)
  """
  def revise(self, X, Y):
    revised = False

    domain_X = self.get_domain(self.variables[X]["domain"])
    domain_Y = self.get_domain(self.variables[Y]["domain"])

    constraints = [
      c for c in self.constraints
      if isinstance(c, Constraint) and X in c.variables and Y in c.variables
    ]

    new_domain = []

    for x in domain_X.domain_entities:
      # Check if there is *any* y ∈ domain_Y that satisfies all constraints
      found = False
      for y in domain_Y.domain_entities:
        assignment = {X: x, Y: y}
        if all(c.satisfied(assignment) for c in constraints):
          found = True
          break
      if found:
        new_domain.append(x)
      else:
        revised = True  # x had to be removed

    domain_X.domain_entities = new_domain  # update domain
    return revised

  def ac3(self):
    # Costruisci la coda con tutti gli archi (X,Y) presenti nei vincoli binari
    queue = []
    for constraint in self.constraints:
        if len(constraint.variables) == 2:
            X, Y = constraint.variables
            queue.append((X, Y))
            queue.append((Y, X))  # per farlo bidirezionale

    while queue:
        X, Y = queue.pop(0)
        if self.revise(X, Y):
            domain_X = self.get_domain(self.variables[X]["domain"])
            # Se dominio svuotato → fallimento
            if len(domain_X.domain_entities) == 0:
                return False
            # Aggiungi alla coda archi (Z, X) dove Z è vicino a X ma diverso da Y
            neighbors = set()
            for c in self.constraints:
                if X in c.variables:
                    for var in c.variables:
                        if var != X and var != Y:
                            neighbors.add(var)
            for Z in neighbors:
                queue.append((Z, X))
    return True

  """
    Start the backtracking search
  """
  def backtracking_search(self):
    return self.backtrack({})  # assignment iniziale vuoto

  """
    Backtrack: recursive CSP solver
  """
  def backtrack(self, assignment):
    # Se tutte le variabili sono assegnate, ritorna la soluzione
    if len(assignment) == len(self.variables):
      return assignment

    # Seleziona una variabile non ancora assegnata
    unassigned_vars = [v for v in self.variables if v not in assignment]
    var = unassigned_vars[0]  # euristica: prima variabile libera

    domain_label = self.variables[var]["domain"]
    domain_values = self.get_domain(domain_label).domain_entities

    for value in domain_values:
      local_assignment = assignment.copy()
      local_assignment[var] = value

      if self.is_consistent(var, local_assignment):
        result = self.backtrack(local_assignment)
        if result is not None:
          return result  # successo

    return None  # fallimento

  """
    Controlla se l'assegnamento è consistente con i vincoli del CSP
  """
  def is_consistent(self, var, assignment):
    for constraint in self.constraints:
      if var in constraint.variables:
        if not constraint.satisfied(assignment):
          return False
    return True


  def plot_graph_problem(self):
    G = nx.Graph()
    G.add_nodes_from(self.variables.keys())

    for constraint in self.constraints:
        if constraint.get_arity() == 2:
            # for binary constraints
            G.add_edge(constraint.variable1, constraint.variable2)
        elif constraint.get_arity() > 2:
            # for n-arity constraints
            vars = constraint.variables
            for i in range(len(vars)):
                for j in range(i + 1, len(vars)):
                    G.add_edge(vars[i], vars[j])

    # Plot
    nx.draw(G, with_labels=True, node_color='cyan', node_size=1000, font_size=16)
    plt.show()