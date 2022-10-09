import mysql.connector


class Database:
    cnx = mysql.connector.connect(user='root', password="", database='job_board')
    cursor = cnx.cursor()

    def __init__(self):
        pass

    def close_connect(self):
        self.cursor.close()
        self.cnx.close()

    def get_job_types(self):
        self.cursor.execute("SELECT label FROM job_types")
        r = []
        labels = self.cursor.fetchall()
        for label in labels:
            r.extend(label)
        return r

    def delete_all_job(self):
        self.cursor.execute("TRUNCATE TABLE advertisements")

    def delete_all_job_types(self):
        self.cursor.execute("TRUNCATE TABLE job_types")

    def get_all_job_indeed_id(self):
        self.cursor.execute("SELECT indeed_id FROM advertisements")
        r = []
        ids = self.cursor.fetchall()
        for id in ids:
            r.extend(id)
        return r

    def add_job_type(self, label: str, score: int):
        request = "INSERT INTO job_types ""(label, score)" "VALUES (%s, %s)"
        try:
            self.cursor.execute(request, (label, score))
            print({
                "label": label,
                "score": score
            })
            self.cnx.commit()
        except:
            pass

    def add_job(self, title: str, description: str, salary: int, place: str, indeed_id: str):
        request = ("INSERT INTO advertisements ""(title, description, salary, place, working_time, owner_id, indeed_id)"
                   " VALUES (%s, %s, %s, %s, %s, %s, %s)")
        self.cursor.execute(request, (title, description, salary, place, 39, 1, indeed_id))
        self.cnx.commit()
