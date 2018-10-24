import csv
import os
from collections import defaultdict

import requests
from estnltk import Text


def coursesId(id):
    """
    request = requests.get('https://ois2dev.ut.ee/api/courses/' + id)
    status_code = request.status_code
    if status_code == 200:
        return request.json()
    raise Exception("reguest status code: ",status_code)
"""
    courses = _getCourses()
    a = {"title": {"et": courses[id.upper()][0][0]}, "credits": courses[id.upper()][0][1]}
    return a


def getNCourses(n: int, start: int):
    request = requests.get('https://ois2dev.ut.ee/api/courses?take=' + str(n) + '&start=' + str(start))
    status_code = request.status_code
    if status_code == 200:
        return request.json()
    raise Exception("reguest status code: ",status_code)

def _getCourses():
    """
    Reads courses from csv file
    :return: courses in dictionary
    """
    courses = defaultdict(list)
    with open(os.path.join(os.path.dirname(__file__), 'courses.csv'), encoding="UTF-8") as file:
        reader = csv.reader(file)
        for line in reader:

            courses[line[0].strip()].append([line[1].strip(), line[2]])
        return courses

def updateCoursesCSV():
    """
    Updates csv file where is all courses
    """
    with open(os.path.join(os.path.dirname(__file__), 'courses.csv'), 'w', newline='', encoding="UTF-8") as file:
        n = 300
        writer = csv.writer(file, delimiter=',')
        i = 1
        courses = getNCourses(n, i)
        while len(courses) != 0:
            for c in courses:
                if 'title' in c:
                    if 'et' in c['title']:
                        writer.writerow([c['code'], c['title']['et'], c['credits']])
                    elif 'en' in c['title']:
                        writer.writerow([c['code'], c['title']['en'], c['credits']])
            i += n
            courses = getNCourses(n, i)

#updateCoursesCSV()