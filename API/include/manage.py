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

def create_entity() -> int:
    '''
    Creates a new entity
    '''
    newId=random.randint(0,ID_CAP)  # Creates a new random id between 0 and the maximum ID possible
    # Loads the data into a dictionary
    with LOCK:
        with open(os.path.join(CWD,"data","entities.json"),mode="r",encoding="utf-8") as f:
            data=json.load(f)
    data[newId]=[] # Creates new dictionary associated with this ID
    # Dumps it into the file
    with LOCK:
        with open(os.path.join(CWD,"data","entities.json"),mode="r",encoding="utf-8") as f:
            json.dump(data,f)
    return newId

def fetch(id: int) -> str:
    '''
    Fetches the latest entity SHA digest
    '''
    with LOCK:
        with open(os.path.join(CWD,"data","entities.json"),mode="r",encoding="utf-8") as f:
            data=json.load(f)
    return data[id][0]

def check(id: int) -> bool:
    '''
    Checks for entity presence inside the entities.json file
    '''
    with LOCK:
        with open(os.path.join(CWD,"data","entities.json"),mode="r",encoding="utf-8") as f:
            data=json.load(f)
    return id in data.keys()

def link_entity(id: int,digest: str,timestamp: int) -> str:
    '''
    Returns the link associated with the selected update from entities.json, returns an empty string if it was not found
    '''
    with LOCK:
        with open(os.path.join(CWD,"data","entities.json"),mode="r",encoding="utf-8") as f:
            data=json.load(f)
    l=data[id]
    for u in l:
        if u["digest"]==digest:
            return u["link"]
    return ""