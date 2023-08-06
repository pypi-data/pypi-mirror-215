from librairy import bookshelf
import os

HOST        = "http://localhost:8000"
COLLECTION  = os.getenv("COLLECTION","MyBookshelf")
TOKEN       = os.getenv("TOKEN","None")
SERVICE     = os.environ.get("SERVICE",HOST)

def prepare(name=COLLECTION,token=TOKEN,core=SERVICE):
    return bookshelf.Bookshelf(name, token, core)
