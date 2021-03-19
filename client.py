
import socket, os, datetime, threading,time

from sprkl import Sprkl 
import configs,time


s = Sprkl()
class TCPClient():

    def __init__(self, host = configs.localhost, port = configs.port):  
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address =  (host, port)
        self.port = port
        self.host = host
        self.up = True
    def standardize_message(self, message):
        # converts the message (in str form)
        # to a 1024 bit format
        header = configs.header
        additional_data = b" "*(header - len(message))
        message = message.encode(configs.enc)
        result = message + additional_data
        return result
    def send_messages(self):
        while self.up ==  True:
            try:
                data= input("~~~~~~>  :")
                data = self.standardize_message(data)
                self.sock.sendall(data )
              
            except:
                s.ntf("broke connection with server ...reconnecting")
                self.reconnect()
                time.sleep(.2)
                
    def reconnect(self):
      
        try:
            
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(self.address)
            print("successfully connected  ")
        except:
            print("reconnecting")
            
        
    def disconnect(self):
        try:
            self.sock.shutdown()
            self.sock.close()
            print("SHUT DOWN SOCKET SUCCESSSFULLT")
        except:
            s.ntf("could not close sockeet : (")
            
   
                
    def receive_messages(self):
        while self.up == True:
            try:
                message = self.sock.recv(configs.header).decode(configs.enc)
                if message == 0 or None:
                    self.reconnect()
                    time.sleep(1)
                data =message.rstrip()
                if data == '':
                    pass
                else:
                    server_mess = (f"\n [ group chat ]:\n{data}\n")
                    print(server_mess )
                
            except:
                pass

    def establish_connection(self):
        try:
            # est connnection with 
            self.sock.connect(self.address)
        except:
            print("could not connect")


    def runclient(self):
        s.ntf("establishing connection")
        self.establish_connection()
        write_messages_thread = threading.Thread(target = self.send_messages)
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()
        write_messages_thread.start()
                
    def StartChat(self):
        self.runclient()
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
    def ClientInterface(self):
        intro = """
        
        Welcome !!!
        
        You are about to connect to server
        on HOST{configs.host} on PORT   {configs.port}
        
        Do you want to cahnge the host ? Y/N"""
        print(intro)
        while True:
            ch = input("\n>")
            if ch == 'Y' :
                host = input("\nNEW  HOST (name or IP  address):")
                if host == 'X' :
                    ch = 'N'
                elif self.validate_host(host) == True:
                    self.host = host
                    self.StartChat()
                    break
                    

                else:
                    print(f"\npress X to go back\n\nINVALID HOSTNAME  [{host}]       is it connected ?")

            if ch == 'N' :
                self.StartChat()
                break
            else:
                self.ClientInterface()
                break

=
