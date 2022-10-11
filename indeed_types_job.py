import requests
from database import Database
import json


class IndeedTypesJob:
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
    database = Database()

    def __init__(self):
        self.database.delete_all_job_types()
        for letter in self.alphabet:
            self.get_types_job(letter)

    def get_types_job(self, letter: str):
        url = f'https://autocomplete.indeed.com/api/v0/suggestions/what?country=FR&language=fr&count=100000000' \
              f'&formatted=1&query={letter}&useEachWord=false&page=serp&showAlternateSuggestions=false&merged=true&rich=true'

        r = requests.get(url)
        self.save_jobs(json.loads(r.content))
        print(json.loads(r.content))

    def save_jobs(self, jobs):
        for type_job in jobs:
            self.database.add_job_type(type_job["suggestion"], type_job["payload"]["score"])


indeed_types_job = IndeedTypesJob()
