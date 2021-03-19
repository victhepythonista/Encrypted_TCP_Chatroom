
import socket, os, datetime, threading,random, sys

from sprkl import Sprkl 
import configs
from logger import Logger

logr = Logger()



s = Sprkl()
class TCPServer( ):
    def __init__(self, localhost_or_ip, port):
        self.clients = []
        self.names = []
        self.server_log = ""
        self.server_name = "testserver"
        self.address = (localhost_or_ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.up = True

    def receive_message(self, conn,addr):
        
        try:
            while self.up == True:
                data = conn.recv(configs.header).decode(configs.enc)
                
                
                if data == 0 or None:
                    
                    self.remove_client(conn, addr)
                    logr.log(f"{addr} disconnected")
                    print(addr," JUST LEFT THE CHAT")
                    self.broadcast_message(s.ntf("  has left the chat"))
                    break
                
                data = data.rstrip()
                broadcast = f"[ {addr} ] : \n    {data}\n------------------------"
                self.broadcast_message(broadcast)
               
                self.send_message(data, conn)
                
            
                   
        except:
            print(addr, "is silent but can send messages")
            pass
           
     
                    

  
        
    def send_message(self,  mess,conn):
        
        try:
            logr.log(f"\n[ message sent  to   SUCCESSFULLY]")
            conn.send(self.standardize_message(mess))
        except:
            print("could not  send ")
            print(conn)
            pass
  
    def add_client(self, conn, addr):
        self.clients.append([addr,conn])
    def remove_client(self, conn, addr):
        if [addr[0], conn] in self.clients:
            self.clients.pop(self.clients.index([addr, conn]))
            self.disconnect_client(conn,addr)
            s.ntf('disconnected {addr}')
        else:
            logr.log("could not remove {addr}\n")
            print(self.clients)
    def kill_server(self):
        
        try:
            s.ntf("killling connnections")
            if self.clients !=[]:
                for conn in self.clients:
                    self.remove_client(conn[1], conn[0])
                    s.ntf(f"REMOVED {conn[0]}")
                    s.ntf("killed connections")
            self.sock.shutdown()
            self.sock.close()
            print("Server closed")
            self.up = False
    

        except:
            sys.exit()
            print("could not shut down properly...........\n................\n...............")

    def handle_connection(self, conn, addr):
        # handle client connection
        s.ntf("handling client")
        s.ntf(f" {addr[0]}    client added to logs")
        try:
            receive_from_client = threading.Thread(target=self.receive_message, args = (conn,addr))
            receive_from_client.start()
        except:
            s.ntf("problem handling client..disconnecting")
        s.ntf("client handled")
      
    def disconnect_client(self, conn, addr):
        try:
            print(f"\nDISCONNECTING  CLIENT  \n ", addr)
            self.broadcast_message(f"{addr}  has left the chat")
       
            Logger().log(self.server_log)
            conn.shutdown()
            conn.close()
            s.ntf("disconnected client successfully")
            print(conn)
        except:
            print("WE COULD NOT DISCONNECT ")

        

    def broadcast_message(self, message):
        # broadcast message to clients
       

        message = self.standardize_message(message)
        
        for conn in self.clients:
            try:
                print(conn)
                self.send_message(message, conn)
            except:
                 
                s.ntf('could not broadcast meassage')
        print(type(message), s.ntf("message type"))
       


    def standardize_message(self, message):
        # converts the message (in str form)
        # to a 1024 bit format
        header = configs.header
        additional_data = b" "*(header - len(message))
        message = message.encode(configs.enc)
        result = message + additional_data
        return result
    def receive_connections(self):
        self.sock.listen()
        while self.up == True:
            print("connecting.........")
            try:

                conn, addr = self.sock.accept()
            
                self.add_client(conn, addr[0])
                
                addr = addr[0]
                print("address",addr)
                print(type(conn) , 'CONNECTION')
                print(f"[CONNECTION  FROM  {addr}]")
                self.broadcast_message(f"{addr}  has  joined the chat")
                client_thread = threading.Thread(target=self.handle_connection, args= (conn, addr))
                client_thread.start()
            except:
                self.receive_connections()
                s.ntf("RESTARTING  CONNECTIONS HANDLER")
                pass

            


    def server_terminal(self):
        while self.up == True:
            try:

                command = input("~# ")
                if command == 'kill':
                    self.up = False
                    self.kill_server()
                elif command == 'users':
                    print(self.clients, self.names)
                elif command == 'stats':
                    s.ntf("-----------  SERVER  STATS ------------")
                    print(f"""THREADS  :   {threading.active_count()}""")
                    print(f for f in self.clients)

            except:
                s.ntf('terminal has shut down')


    def start_server(self):
        # starts the server
        print("server starting on \n\n" , self.address, '\n')
        self.sock.bind(self.address)
        self.sock.listen(5)
        
        s.ntf("server starting")
        
        s.ntf('address  is ok ..setting up')
        terminal = threading.Thread(target=self.server_terminal)
        receive_connections_thread = threading.Thread(target = self.receive_connections)

        receive_connections_thread.start()
        terminal.start()
        

      
        


