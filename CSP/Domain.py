class Domain:
  def __init__(self, domain_label, domain_entities):
    self.domain_label = domain_label
    self.domain_entities = domain_entities

  """
    Remove duplicates from a domain
  """
  def drop_duplicates(self):
    self.domain_entities = list(set(self.domain_entities))

  """
    Check if domain contains specified value
  """
  def contains(self, value):
    return value in self.domain_entities