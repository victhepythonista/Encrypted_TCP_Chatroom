
## main file..run this !
from  serverinterface import ServerInterface
from client  import TCPClient


intro = """
    ENCRYPTED CHAT ROOM APPLICATION
    _______________________________


    What will you run as ?

    1 . Server [ manage connections and broadcast messages]

    2 . CLient [ connect to an existing server and start chatting ]

    3  . QUIT

    """

class Application:
    def __init__(self):
        self.running = True
    def run(self):
        
        print(intro)
        while self.running == True:
            choice = input("\n >")
            if choice == '3':
                self.running = False
            elif choice == '2':
                TCPClient().ClientInterface()
                self.running = False
                break
            elif choice == '1':
                ServerInterface().ChatRoomInterface()
                self.running = False
                break
            else:
                print("\nINVALID CHOICE")
            

if __name__ == '__main__':
    Application().run()
