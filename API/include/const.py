import os
import sqlite3
#
# WRAPPER FILE FOR SOME GENERAL PURPOSE CONSTANTS
#

CWD=os.getcwd()
SUCCESSFUL=200
INTERNAL_ERROR=500
BAD_REQUEST=400
NOT_FOUND=404
UNAUTHORIZED=401
with open(os.path.join(CWD,"data","key.txt"),mode="r",encoding="utf-8") as f:
    KEY=f.read()
DB=sqlite3.connect(os.path.join(CWD,"data","entities.db"))