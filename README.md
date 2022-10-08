<h2 align="center">Indeed Python Scraping</h2>

<p>
 Python library to retrieve the latest results from indeed every 24 hours (employees, cities and types of employment), and save the data in the mysql database.
</p>


![Language](https://img.shields.io/badge/language-python-yellow.svg?style=flat)
![Language](https://img.shields.io/badge/language-mysql-blue.svg?style=flat)

<img alt="hero" width="100%" height="auto" src="https://i.ibb.co/3dnYZCt/index.png">



> The source code is on the repo [indeed-python-scraping](https://github.com/Leoglme/indeed-python-scraping)

## Install

   ```sh
    $ git clone https://github.com/Leoglme/indeed-python-scraping
    $ cd indeed-python-scraping
    $ pip install time requests bs4 re termcolor colorama
   ```

## Features

### Execute indeed scraping script

```sh
$ cd indeed-python-scraping
$ pip install
$ python indeed.py
```
#### resultat =>
```sh
http://fr.indeed.com/emplois?q=développeur&l=Nantes&radius=0&fromage=1&vjk=8651b9be54b7b5ef&start=20&sort=date
{'per_page': 1, 'current_page': 3, 'start': 30, 'max_results': 31, 'number_jobs': 31}
Paused for 10 seconds
```

## License

Copyright (MIT) 2022 [Dibodev](https://dibodev.com/)
