# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 22:14:11 2021

@author: 46737
"""
import sys
import subprocess
import pkg_resources


def install(package):
    installed = {pkg.key for pkg in pkg_resources.working_set}
    if(package not in installed):
        python = sys.executable
        subprocess.check_call([python, '-m', 'pip', 'install', package])
        
install("pymongo")
import pymongo

class MongoDb:
    def __init__(self,databaseName):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.database = self.client(databaseName)