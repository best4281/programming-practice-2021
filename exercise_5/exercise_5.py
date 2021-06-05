import node2 as n

host = "localhost"

def exercise_5(inputs): # DO NOT CHANGE THIS LINE
    
    for port in range (8001, 8021):
        try:
            node = n.Node("localhost", port)
            node.start()
            break
        except:
            continue
    try:
        node.connect_to("localhost", port-1)
    except:
        pass

    #node.join()

    while True:
        val= input("message to send:")
        for conn in node.connected_node:
            conn.send_message(f"\n{node.id}: {val}")

    output = inputs

    return output       # DO NOT CHANGE THIS LINE

exercise_5(None)

'''if __name__ == "__main__":
    nodes = [n.Node("localhost", port) for port in range(8001, 8021)]
    for node in nodes:
        node.start()
    nodes[1].connect_to("localhost", nodes[0].port)
    nodes[2].connect_to("localhost", nodes[0].port)
    nodes[3].connect_to("localhost", nodes[0].port)
    nodes[4].connect_to("localhost", nodes[0].port)
    nodes[5].connect_to("localhost", nodes[0].port)
    nodes[6].connect_to("localhost", nodes[0].port)
    nodes[6].connect_to("localhost", nodes[0].port)
    nodes[7].connect_to("localhost", nodes[0].port)
    nodes[8].connect_to("localhost", nodes[0].port)
    nodes[9].connect_to("localhost", nodes[0].port)
    nodes[10].connect_to("localhost", nodes[0].port)
    nodes[11].connect_to("localhost", nodes[0].port)
    nodes[12].connect_to("localhost", nodes[0].port)
    nodes[13].connect_to("localhost", nodes[0].port)
    print("Yes?")'''