import time
from termcolor import cprint
from indeed_types import IndeedJobTypes
from job_suggestions import IndeedJobSuggestions


class App:
    sleep = 86400  # 1day

    def __init__(self):
        self.run()

    def run(self):
        cprint("GET Indeed job suggestions", "green")
        IndeedJobSuggestions()
        cprint("GET Indeed job types", "green")
        IndeedJobTypes()
        time.sleep(self.sleep)
        self.run()


app = App()
