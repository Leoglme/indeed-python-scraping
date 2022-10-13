import mysql.connector


class Database:
    cnx = mysql.connector.connect(user='root', password="", database='job_board')
    cursor = cnx.cursor()

    def __init__(self):
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

    def delete_all_job(self):
        self.cursor.execute("TRUNCATE TABLE advertisements")

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

    def add_job_type(self, label: str):
        request = "INSERT INTO types label VALUES %s"

        print(f'The type of job {label} has been saved in the database')
        print(request)
        self.cursor.execute(request, label)
        self.cnx.commit()

    def add_job(self, job):
        request = ("INSERT INTO advertisements ""(title, description, salary, place, working_time, owner_id, indeed_id)"
                   " VALUES (%s, %s, %s, %s, %s, %s, %s)")
        self.cursor.execute(request,
                            (job['title'], job['description'], job['salary'], job['place'], 39, 1, job['indeed_id']))
        self.cnx.commit()
