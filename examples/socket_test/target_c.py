import socket
import sys
import os


# log file
if not os.path.isdir("output/"):
  os.mkdir("output/")
outfile = open("output/server.log", 'w')


# define FSM
DUMMY_OUTPUTS = ["0", "1", "2", "3", "4", "5"] # dummy because the referene FSM does not have any output symbols. However, other MMs can have important outputs, so I am demonstrating them.

STATES = ["EMM-DEREGISTERED", "EMM-DEREGISTERED-INITIATED", "EMM-REGISTERED", "EMM-COMMON-PROCEDURE-INITIATED"]

ALPHABET = ["detach_accepted", "lower_layer_failure", "network_initiated_detach_requested", "ue_initiated_detach_requested", "tau_rejected", "implicit_detach", "attach_procedure_success", "common_procedure_requested", "common_procedure_failed", "common_procedure_success" ]

TRANSITIONS = {
  ("EMM-DEREGISTERED", "common_procedure_requested"): ("EMM-COMMON-PROCEDURE-INITIATED", "2"),
  ("EMM-DEREGISTERED", "attach_procedure_success"): ("EMM-REGISTERED", "1"),

  ("EMM-REGISTERED", "network_initiated_detach_requested"): ("EMM-DEREGISTERED-INITIATED", "5"),
  ("EMM-REGISTERED", "common_procedure_requested"): ("EMM-COMMON-PROCEDURE-INITIATED", "3"),
  ("EMM-REGISTERED", "ue_initiated_detach_requested"): ("EMM-DEREGISTERED", "4"),
  ("EMM-REGISTERED", "tau_rejected"): ("EMM-DEREGISTERED", "5"),
  ("EMM-REGISTERED", "implicit_detach"): ("EMM-DEREGISTERED", "1"),

  ("EMM-COMMON-PROCEDURE-INITIATED", "common_procedure_success"): ("EMM-REGISTERED", "3"),
  ("EMM-COMMON-PROCEDURE-INITIATED", "attach_procedure_success"): ("EMM-REGISTERED", "1"),
  ("EMM-COMMON-PROCEDURE-INITIATED", "common_procedure_failed"): ("EMM-DEREGISTERED", "2"),
  ("EMM-COMMON-PROCEDURE-INITIATED", "lower_layer_failure"): ("EMM-DEREGISTERED", "4"),

  ("EMM-DEREGISTERED-INITIATED", "detach_accepted"): ("EMM-DEREGISTERED", "4"),
  ("EMM-DEREGISTERED-INITIATED", "lower_layer_failure"): ("EMM-DEREGISTERED", "5")
}

INIT_STATE = "EMM-DEREGISTERED"
NULL_OUTPUT = "0"

cmd_count = 0


# create server 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 8888))
s.listen(1)

print("***Server started***")
outfile.write("***Server started***\n")

# wait for client
(client, address) = s.accept()


# client connected
print("***Cilent connected***")
outfile.write("***Cilent connected***\n\n")


state = INIT_STATE
response = ""

while 1:
  # cmd = input()         # for testing with command line inputs
  cmd = client.recv(1024).decode("utf-8").strip()
  cmd_count += 1

  # print("Received command:  ", cmd)
  outfile.write("Received command:  "+ cmd + '\n')
  
  if cmd == "":                     # learning done
    outfile.write("Breaking...\n")
    break
  elif cmd == "RESET":              # default reset action
    state = INIT_STATE
    response = "DONE"
  else:
    try:
      (dst_state, response) = TRANSITIONS[(state, cmd)]
      state = dst_state
    except KeyError:
      response = NULL_OUTPUT

  # print(state, response)
  # print("Sending response:  ", response)
  outfile.write("Sending response:  " + response + '\n\n')

  client.sendall(bytes(response + "\n", 'utf-8'))

  # print()

print("cmd_count:", cmd_count)
outfile.write("\n\ncmd_count:  " + str(cmd_count) + '\n')

outfile.close()