import requests
from database import Database
import json


class IndeedTypesJob:
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
    database = Database()
    types_job = []

    def __init__(self):
        for letter in self.alphabet:
            self.get_types_job(letter)
        self.save_jobs()

    def get_types_job(self, letter: str):
        url = f'https://autocomplete.indeed.com/api/v0/suggestions/what?country=FR&language=fr&count=100000000' \
              f'&formatted=1&query={letter}&useEachWord=false&page=serp&showAlternateSuggestions=false&merged=true&rich=true '
        r = requests.get(url)
        self.types_job += json.loads(r.content)

    def save_jobs(self):
        for type_job in self.types_job:
            self.database.add_job_type(type_job["suggestion"], type_job["payload"]["score"])
        self.database.close_connect()


indeed_types_job = IndeedTypesJob()
