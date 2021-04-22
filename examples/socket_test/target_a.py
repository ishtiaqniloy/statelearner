import socket

outfile = open("output/server.log", 'w')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 8888))
s.listen(1)

print("***Server started***")
outfile.write("***Server started***\n")

(client, address) = s.accept()

print("***Cilent connected***")
outfile.write("***Cilent connected***\n\n")

INIT_STATE = 0
cmd_count = 0

state = INIT_STATE
response = ""

while 1:
  cmd = client.recv(1024).decode("utf-8").strip()
  cmd_count += 1

  # print("Received command:  ", cmd)
  outfile.write("Received command:  "+ cmd + '\n')

  if cmd == "":
    outfile.write("Breaking...\n")
    break

  if cmd == "RESET":
    state = INIT_STATE
    response = "DONE"
  
  elif cmd == "A":
    if state == 0:
      response = "C"
    else:
      response = "D"

  elif cmd == "B":
    state = 1 - state
    response = "E"
  
  elif cmd == "C":
    response = str(state)
    state = 1 - INIT_STATE

  # print("Sending response:  ", response)
  outfile.write("Sending response:  " + response + '\n\n')

  client.sendall(bytes(response + "\n", 'utf-8'))

  # print()

print("cmd_count:", cmd_count)
outfile.write("\n\ncmd_count:  " + str(cmd_count) + '\n')

outfile.close()