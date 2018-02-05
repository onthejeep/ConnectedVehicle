'''
Created on Apr 28, 2014

@author: admshuyang
'''

import pymssql;
import pyodbc;

class Connect2MSSQL:
    
    #private attribute
    __Connection__ = None;
    
    def __init__(self):
        pass;
    
    @staticmethod
    def GetInisitance():
        if(Connect2MSSQL.__Connection__ is None):
            Connect2MSSQL.__Connection__ = pymssql.connect(host = '131.247.19.173', user = 'Shu', password='XXXX', database= 'Here'); #  SunTran     MBTA
            
        return Connect2MSSQL.__Connection__;

    @staticmethod
    def GetInisitance_ODBC():
        if(Connect2MSSQL.__Connection__ is None):
            Connect2MSSQL.__Connection__ = pyodbc.connect('DRIVER={SQL Server};SERVER=131.247.19.173;UID=Shu;PWD=XXXXX'); #  SunTran     MBTA
            
        return Connect2MSSQL.__Connection__;
