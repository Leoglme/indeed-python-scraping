import mysql.connector


class Database:
    cnx = mysql.connector.connect(user='root', password="", database='job_board')
    cursor = cnx.cursor()

    def __init__(self):
        pass

    def close_connect(self):
        self.cursor.close()
        self.cnx.close()

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
