import pickle
import socket
import threading

'''def sendmsg(node, msg, sended=set()):
    if node is not None:
        for connected_node in node.connected_node:
            if connected_node.connected_node_id not in sended:
                sended.add(connected_node.connected_node_id)
                connected_node.send_message(f"\n{node.id}: {msg}")
                #sendmsg(find_node_by_port(node.port - 1), msg, sended)
                #sendmsg(find_node_by_port(node.port + 1), msg, sended)
    else:
        return'''

class NodeConnection(threading.Thread):

    def __init__(self, main_node, socket, connected_node_id, host, port):
        super().__init__()
        self.main_node = main_node
        self.s = socket
        self.connected_node_id = connected_node_id
        self.host = host
        self.port = port
        self.running = True
    
    def send_message(self, msg, sended=set()):
        if self.connected_node_id not in sended:
            sended.add(self.connected_node_id)
            data = {
                "msg": msg,
                "sended": sended
            }
            data = pickle.dumps(data)
            try:
                self.s.sendall(data)
            except Exception as e:
                print(f"{self.main_node.id}: cannot send message.")
        else:
            return

    def run(self):
        #self.s.timeout = 5.0
        while self.running:
            try:
                data = pickle.loads(self.s.recv(4096))
                msg = data["msg"]
                sended = data["sended"]
                if not data:
                    self.running = False
                    print("Ummm?")
                    break
                print(f"{msg}")
                try:
                    self.send_message(msg, sended)
                except Exception as e:
                    print(e)
            except Exception as e:
                self.running = False
                print(e)
        
        self.s.close()
        print(f"{self.port} closed.")
    
    def stop(self):
        self.running = False

class Node(threading.Thread):

    def __init__(self, host, port, max_connections=2):
        super().__init__(daemon=True)
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.connected = 0
        self.connected_node = []
        self.running = True
        self.id = str(id(self.port))   #Too lazy, so I just assign id using memory address
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))
        self.s.listen(max_connections)
        print(f"listening on port {port} with ID:{self.id}")
    
    def connect_to(self, target_host, target_port):
        
        if self.connected >= self.max_connections:
            print(f"{self.id} has maximum number of connections already.")
            return
        
        if target_host == self.host and target_port == self.port:
            print(f"{self.id}: Cannot connect to itself.")
            return
        
        for conn in self.connected_node: 
            if target_port == conn.port:
                print(f"{self.id}: port {target_port} was already connected on this node.")

        try:
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_socket.connect((target_host, target_port))
            self.connected = self.connected + 1

            new_socket.sendall(self.id.encode())
            connected = new_socket.recv(4096).decode()

            client = NodeConnection(self, new_socket, connected, target_host, target_port)
            client.start()
            self.connected_node.append(client)
        except Exception as e:
            print(e)
            return

    def run(self):
        while self.running and self.connected < self.max_connections:
            try:
                connection, address = self.s.accept()

                incoming_node = connection.recv(4096).decode()
                connection.sendall(self.id.encode())
                
                print(f"{self.id}: established connection with {incoming_node}")
                self.connected = self.connected + 1
                client = NodeConnection(self, connection, incoming_node, address[0], address[1])
                client.start()

                self.connected_node.append(client)
            except Exception as e:
                print(e)
                self.running = False
        else:
            while self.running:
                pass