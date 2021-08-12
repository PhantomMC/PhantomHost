import threading
import traceback
import socket

class CommandListener(threading.Thread):
    def __init__(self, port, phantomInstance,logger):
        threading.Thread.__init__(self)
        self.phantomInstance = phantomInstance
        self.port = port
        self.logger = logger
        self.listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def run(self):
        try:
            self.listeningSocket.bind((self.host, self.port))
        except socket.timeout:
            restart = True
            self.logger.error(traceback.format_exc())
        except Exception:
            self.logger.error(traceback.format_exc())
        finally:
            self.close()
            
        if(restart):
            self.run()
            
    def close(self):
         self.listeningSocket.close()