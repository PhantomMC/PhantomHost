# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 
 @author: Thorin
"""
from time import strftime, localtime
import os
from os import path

def list_to_string(alist):
    output = ""
    for item in alist:
        if type(item) is bytes:
            try:
                item = str(item.decode("utf8"))
            except:
                item = str(item)
        elif type(item) is not str:
            item = str(item)
        
        output = output + " " + item
        
    return output
        
def write_time():
    return strftime("%y.%m.%d@%H:%M", localtime())


class logger:
    def __init__(self,isLogMsgs = False,isDebug = False):
        
        if not os.path.exists("log"):
            os.mkdir("log")
        
        self.isLogMsgs = isLogMsgs
        self.isDebug = isDebug
        self.file_path = "log"
            
        
        self.create_new_log()
        
    def info(self,*msg):
        end_msg = " [INFO]" + list_to_string(msg)
        self.printMsg(end_msg)
    
    def debug(self,*msg):
        if self.isDebug:
            end_msg = " [DEBUG]" + list_to_string(msg)
            self.printMsg(end_msg)
            
    def error(self, *msg):
        end_msg = " [ERROR]" + list_to_string(msg)
        self.printMsg(end_msg)
    
    def warning(self, *msg):
        end_msg = " [WARNING]" + list_to_string(msg)
        self.printMsg(end_msg)
        
    def printMsg(self, msg):
        msg = write_time() + msg;
        self.write_to_file(msg)
        print(msg)
        
    def register_user(self,client_port,client_address,client_username):
        msg = "from " + client_address + ":" + str(client_port)
        
        if client_username is not None:
            msg = "Connection as " + client_username.decode("utf8") +" "+ msg
            self.info(msg)
            return
        
        self.debug("Connection "+msg)
        
        
        
        
    def create_new_log(self):
        if path.exists(self.file_path+"/pings.log"):
            self.rename_old_log()
    def rename_old_log(self):
        i = 1
        while path.exists(self.file_path+"/pings"+ str(i) +".old"):
            i += 1
        os.rename(self.file_path+"/pings.log", self.file_path+"/pings"+ str(i) +".old")
        
    def write_to_file(self,msg):
        if not self.isLogMsgs:
            return
        
        with open(self.file_path + "/pings.log","a") as file:
            file.writelines(msg + "\n")
    
    
    