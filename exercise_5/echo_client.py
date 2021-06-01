
import socket
import pickle

host = '127.0.0.1'  # The server's hostname or IP address
port = 65333        # The port used by the server


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

    while True:
        val= input("message to send:")
        if val is not None:
            #package=pickle.dumps(val)
            
            s.sendall(val.encode())
            data = s.recv(1024)
        else:
            break;

print('Received', repr(data))


