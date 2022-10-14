import json

import requests
from bs4 import BeautifulSoup
from termcolor import cprint
from colorama import init
from database import Database


class CreateCompany:
    database = Database()
    json_infos = None
    company_id = None
    agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.0.0 '
                      'Safari/537.36 Vivaldi/5.3.2679.70.'}

    def __init__(self, company_url, company_name):
        init()
        self.company_url = company_url.replace('https', 'http')
        cprint(company_url, 'cyan')

        company = self.database.get_company(company_name)

        if company is None:
            company_html = self.get_company_html()
            self.json_infos = self.get_json_infos(company_html)
            company_logo = self.get_company_logo()
            company_website = self.get_company_website()
            company_sector = self.get_company_sector()

            company_sector_id = self.database.add_sector(company_sector)
            company_description = self.get_company_description()

            company_place = self.get_company_place()
            company_founded_at = self.get_company_founded_at()
            companies = self.get_companies_html(company_name)
            company_short_description = self.get_company_short_description(companies)

            company = {
                'logo': company_logo,
                'name': company_name,
                'sector_id': company_sector_id,
                'description': company_description,
                'place': company_place,
                'founded_at': company_founded_at,
                'short_description': company_short_description
            }

            self.company_id = self.database.add_company(company)

            if company_website is not None:
                self.database.add_company_website(company_website, self.company_id)
                cprint(f'Company {company_name} saved in the database.', 'cyan')
        else:
            self.company_id = company[0]
            cprint(f'Company {company_name} already exist.', 'red')
            pass

    @staticmethod
    def get_json_infos(company_html):
        try:
            return json.loads(company_html.find('script', id="comp-initialData").text)
        except:
            pass

    def get_company_html(self):
        r = requests.get(self.company_url, headers=self.agent)
        return BeautifulSoup(r.content, 'html.parser')

    def get_companies_html(self, company_name: str):
        r = requests.get(f'http://fr.indeed.com/companies/search?q=${company_name}', headers=self.agent)
        return BeautifulSoup(r.content, 'html.parser')

    def get_company_logo(self):
        try:
            return self.json_infos['companyPageHeader']['auroraLogoUrl2x']
        except:
            pass

    def get_company_website(self):
        try:
            return self.json_infos['aboutSectionViewModel']['aboutCompany']['websiteUrl']['url']
        except:
            pass

    def get_company_sector(self):
        try:
            return self.json_infos['aboutSectionViewModel']['aboutCompany']['industry']
        except:
            pass

    @staticmethod
    def get_company_short_description(companies):
        try:
            company_row = companies.find('div', {"data-tn-component": "CompanyRow"})
            children = company_row.findChildren("p", recursive=True)
            return children[0].text
        except:
            pass

    def get_company_description(self):
        try:
            return self.json_infos['aboutSectionViewModel']['aboutCompany']['description']
        except:
            pass

    def get_company_place(self):
        try:
            return self.json_infos['aboutSectionViewModel']['aboutCompany']['headquartersLocation']['address']
        except:
            pass

    def get_company_founded_at(self):
        try:
            return self.json_infos['aboutSectionViewModel']['aboutCompany']['founded']
        except:
            pass