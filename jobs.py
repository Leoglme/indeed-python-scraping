import requests
from colorama import init
from bs4 import BeautifulSoup
from termcolor import cprint
import re
import time
from database import Database

database = Database()


class IndeedJobs:
    sleep = 10
    start = 0
    current_page = 0
    number_jobs_added = 0
    jobs = []

    def __init__(self, cities: []):
        self.stop = False
        print('starting...')
        init()
        self.jobs_indeed_id = database.get_all_job_indeed_id()
        self.url = None
        self.cities = cities

    def stop_search(self):
        self.stop = True
        self.start = 0

    def run(self):
        for city in self.cities:
            self.jobs_indeed_id = database.get_all_job_indeed_id()
            self.number_jobs_added = 0
            self.stop = False
            self.read_pages(city)

        print(f'Paused for {self.sleep} seconds')
        time.sleep(self.sleep)
        self.run()

    def read_pages(self, city: str):
        html_jobs = self.get_html_jobs(city)

        job_cards = self.get_job_cards(html_jobs)
        self.current_page = self.get_current_page(html_jobs)
        max_results = self.get_max_results(html_jobs)

        cprint(f'Page {self.current_page} de {max_results} emplois, {city}', "yellow")

        for job_card in job_cards:
            title = self.get_job_tile(job_card)
            description = self.get_job_description(job_card)
            salary = self.get_job_salary(job_card)
            place = self.get_job_place(job_card)
            indeed_id = self.get_job_indeed_id(job_card)

            job = {
                'title': title,
                'description': description,
                'salary': salary,
                'place': place,
                'indeed_id': indeed_id
            }

            self.jobs.append(job)

            self.save_job(job)

            self.number_jobs_added += 1

        if not self.stop:
            infos = {
                "current_page": self.current_page,
                "max_results": max_results,
                "number_jobs_added": self.number_jobs_added,
                "number_jobs": len(self.jobs),
            }

            cprint(f"{infos}", 'green')

            if len(self.jobs) <= (max_results - len(job_cards)):
                self.start += 10
                self.read_pages(city)

    def get_html_jobs(self, city: str):
        self.url = f'http://fr.indeed.com/jobs?q=&l={city}&sort=date&fromage=1&start={self.start}'
        cprint(self.url, 'cyan')
        agent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/104.0.0.0 '
                          'Safari/537.36 Vivaldi/5.3.2679.70.'}
        r = requests.get(self.url, headers=agent)
        return BeautifulSoup(r.content, 'html.parser')

    def get_current_page(self, html_jobs):
        try:
            return html_jobs.find('button', {"data-testid": "pagination-page-current"}).text
        except:
            self.stop_search()

    @staticmethod
    def get_job_cards(html_jobs):
        return html_jobs.find_all('div', class_='job_seen_beacon')

    def get_count_and_sort(self, html_jobs):
        try:
            return html_jobs.find('div', class_='jobsearch-JobCountAndSortPane-jobCount').text.strip()
        except:
            self.stop_search()

    @staticmethod
    def get_job_tile(job_card):
        return job_card.find('a').text.strip()

    @staticmethod
    def get_job_description(job_card):
        return job_card.find('div', class_='job-snippet').text.strip()

    @staticmethod
    def get_job_place(job_card):
        return job_card.find('div', class_='companyLocation').text.strip()

    @staticmethod
    def get_job_indeed_id(job_card):
        indeed_id = None
        link = job_card.find('a')
        if link is not None:
            indeed_id = link['data-jk']
        return indeed_id

    @staticmethod
    def get_job_salary(job_card):
        salary = job_card.find('div', class_='salary-snippet-container')

        if salary is not None:
            salary = salary.text.strip()
        return salary

    def get_max_results(self, html_jobs):
        try:
            count_and_sort = self.get_count_and_sort(html_jobs)
            return int(re.search("(?<=de)(.*)(?=emplois)", count_and_sort).group(0).replace(',', '').replace(' ', ''))
        except:
            self.stop_search()

    def get_html_job(self):
        pass

    def save_job(self, job):
        try:
            database.add_job(job)
        except:
            cprint(f'Id {job["indeed_id"]} already exist', 'red')


c = database.get_places()
indeed_jobs = IndeedJobs(c)
indeed_jobs.run()
