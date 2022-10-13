from database import Database


class Socials:
    database = Database()

    def __init__(self):
        self.save_socials()

    def save_socials(self):
        socials = ['website', 'linkedin', 'twitter', 'facebook', 'instagram']
        self.database.save_socials(socials)


Socials()
