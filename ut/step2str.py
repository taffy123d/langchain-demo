def step_to_string(step):
  string = ""
  action = step[0]
  string += "动作:\n"
  for it in action:
    string += str(it[0]) + " :"
    string += str(it[1]) + "\n"
  observation = step[1]
  string += f'结果:\n {observation}'
  return string