import json
import requests

results = []
job_types = ['developpeur', 'eboueur']
cities = ['Rennes', "caen"]
api_key = '###'
start = 0


def get_google_jobs(job_type: str, city: str, s: int):
    print({
        'start': s,
        'job_type': job_type,
        'city': city
    })
    url = f'https://serpapi.com/search.json?engine=google_jobs&q={job_type}+{city}&hl=fr&api_key={api_key}&start={s}'
    req = requests.get(url)

    try:
        data = json.loads(req.content)['jobs_results']

        for job in data:
            results.append(job)

        print(f'{len(data)} jobs for the type {job_type} in {city} added')
        s+=10
        get_google_jobs(job_type, city, s)
    except:
        print("stop")


for t in job_types:
    for c in cities:
        get_google_jobs(t, c, start)

with open('jobs.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)
