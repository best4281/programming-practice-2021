
import socket
import pickle

host = "127.0.0.1"
port= 65333
number_of_connections= 3


#by using "with" we do not need to close the socket= s.close()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #TCP = SOCK_STREAM
    #IPV4 = AF_INET
    s.bind((host, port))
    s.listen(number_of_connections)
    
    #get a connection
    conn, addr= s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print("Server received:", data)
            if not data:
                break
            conn.sendall(data)
            
            data= data.decode()
            print("server value:", data)




