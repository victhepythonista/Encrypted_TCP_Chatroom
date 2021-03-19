### START UP THE SERVER HERE

## 
import socket
import configs
from server import TCPServer
from sprkl import Sprkl



s = Sprkl()
host = "127.0.0.1"
port = configs.port

intro = f"""
WELCOME !!
The ChatRoom server is starting

it will start on
    HOST : {host}
    PORT : {port}

    The port name can (for now ) be changed
    by changing port[variable] in 
    configs.py 



    @victhepythonista.github.com


    """

class ServerInterface:
    ## chat room class
    ## this initiates the  server   and   someone else can 
    ## also connect through  running client .py

    def __init__(self):
        self.port = configs.port
        self.host = host
        self.server = None
        self.running = True
  
    def validate_host(self, host):
        # validate if a host is real by creating and closing
        # a test socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((host,self.port))
            sock.shutdown()
            sock.close()
            s.ntf("valid host")
            return True
        except:
         
            s.ntf("invalid host  ..please check again ")
            return False

    def StartServer(self):
        ## after all requirements are met
        # we create and activate our TCPServer  Class
        #  
        input("\n ENTER ANY KEY TO START SERVER :")
        s.ntf("\n---------------starting  server---------------")
        self.server =TCPServer(self.host, self.port)
        self.server.start_server()
    def ChatRoomInterface(self):
        ## interface  for  server setup
        # 
        print(intro)
        ch = input("\ndo you wish to change the  host ??  Y/N :")
        ## if you dont want to change anything
        # just enter 'M'
        while self.running == True:
            
            if ch == 'Y' :
                host = input("\nNEW  HOST (name or IP  address):")
                if host == 'X' :
                    ch = 'N'
                elif self.validate_host(host) == True:
                    self.host = host
                    self.StartServer()
                    break
                   

                else:
                    print(f"\npress X to go back\n\nINVALID HOSTNAME  [{host}]       is it connected ?")

            if ch == 'N' :
               self.StartServer()
               break
            else:
                self.ChatRoomInterface()
                break


                
        
      
       

