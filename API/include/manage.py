import json
import random
import os
import threading
import sqlite3

from include.descriptors import *
from include.const import *

#
# INCLUDES FUNCTIONS TO HANDLE THE MANAGEMENT OF THE DATA 
#

ID_CAP = 10**10 - 1
LOCK = threading.Lock()
CWD = os.getcwd()  # Get the current working directory

class Storage:
    @staticmethod
    def create_entity() -> int:
        '''
        Creates a new entity
        '''
        newId = random.randint(0, ID_CAP)
        return newId

    @staticmethod
    def fetch(id: int) -> str:
        '''
        Fetches the latest entity SHA digest
        '''
        with sqlite3.connect(os.path.join(CWD, "data", "entities.db")) as DB:
            cursor = DB.cursor()
            cursor.execute('''
                           SELECT digest
                           FROM entities
                           WHERE id=?
                           ORDER BY timestamp DESC
                           LIMIT 1
                           ''', (id,))
            result = cursor.fetchall()

            # Check if result is empty and return None or appropriate value
            return result[0][0] if result else None

    @staticmethod
    def check(id: int) -> bool:
        '''
        Checks for entity presence inside the entities table
        '''
        with sqlite3.connect(os.path.join(CWD, "data", "entities.db")) as DB:
            cursor = DB.cursor()
            cursor.execute('''
                           SELECT *
                           FROM entities
                           WHERE id=?
                           ''', (id,))
            result = cursor.fetchall()

            return len(result) != 0

    @staticmethod
    def link_entity(id: int, timestamp: int) -> str:
        '''
        Returns the link associated with the selected update from entities table, returns an empty string if it was not found
        '''
        with sqlite3.connect(os.path.join(CWD, "data", "entities.db")) as DB:
            cursor = DB.cursor()
            cursor.execute('''
                           SELECT link
                           FROM entities
                           WHERE id=? AND timestamp=?
                           ORDER BY timestamp DESC
                           ''', (id, timestamp,))
            result = cursor.fetchall()

            return result[0][0] if result else ""

    @staticmethod
    def get_timestamps(id: int) -> list:
        '''
        Returns the list of available update (timestamps) for the entity id
        '''
        with sqlite3.connect(os.path.join(CWD, "data", "entities.db")) as DB:
            cursor = DB.cursor()
            cursor.execute('''
                           SELECT timestamp
                           FROM entities
                           WHERE id=?
                           ORDER BY timestamp DESC
                           ''', (id,))
            result = cursor.fetchall()

            return [j[0] for j in result]  # Use list comprehension to create the timestamp list

    @staticmethod
    @bool_except
    def create(data: dict) -> None:
        '''
        Creates a new update
        '''
        with sqlite3.connect(os.path.join(CWD, "data", "entities.db")) as DB:
            cursor = DB.cursor()
            cursor.execute('''
                        INSERT INTO entities (id, digest, timestamp, link)
                        VALUES (?, ?, ?, ?)
                        ''', (data["id"], data["digest"], data["timestamp"], data["link"]))

            DB.commit()
