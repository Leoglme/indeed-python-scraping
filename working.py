import requests
from bs4 import BeautifulSoup
import re

jobs = []


def extract(start):
    url = f'http://fr.indeed.com/jobs?q=poids+lourd&l=Iffendic+%2835%29&vjk=32347f99399e3c06&start={start}&sort=date'
    agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 '
                      'Safari/537.36 Vivaldi/5.3.2679.70.'}
    r = requests.get(url, headers=agent)
    soup = BeautifulSoup(r.content, 'html.parser')
    transform(soup, start)


def transform(soup, start):
    job_cards = soup.find_all('div', class_='job_seen_beacon')
    count_and_sort = soup.find('div', class_='jobsearch-JobCountAndSortPane-jobCount').text.strip()

    per_page = len(job_cards)
    current_page = int(re.search("(?<=Page)(.*)(?=de)", count_and_sort).group(0).replace(' ', ''))
    max_results = int(re.search("(?<=de)(.*)(?=emplois)", count_and_sort).group(0).replace(',', '').replace(' ', ''))

    for job in job_cards:
        title = job.find('a').text.strip()
        company = job.find('span', class_='companyName').text.strip()
        salary = job.find('div', class_='salary-snippet-container')
        if salary is not None:
            salary = salary.text.strip()
        description = job.find('div', class_='job-snippet').text.strip()

        jobs.append({
            'title': title,
            'company': company,
            'salary': salary,
            'description': description
        })

    if (per_page * current_page) < max_results:
        print(f'Get {per_page} job of page {current_page} => START: {start + 10}')
        extract(start + 10)


extract(0)

print(len(jobs))
