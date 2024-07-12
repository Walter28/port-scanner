import socket
import threading
from queue import Queue
#will use socket to connected to some host host port, if the connection succed, means the port is opened

#with only threading there is more chance to scan one port twice or much, the object is to accelerate the process of scan using
#multithreding, Queue is basically like a list, it will hav all kind of element and every time that we get an element in this list
#it no longer get twice in thath list, it means we are basically Queued the element, the "port number" here

target = '127.0.0.1' # this is my own local ipadress network, change this for your network

queue = Queue()
open_ports = []

def portscan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        return True
    except:
        return False
    
#fill the queue
def fill_queue(port_list):
    for port in port_list:
        queue.put(port)
        
#the method that thread will going to be using
def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print(f"Port {port} is open")
            open_ports.append(port)
    
port_list = range(1, 1024)
fill_queue(port_list)

thread_list  = []

for t in range(100):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)
    
for thread in thread_list:
    thread.start()
    
for thread in thread_list:
    thread.join() #wait for the thread to finish after continue with the code
    
print(f"Opens ports are : {open_ports}")
