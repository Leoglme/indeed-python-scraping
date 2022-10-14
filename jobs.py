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
    agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.0.0 '
                      'Safari/537.36 Vivaldi/5.3.2679.70.'}

    def __init__(self, cities: []):
        database.delete_all_job()
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
            short_description = self.get_job_short_description(job_card)
            salary = self.get_job_salary(job_card)
            place = self.get_job_place(job_card)
            indeed_id = self.get_job_indeed_id(job_card)

            # Detail Job
            html_job = self.get_html_details_job(indeed_id)
            description = self.get_job_description(html_job)
            qualifications = self.get_job_qualifications(html_job)
            advantages = self.get_job_advantages(html_job)
            job_types = self.get_job_types(html_job)

            job = {
                'title': title,
                'short_description': short_description,
                'description': description,
                'qualifications': qualifications,
                'salary': salary,
                'place': place,
                'indeed_id': indeed_id
            }

            self.jobs.append(job)

            job_id = self.save_job(job)

            database.add_advantage_advertisements(advantages, job_id)
            database.add_job_types(job_types, job_id)

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

        r = requests.get(self.url, headers=self.agent)
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
    def get_job_short_description(job_card):
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

    def get_html_details_job(self, indeed_id: str):
        try:
            # url = f'http://fr.indeed.com/viewjob?jk={indeed_id}'
            url = f'http://fr.indeed.com/viewjob?jk=c7ec4978f5b1a60a'
            cprint(url, 'magenta')

            r = requests.get(url, headers=self.agent)
            return BeautifulSoup(r.content, 'html.parser')
        except:
            pass

    @staticmethod
    def get_job_types(html_job):
        try:
            job_details_section = html_job.find('div', id='jobDetailsSection')
            children = job_details_section.findChildren("div", recursive=True)
            childs = []
            for child in children:
                childs.append(child.text)
            cut_index = childs.index("Type de contrat") - 1

            return childs[-cut_index:]
        except:
            pass

    @staticmethod
    def get_job_description(html_job):
        try:
            return html_job.find('div', id='jobDescriptionText').text.strip()
        except:
            pass

    @staticmethod
    def get_job_qualifications(html_job):
        try:
            return html_job.find('div', class_='jobsearch-ReqAndQualSection-item--closedBullets').text.strip()
        except:
            pass

    @staticmethod
    def get_job_advantages(html_job):
        try:
            ads = []
            advantages = html_job.find_all('div', class_='ecydgvn1')
            for advantage in advantages:
                database.add_advantage(advantage.text.strip())
                ads.append(advantage.text.strip())
            return ads
        except:
            pass

    def save_job(self, job):
        try:
            return database.add_job(job)
        except:
            cprint(f'Id {job["indeed_id"]} already exist', 'red')


c = database.get_places()
indeed_jobs = IndeedJobs(c)
indeed_jobs.run()
