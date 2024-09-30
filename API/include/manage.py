import json
import random
import os
import threading
    
from include.descriptors import *
from include.const import *
    
    
#
# INCLUDES FUNCTIONS TO HANDLE THE MANAGEMENT OF THE DATA 
#
    
ID_CAP=10**10-1
LOCK=threading.Lock()

class Storage:
    @staticmethod
    def create_entity() -> int:
        '''
        Creates a new entity
        '''
        newId=random.randint(0,ID_CAP)
        return newId
    
    @staticmethod
    def fetch(id: int) -> str:
        '''
        Fetches the latest entity SHA digest
        '''
        cursor=DB.cursor()
        cursor.execute('''
                       SELECT digest
                       FROM entities
                       WHERE id=?
                       ORDER_BY timestamp DESC
                       LIMIT 1
                       ''',(id,))
        result=cursor.fetchall()
        cursor.close()
        return result[0][0]
    
    @staticmethod
    def check(id: int) -> bool:
        '''
        Checks for entity presence inside the entities.json file
        '''
        cursor=DB.cursor()
        cursor.execute('''
                       SELECT *
                       FROM entities
                       WHERE id=?
                       ''',(id,))
        result=cursor.fetchall()
        cursor.close()
        return len(result)!=0
    
    @staticmethod
    def link_entity(id: int,timestamp: int) -> str:
        '''
        Returns the link associated with the selected update from entities.json, returns an empty string if it was not found
        '''
        cursor=DB.cursor()
        cursor.execute('''
                       SELECT link
                       FROM entities
                       WHERE id=?,timestamp=?
                       ORDER_BY timestamp DESC
                       ''',(id,timestamp,))
        result=cursor.fetchall()
        cursor.close()
        return result[0][0]
    
    @staticmethod
    def get_timestamps(id: int) -> list:
        '''
        Returns the list of available update (timestamps) for the entity id
        '''
        cursor=DB.cursor()
        cursor.execute('''
                       SELECT timestamp
                       FROM entities
                       WHERE id=?
                       ORDER_BY timestamp DESC
                       ''',(id,))
        result=cursor.fetchall()
        cursor.close()
        timestamps=[0]*len(result)
        for i,j in enumerate(result):
            timestamps[i]=j[0]
        return timestamps
    
    @staticmethod
    @bool_except
    def create(data: dict) -> None:
        '''
        Creates a new update
        '''
        cursor=DB.cursor()
        cursor.execute('''
                       INSERT INTO entities
                       VALUES (id=?,digest=?,timestamp=?,link='?')
                       ''',(data["id"],data["digest"],data["timestamp"],data["link"]))
        DB.commit()
        cursor.close()