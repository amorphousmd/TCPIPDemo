import socket
import threading
import time

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
conn = None
addr = None

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def createData(coords_list):
    list1 = [elem for coords in coords_list for elem in coords]
    msg = ""
    for i in list1:
        msg += ","
        msg += str(i)
    msg = str(len(coords_list)) + msg
    return msg


def zeroExtend(inputList):
    output = []
    for tup in inputList:
        tup = (*tup, 0)
        output.append(tup)
    return output


data1 = [(1, 2), (3, 5), (222, 333)]

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def establish_connection():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    global conn
    global addr
    conn, addr = server.accept()

def send_data_thread(data):
    def send(msg):
        # HEADER = 64
        FORMAT = 'utf-8'
        message = msg.encode(FORMAT)
        # msg_length = len(message)
        # send_length = str(msg_length).encode(FORMAT)
        # send_length += b' ' * (HEADER - len(send_length))
        # client.send(send_length)
        conn.send(message)
    send(createData(zeroExtend(data)))
