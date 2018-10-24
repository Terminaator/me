import csv
import os
from collections import defaultdict

import requests
from estnltk import Text


def getStructuralUnit(code):
    """
    request = requests.get('https://ois2dev.ut.ee/api/structural-units/' + code.upper())
    status_code = request.status_code
    if status_code == 200:
        return request.json()
    raise Exception("reguest status code: ", status_code)
    """

    sUnits = _getStructuralUnits()
    a = {"name": {"et": sUnits[code.lower()][0]}}
    return a

def getAllStructuralUnits():
    request = requests.get('https://ois2dev.ut.ee/api/structural-units/all')
    status_code = request.status_code
    if status_code == 200:
        return request.json()
    raise Exception("reguest status code: ", status_code)

def _getStructuralUnits():
    """
    Reads structural Units from csv file
    :return: structural Units' codes and names in estonian in a dictionary
    """
    sUnits = defaultdict(list)
    with open(os.path.join(os.path.dirname(__file__), 'structuralUnits.csv'), encoding="UTF-8") as file:
        reader = csv.reader(file)
        for line in reader:
            sUnits[line[0].strip()].append(line[1].strip())
        return sUnits

def updateStructuralUnitsCSV():
    """
    Updates csv file where are all the university structure units
    """
    with open(os.path.join(os.path.dirname(__file__), 'structuralUnits.csv'), 'w', newline='', encoding="UTF-8") as file:
        writer = csv.writer(file, delimiter=',')
        sUnits = getAllStructuralUnits()
        for c in sUnits:
            if 'code' in c:
                if 'et' in c['name']:
                    writer.writerow([c['code'].lower(), c['name']['et']])


