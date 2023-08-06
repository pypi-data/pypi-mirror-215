from librairy import collector
import requests
import os
import hashlib
import uuid
import logging
import schedule
import time
from logging.config import dictConfig
import logging
from .config import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("librairy")


class Bookshelf():

    def __init__(self, name, token, core):
        self.name = name
        self.headers = {'Authorization': f"Bearer {token}"}
        self.core = core

    def set_credentials(self, token):
        self.headers = {'Authorization': f"Bearer {token}"}

    def set_name(self, name):
        self.name = name

    def set_core(self, core):
        self.core = core

    def is_valid_uuid(self, val):
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False

    def get_uuid(self, id):
        if (self.is_valid_uuid(id)):
            return id
        hash_object = hashlib.md5((id).encode())
        return str(uuid.UUID(hash_object.hexdigest()))


    def add(self, doc):
        doc['document_id'] = self.get_uuid(doc['document_id'])
        doc['index'] = self.name    
        resp =  requests.post(f'{self.core}/add', headers=self.headers, json = doc)
        if (resp.status_code != 200):
            logger.warn(resp.text)
        return resp
    
    def remove(self, doc_id):
        request = {
            "index": self.name,
            "document_id": self.get_uuid(doc_id)
        }        
        logger.debug(f"Delete: {request}")
        resp = requests.post(f'{self.core}/remove', headers=self.headers, json = request)
        if (resp.status_code != 200):
            logger.warn(resp.text)
        return resp
    

    def ask(self, question, limit=1):
        request = {
            "index": self.name,
            "text": question,
            "limit" : limit
        }        
        return requests.post(f'{self.core}/ask', headers=self.headers, json = request)

    def search(self, query, limit=2):
        request = {
            "index": self.name,
            "text": query,
            "limit" : limit
        }
        return requests.post(f'{self.core}/search', headers=self.headers, json = request)

    
    def add_collector(self, collector, interval, initial_delay=0):
        collector.add_bookshelf(self)
        schedule.every(initial_delay).minutes.do(collector.retrieve, one_job=True)
        schedule.every(interval).minutes.do(collector.retrieve)
