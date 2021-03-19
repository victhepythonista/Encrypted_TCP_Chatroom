## for logging in server data into our database
import datetime,sprkl

s= sprkl.Sprkl()
class Logger:
    def __init__(self):
        self.logfile = 'data.logg'

    
    def log(self, data):
        date = datetime.datetime.now().strftime("%Y : %m : %d :%H :%M")
        
        try:
            prev = ""
            with open(self.logfile, 'r') as f:
                prev = f.read()
                f.close()
            with open(self.logfile, 'w') as f:
                f.write(prev + "\n\n\n\n" +date + "\n"+ data)
        except:
            try:
                with open(self.logfile, 'w') as l:
                    l.write('')
                    l.close()
            except:
                print("we cant log this data")
            self.log(data)
            

    
#Logger().log("haaaaatchuuu")


   