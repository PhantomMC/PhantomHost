"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""
import socket
import os
import threading
import traceback
from pha_connection import connection_manager
from pha_json import json_creator
from pha_yaml import yaml_manager
from pha_bstats import bstats
import pha_listener
import pha_logging

Version = "0.7.0"
defaultConfig = {
        "configVersion" : 6,
        "serverInfo" : {
            "host" : "51.222.28.81",
            "port" : 25565
        },
        "Style" : 1, #chose between 1, 2 and 3
        "Content" : {
            "lowerMessage" : "A message",
            "upperMessage": "This msg appears above the server!",
            "hoverMessage" : "You should have brought a config",
            "kickMessage" : "Angry",
            "imagePath" : "Logo.png"
        },
        "Logging" : {
                "log" : False,
                "storeUsers":True
             },
        "debug" : False
        }


class Server(threading.Thread):
    def __init__(self, config, logger):
        threading.Thread.__init__(self)
        self.logger = logger
        self.setConfig(config)
        
        self.isRunning = True
        msg = "<Phantom V."+Version+"> Listening on port " + str(config["serverInfo"]["port"])
        self.logger.printMsg(msg)
        
    def run(self):
        restart = False
        try:
            self.listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listeningSocket.bind((self.host, self.port))
            i = 1
            while self.isRunning:
                self.listeningSocket.listen(0)
                conn, addr = self.listeningSocket.accept()
                conn_mngr = connection_manager(conn,self.json_creator,self.logger,i,addr)
                conn_mngr.start()
                i += 1
            print("This will never get triggered, but has to be here because of python")
        except socket.timeout:
            restart = True
            self.logger.error(traceback.format_exc())
        except OSError as e:
            # OSError 10038 is something that gets thrown everytime when the server is closed
            if not (e.args[0] == 10038):
                self.logger.error(traceback.format_exc())
        except:
            self.logger.error(traceback.format_exc())
        finally:
            self.logger.info("closed server on port " + str(self.port))
            self.close()
            
        if(restart):
            self.run()
            
    def close(self):
        self.isRunning = False
        self.listeningSocket.close()
        
    def setConfig(self,config):
        self.config = config
        self.json_creator = json_creator(config,self.logger)
        self.host = self.config["serverInfo"]["host"]
        self.port = self.config["serverInfo"]["port"]

class Phantom:
    def __init__(self,config):
        self.logger = pha_logging.logger()
        plugin_id = 10892
        bstats(plugin_id).start()

        self.servers = {}
        port = 10390
        pha_listener.CommandListener(port,self,self.logger)
    
    def start(self):
        
        while(True):
            command = input()
            if command.lower() == "stop" or command.lower() == "exit":
                os._exit(1)
                break;
            if command.lower() == "restart":
                print("not implemented yet")
                continue
            print("unknown command " + command.lower())
                    
    def addServer(self,userName,config):
        self.logger.debug("adding server",userName)
        self.servers[userName] = Server(config,self.logger)
        self.servers[userName].start()
    
    def removeServer(self,userName):
        self.servers[userName].close()
        del self.servers[userName]
        
    def reloadServer(self, userName, config):
        self.servers[userName].setConfig(config)

is_config = True
config_path = "config"
config_retriever = yaml_manager(defaultConfig,config_path,is_config)
config = config_retriever.get_yml()
instance = Phantom(config)
instance.start()