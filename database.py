import mysql.connector
from termcolor import cprint
from colorama import init


class Database:
    cnx = mysql.connector.connect(user='root', password="", database='job_board')
    cursor = cnx.cursor()

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

    def delete_all_job(self):
        self.cursor.execute("SELECT id FROM advertisements")
        ids = self.cursor.fetchall()

        for id in ids:
            request = "DELETE FROM advertisements WHERE (%s)"
            self.cursor.execute(request, id)
            self.cnx.commit()
            cprint(f'Delete advertisement {id}', 'red')
        self.delete_advantage_advertisements()

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

    def get_advantage(self, advantage: str):
        if advantage is not None:
            self.cursor.execute("SELECT id FROM advantages WHERE label = '" + advantage + "'")
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
