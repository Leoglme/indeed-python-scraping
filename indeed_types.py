import requests
import json
from database import Database
from bs4 import BeautifulSoup
import re


class IndeedJobTypes:
    database = Database()

    def __init__(self):
        self.get_types()

    def get_types(self):
        url = f'http://fr.indeed.com/jobs?q=d&l=France&vjk=b0ee7f3282b7aa83'
        agent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/104.0.0.0 '
                          'Safari/537.36 Vivaldi/5.3.2679.70.'}

        r = requests.get(url, headers=agent)
        content = BeautifulSoup(r.content, 'html.parser')
        try:
            content = content.find('ul', {"id": "filter-jobtype-menu"}).text.replace(',', '')
            types = re.findall("[$A-Za-zéèà\s-]+", content)
            self.save_types(types)

        except:
            pass

    def save_types(self, types):
        for type in types:
            self.database.add_job_type(type.strip())


indeed_job_types = IndeedJobTypes()
