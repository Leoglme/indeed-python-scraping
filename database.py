import mysql.connector
from termcolor import cprint
from colorama import init


class Database:
    cnx = mysql.connector.connect(user='root', password="", database='job_board')
    cursor = cnx.cursor(buffered=True)

    def __init__(self):
        init()
        pass

    def close_connect(self):
        self.cursor.close()
        self.cnx.close()

    def get_places(self):
        places = []
        self.cursor.execute("SELECT name FROM regions")
        names = self.cursor.fetchall()
        for name in names:
            places.extend(name)

        self.cursor.execute("SELECT name FROM departments")
        names = self.cursor.fetchall()
        for name in names:
            places.extend(name)
        return places

    def delete_advantage_advertisements(self):
        self.cursor.execute("TRUNCATE TABLE advantage_advertisements")

    def delete_job_types(self):
        self.cursor.execute("TRUNCATE TABLE job_types")

    def delete_all_job(self):
        self.cursor.execute("SELECT id FROM advertisements")
        ids = self.cursor.fetchall()

        for id in ids:
            request = "DELETE FROM advertisements WHERE (%s)"
            self.cursor.execute(request, id)
            self.cnx.commit()
            cprint(f'Delete advertisement {id}', 'red')
        self.delete_advantage_advertisements()
        self.delete_job_types()

    def delete_all_job_suggestions(self):
        self.cursor.execute("TRUNCATE TABLE job_suggestions")

    def get_all_job_indeed_id(self):
        self.cursor.execute("SELECT indeed_id FROM advertisements")
        r = []
        ids = self.cursor.fetchall()
        for id in ids:
            r.extend(id)
        return r

    def add_job_suggestion(self, label: str, score: int):
        request = "INSERT INTO job_suggestions ""(label, score)" "VALUES (%s, %s)"
        try:
            self.cursor.execute(request, (label, score))
            print({
                "label": label,
                "score": score
            })
            self.cnx.commit()
        except:
            pass

    def add_job_type(self, type: str):
        request = "INSERT INTO types ""(label)" "VALUES (%s)"
        print(f'The type of job {type} has been saved in the database')

        self.cursor.execute(request, (type,))
        self.cnx.commit()

    def save_socials(self, socials):
        for social in socials:
            request = "INSERT INTO socials ""(name)" "VALUES (%s)"
            print(f'The social network {social} has been saved in the database')
            self.cursor.execute(request, (social,))
            self.cnx.commit()

    def get_company(self, company_name):
        if company_name is not None:
            self.cursor.execute('SELECT id FROM companies WHERE name = "' + company_name + '"')
            return self.cursor.fetchone()
        else:
            pass

    def get_advantage(self, advantage: str):
        if advantage is not None:
            self.cursor.execute('SELECT id FROM advantages WHERE label = "' + advantage + '"')
            return self.cursor.fetchone()
        else:
            pass

    def get_type(self, job_type: str):
        if job_type is not None:
            self.cursor.execute('SELECT id FROM types WHERE label = "' + job_type + '"')
            return self.cursor.fetchone()
        else:
            pass

    def add_advantage(self, advantage: str):
        res = self.get_advantage(advantage)
        if res is None:
            request = "INSERT INTO advantages ""(label)" "VALUES (%s)"
            print(f'The advantage {advantage} has been saved in the database')
            self.cursor.execute(request, (advantage,))
            self.cnx.commit()

    def add_advantage_advertisements(self, advantages: [], job_id: int):
        try:
            for advantage in advantages:
                advantage_ids = self.get_advantage(advantage)
                request = "INSERT INTO advantage_advertisements ""(avantage_id, advertisement_id)" "VALUES (%s, %s)"
                for advantage_id in advantage_ids:
                    self.cursor.execute(request, (advantage_id, job_id))
            self.cnx.commit()
        except:
            pass

    def add_job_types(self, job_types: [], job_id: int):
        try:
            for job_type in job_types:
                type_ids = self.get_type(job_type)
                request = "INSERT INTO job_types ""(type_id, advertisement_id)" "VALUES (%s, %s)"
                for type_id in type_ids:
                    self.cursor.execute(request, (type_id, job_id))
            self.cnx.commit()
        except:
            pass

    def get_sector(self, sector: str):
        if sector is not None:
            self.cursor.execute('SELECT id FROM sectors WHERE label = "' + sector + '"')
            res = self.cursor.fetchone()
            if res is not None:
                res = res[0]
            return res
        else:
            pass

    def add_sector(self, sector: str):
        res = self.get_sector(sector)

        if res is None:
            request = "INSERT INTO sectors ""(label)" "VALUES (%s)"
            print(f'The sector {sector} has been saved in the database')
            self.cursor.execute(request, (sector,))
            self.cnx.commit()
            return self.cursor.lastrowid
        else:
            return res

    def get_social_id(self, key: str):
        if key is not None:
            self.cursor.execute('SELECT id FROM socials WHERE name = "' + key + '"')
            return self.cursor.fetchone()
        else:
            pass

    def add_company_website(self, website: str, company_id: int):
        try:
            social_id = self.get_social_id('website')
            request = "INSERT INTO social_companies ""(social_id, company_id, url)" "VALUES (%s, %s, %s)"
            for id in social_id:
                self.cursor.execute(request, (id, company_id, website))
            self.cnx.commit()
        except:
            pass

    def add_job(self, job):
        request = (
            "INSERT INTO advertisements ""(title, description, short_description, salary, qualifications, place, indeed_id, company_id)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

        self.cursor.execute(request,
                            (
                                job['title'],
                                job['description'],
                                job['short_description'],
                                job['salary'],
                                job['qualifications'],
                                job['place'],
                                job['indeed_id'],
                                5
                            ))

        self.cnx.commit()
        return self.cursor.lastrowid

    def add_company(self, company):
        request = (
            "INSERT INTO companies ""(logo, name, sector_id, description, place, founded_at, short_description)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s)")

        self.cursor.execute(request,
                            (
                                company['logo'],
                                company['name'],
                                company['sector_id'],
                                company['description'],
                                company['place'],
                                company['founded_at'],
                                company['short_description']
                            ))

        self.cnx.commit()
        return self.cursor.lastrowid
