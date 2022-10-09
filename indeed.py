import time
import requests
from bs4 import BeautifulSoup
import re
from termcolor import cprint
from colorama import init
from database import Database


class Indeed:
    start = 0
    step_page = 10
    sleep = 10
    jobs = []
    jobs_indeed_id = []
    job_cards_class = 'job_seen_beacon'
    count_and_sort_class = 'jobsearch-JobCountAndSortPane-jobCount'
    company_class = 'companyName'
    salary_class = 'salary-snippet-container'
    description_class = 'job-snippet'
    database = Database()

    # Job Fields
    title = None
    description = None
    salary = None
    place = None
    indeed_id = None
    company = None

    def __init__(self, types_job: [], cities: []):
        print('starting...')
        init()
        # self.database.delete_all_job()
        self.jobs_indeed_id = self.database.get_all_job_indeed_id()
        self.url = None
        self.types_job = types_job
        self.cities = cities

    def run(self):
        for type_job in self.types_job:
            for city in self.cities:
                self.get_html_page(type_job, city)
                self.reset()
        self.database.close_connect()
        print(f'Paused for {self.sleep} seconds')
        time.sleep(self.sleep)
        self.run()

    def reset(self):
        self.jobs.clear()
        self.start = 0

    def get_html_page(self, type_job: str, city: str):
        self.url = f'http://fr.indeed.com/emplois?q={type_job}&l={city}&radius=0&fromage=1&vjk=8651b9be54b7b5ef' \
                   f'&start={self.start}&sort=date'
        agent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/104.0.0.0 '
                          'Safari/537.36 Vivaldi/5.3.2679.70.'}
        r = requests.get(self.url, headers=agent)
        soup = BeautifulSoup(r.content, 'html.parser')
        self.get_page_data(soup, type_job, city)

    def get_page_data(self, soup, type_job: str, city: str):
        try:
            job_cards = soup.find_all('div', class_=self.job_cards_class)
            count_and_sort = soup.find('div', class_=self.count_and_sort_class).text.strip()
            cprint(f'{count_and_sort}, {type_job}', "yellow")
            per_page = len(job_cards)
            current_page = int(re.search("(?<=Page)(.*)(?=de)", count_and_sort).group(0).replace(' ', ''))
            max_results = int(
                re.search("(?<=de)(.*)(?=emplois)", count_and_sort).group(0).replace(',', '').replace(' ', ''))

            self.print_job(per_page, current_page, max_results)
            self.get_jobs_data(job_cards, city)

            if len(self.jobs) <= (max_results - per_page):
                if self.indeed_id not in self.jobs_indeed_id:
                    self.start += self.step_page
                    self.get_html_page(type_job, city)
        except:
            pass

    def get_jobs_data(self, job_cards, city: str):

        for job in job_cards:
            self.title = job.find('a').text.strip()
            link = job.find('a')

            if link is not None:
                self.indeed_id = link['data-jk']
                if self.indeed_id in self.jobs_indeed_id:
                    cprint(f'Job with id {self.indeed_id} already exist', 'red')
                    break
                self.jobs_indeed_id.append(self.indeed_id)

            self.company = job.find('span', class_=self.company_class).text.strip()

            salary = job.find('div', class_=self.salary_class)

            if salary is not None:
                self.salary = salary.text.strip()
            self.description = job.find('div', class_=self.description_class).text.strip()
            self.place = city
            self.save_job()

    def save_job(self):
        self.jobs.append({
            'indeed_id': self.indeed_id,
            'title': self.title,
            'salary': self.salary,
            'description': self.description,
            'place': self.place
        })
        self.database.add_job(self.title, self.description, self.salary, self.place, self.indeed_id)

    def print_job(self, per_page, current_page, max_results):
        cprint(self.url, 'cyan')

        infos = {
            "per_page": per_page,
            "current_page": current_page,
            "start": self.start,
            "max_results": max_results,
            "number_jobs": len(self.jobs),
        }

        cprint(f"{infos}", 'green')


database = Database()
job_types = database.get_job_types()

indeed = Indeed(job_types, ["France"])
indeed.run()
