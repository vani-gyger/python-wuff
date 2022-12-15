import click
import requests
import csv
import datetime
from collections import Counter



# TODO check internet connection & no url
def fetchData():
    res = requests.get("https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002/download/KUL100OD1002.csv")
    if not res:
        return
    res.encoding = "utf-8-sig"
    return res.text.splitlines()

def stats(file, year):
    longestName = 'a'
    shortestName ='ThisisNotTheShortestName'
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


@click.option('-y', '--year',  type=int, help='The year to search for your dog. Not birthdate and min 2015')
@click.command()  
def main(year):
    if year and len(str(year)) != 4:
       return click.echo('Error: Invalid year. Please provide a four digit number.')
    elif not year:
        year = datetime.date.today().year
        click.echo(f'No Year is provided, actual year will be taken.')

    print(f'Inspecting year is: {year}')
    file = csv.DictReader(fetchData())
    stats(file, year)

if __name__ == '__main__':
    main()