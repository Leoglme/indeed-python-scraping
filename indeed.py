import json
import time
import requests
from bs4 import BeautifulSoup
import re
from termcolor import cprint
from colorama import init


class Indeed:
    start = 0
    step_page = 10
    sleep = 10
    jobs = []
    job_cards_class = 'job_seen_beacon'
    count_and_sort_class = 'jobsearch-JobCountAndSortPane-jobCount'
    company_class = 'companyName'
    salary_class = 'salary-snippet-container'
    description_class = 'job-snippet'
    json_file_name = 'indeed.json'

    def __init__(self, job: str, city: str):
        self.url = None
        self.job = job
        self.city = city

    def run(self):
        self.get_html_page()
        self.write_json()
        print(f'Paused for {self.sleep} seconds')
        time.sleep(self.sleep)
        self.run()

    def write_json(self):
        with open(self.json_file_name, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, ensure_ascii=False, indent=4)
        self.reset()

    def reset(self):
        self.jobs.clear()
        self.start = 0

    def get_html_page(self):
        self.url = f'http://fr.indeed.com/emplois?q={self.job}&l={self.city}&radius=0&fromage=1&vjk=8651b9be54b7b5ef' \
                   f'&start={self.start}&sort=date'
        agent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/104.0.0.0 '
                          'Safari/537.36 Vivaldi/5.3.2679.70.'}
        r = requests.get(self.url, headers=agent)
        soup = BeautifulSoup(r.content, 'html.parser')
        self.get_page_data(soup)

    def get_page_data(self, soup):
        job_cards = soup.find_all('div', class_=self.job_cards_class)
        count_and_sort = soup.find('div', class_=self.count_and_sort_class).text.strip()
        per_page = len(job_cards)
        current_page = int(re.search("(?<=Page)(.*)(?=de)", count_and_sort).group(0).replace(' ', ''))
        max_results = int(
            re.search("(?<=de)(.*)(?=emplois)", count_and_sort).group(0).replace(',', '').replace(' ', ''))

        if len(self.jobs) <= (max_results - per_page):
            self.get_jobs_data(job_cards)
            self.print_job(per_page, current_page, max_results)
            self.start += self.step_page
            self.get_html_page()

    def get_jobs_data(self, job_cards):
        for job in job_cards:
            title = job.find('a').text.strip()
            company = job.find('span', class_=self.company_class).text.strip()
            salary = job.find('div', class_=self.salary_class)
            if salary is not None:
                salary = salary.text.strip()
            description = job.find('div', class_=self.description_class).text.strip()

            self.save_job(title, company, salary, description)

    def save_job(self, title, company, salary, description):
        self.jobs.append({
            'title': title,
            'company': company,
            'salary': salary,
            'description': description
        })

    def print_job(self, per_page, current_page, max_results):
        init()
        cprint(self.url, 'cyan')

        infos = {
            "per_page": per_page,
            "current_page": current_page,
            "start": self.start + self.step_page,
            "max_results": max_results,
            "number_jobs": len(self.jobs),
        }

        cprint(f"{infos}", 'green')


indeed = Indeed("développeur", "Nantes")
indeed.run()
