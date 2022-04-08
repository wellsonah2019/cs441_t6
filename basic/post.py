class State:
  def __init__(self) -> None:
      self.state = "0"

  def __str__(self) -> str:
    return self.state
  
  def getstate(self):
    return self.state

  def changestate(self, state):
    if isinstance(state, int):
      self.state = state
    else:
      self.state = state

post_exploit_state = State()