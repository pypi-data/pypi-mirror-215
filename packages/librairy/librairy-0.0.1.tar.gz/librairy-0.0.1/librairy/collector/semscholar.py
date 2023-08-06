# Load data
from librairy import bookshelf
from librairy.collector import repository
import schedule
import requests
import os
import csv
import json

BASE_DIR = os.environ.get("BASE_DIR",".")

class SemanticScholar(repository.Repository):
    
    def __init__(self,directory="./data"):
        super().__init__("semantic_scholar",directory)
        self.authors = []

    def add_author(self,name,id):
        self.authors.append((name,id))

    def add_authors(self,authors):
        for a in authors:
            self.add_author(a['name'],a['id'])

    def retrieve(self,one_job=False):
        for author in self.authors:
            author_name = author[0]
            author_id = author[1]
            self.logger.info(f"collecting papers of: {author_name}...")
            limit = 25
            offset = 0
            pending = True
            while(pending):
                res = requests.get(f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers?fields=paperId&limit={limit}&offset={offset}")
                if (res.status_code != 200):
                    self.logger.error(f"Error getting papers: {res.text}")
                    break
                data = res.json()['data']
                pending =  (len(data) == limit)
                offset += 1
                for d in data:
                    paper_id = d['paperId']
                    paper_path = f"{paper_id}.json"
                    if (self.exists(paper_path)):
                        continue
                    self.logger.info(f"retrieving data from paper: {paper_id} ..")
                    paper_res = requests.get(f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=url,title,year,abstract,authors,venue,journal,tldr")
                    if (paper_res.status_code != 200):
                        self.logger.error(f"Error getting paper info: {paper_res.text}")
                        break
                    paper_data = paper_res.json()
                    paper_summary = ""
                    if ("abstract" in paper_data) and (paper_data['abstract'] != None):
                        paper_summary = paper_data['abstract']
                    elif ("tldr" in paper_data) and (paper_data['tldr'] != None) and (paper_data['tldr']['text'] != None):
                        paper_summary = paper_data['tldr']['text']
                    paper_description = f"**'{paper_data['title']}'**"
                    authors = [a['name']for a in paper_data['authors']]
                    paper_description += ", " + ",".join(authors)
                    paper_description += f", *{paper_data['venue']}*"
                    if ("journal" in paper_data) and (paper_data["journal"] != None):
                        if ("pages" in paper_data["journal"]):
                            paper_description += f", {paper_data['journal']['pages']}"
                    paper_description += f", {str(paper_data['year'])}"
                    self.save(paper_id,paper_data['title'],paper_description, paper_path)
                    
                    if (len(paper_summary) > 10):
                        for id,sentence in enumerate(paper_summary.split(".")):
                            self.save(f"{paper_id}_{id}",sentence,paper_description, paper_path)
        if (one_job):
            return schedule.CancelJob