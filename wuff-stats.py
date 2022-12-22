import click
import requests
import csv
import datetime
from collections import Counter
import sys

def fetchData():
    try:
        res = requests.get("https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002/download/KUL100OD1002.csv")     
        if not res:
            sys.exit('Error: Can not get Source CSV from data.stadt-zuerich.ch.')
        res.encoding = "utf-8-sig"
        return res.text.splitlines()
    except requests.exceptions.ConnectionError:
        sys.exit('Error: Could not connect to the API. The external service may be down. Please try again later.')

def stats(file, year):
    longestName = ''
    shortestName = 'NoName'
    dogNames = []
    femaleNames = []
    maleNames = []

    for row in file:
        currentName = row["HundenameText"]
        if row["StichtagDatJahr"] == str(year) and currentName != '?':
            if len(currentName) > len(longestName): longestName = currentName

            if len(currentName) < len(shortestName) and not currentName == '?': shortestName = currentName

            
            if row["SexHundLang"] == "männlich":
                maleNames.append(currentName)
            else:
                femaleNames.append(currentName)
            
    
    print(f'One shortest Name is: {shortestName}')
    print(f'One longest Name is: {longestName}')
    print(f'Counted female dogs: {len(femaleNames)}')
    print(f'Counted male dogs: {len(maleNames)}')
    print(f'Top 10 dog names: {Counter(maleNames + femaleNames).most_common(10)}')
    print(f'Top 10 female dog names: {Counter(femaleNames).most_common(10)}')
    print(f'Top 10 male dog names: {Counter(maleNames).most_common(10)}')

def checkYear(year):
    if year and len(str(year)) != 4:
       sys.exit('Error: Invalid year. Please provide a four digit number.')
    elif not year:
        year = datetime.date.today().year
        print('No Year is provided, current year will be taken.')

    print(f'Inspecting year is: {year}')
    return year

@click.option('-y', '--year',  type=int, help='''The year to inspecting.\n
It is optionally and not the birthdate and min year 2015. If it is empty the current year will be used.\n
''')
@click.command()  
def main(year):
    """
    This tool finds the best dogs from a certain year!

    \b
    It'll find for you the longest Name, counted female dogs, counted male dogs, top 10 dog names, top 10 female dog names and top 10 male dog names.
    
    
    \b 
    As example: python  wuff-stats.py -y 2018
    """
    year = checkYear(year)
    file = csv.DictReader(fetchData())
    stats(file, year)

if __name__ == '__main__':
    main()