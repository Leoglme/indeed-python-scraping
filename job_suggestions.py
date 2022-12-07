import requests
from database import Database
import json


class IndeedJobSuggestions:
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
    database = Database()

    def __init__(self):
        self.database.delete_all_job_suggestions()
        for letter in self.alphabet:
            self.get_job_suggestion(letter)

    def get_job_suggestion(self, letter: str):
        url = f'https://autocomplete.indeed.com/api/v0/suggestions/what?country=FR&language=fr&count=100000000' \
              f'&formatted=1&query={letter}&useEachWord=false&page=serp&showAlternateSuggestions=false&merged=true&rich=true'

        r = requests.get(url)
        self.save_job_suggestions(json.loads(r.content))
        print(json.loads(r.content))

    def save_job_suggestions(self, suggestions):
        for suggestion in suggestions:
            self.database.add_job_suggestion(suggestion["suggestion"], suggestion["payload"]["score"])
