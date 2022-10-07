import requests
from bs4 import BeautifulSoup


def extract(start):
    url = f'http://fr.indeed.com/jobs?q=job+%C3%A9tudiant&l=rennes&start={start}'
    agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.70.'}
    r  = requests.get(url, headers=agent)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    jobs = soup.find_all('div', class_ = 'job_seen_beacon')
    for job in jobs:
        title = job.find('a').text
        print(title)

c = extract(0)
print(transform(c))