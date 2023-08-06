import os
from logging.config import dictConfig
import logging
from ..config import LogConfig


class Repository():
    
    def __init__(self,name,directory):
        dictConfig(LogConfig().dict())
        self.logger = logging.getLogger("librairy")
        self.output_dir = directory+"/"+name
        if not os.path.exists(self.output_dir):
            # If it doesn't exist, create it
            os.makedirs(self.output_dir)


    def add_bookshelf(self,bookshelf):
        self.bookshelf = bookshelf

    def exists(self,ticket):
        return os.path.exists(f"{self.output_dir}/{ticket}")
    
    def create(self,ticket):
        filepath = f"{self.output_dir}/{ticket}"
        with open(filepath, 'w') as outfile:
            outfile.write("empty")
    
    def save(self,doc_id,text,description,ticket):
        doc = {
              "document_id":doc_id,
              "text":text,
              "description":description
        }
        resp = self.bookshelf.add(doc)
        if (resp.status_code == 200) and (not self.exists(ticket)):
            self.create(ticket)