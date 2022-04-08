class State:
  def __init__(self) -> None:
    # self.state = str([line.strip() for line in open("post.txt", 'r')][0])
    return None

  def __str__(self) -> str:
    return str([line.strip() for line in open("post.txt", 'r')][0])
  
  def resetstate(self):
    with open("post.txt", "w") as f:
      f.write("0")

  def getstate(self):
    return str([line.strip() for line in open("post.txt", 'r')][0])

  def changestate(self, state):
    with open("post.txt", "w") as f:
      f.write(state)

post_exploit_state = State()