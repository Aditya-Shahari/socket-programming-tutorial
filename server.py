import socket
import threading

# socket(domain, type, protocol)
# domain -> IPv4 / IPv6
# type -> datagram -> UDP (SOCK_DGRAM) / stream -> TCP (SOCK_STREAM) 

HEADER = 64   # msg 64 bytes 
PORT = 5050
# SERVER = "192.168.0.102"
SERVER = socket.gethostbyname(socket.gethostname())
# get ip address automatically, so that you can run this server on different device, value is not hardcoded
# print(SERVER)
ADDR = (SERVER, PORT)   # binding server to port
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '[!DISCONNECT]'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating a socket

server.bind(ADDR)   # bound socket to address

# Handle individual connections between client and server
def handle_client(conn, addr):      
  print(f"[NEW CONNECTION] {addr} connected.")
  connected = True
  
  while connected:
    msg_length = conn.recv(HEADER).decode(FORMAT)  # decode from bytes format into a string
    if msg_length:
      msg_length = int(msg_length)
      msg = conn.recv(msg_length).decode(FORMAT)
      if msg == DISCONNECT_MESSAGE:
        connected = False
      
      print(f"[{addr}] {msg}")
      conn.send("Msg received".encode(FORMAT))
  conn.close()


# Handle new connections and distribute those
def start():    
  server.listen()
  print(f"[LISTENING] Server is listening on {SERVER}") 

  while True:
    conn, addr = server.accept()        # to create new connection to the server, conn is an object with which we can modify it
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")  # tells how may threads are active in this python process
    # amount of threads = amount of clients
    # since start will be running always, - 1


print("[STARTING] server is starting...")
start()
