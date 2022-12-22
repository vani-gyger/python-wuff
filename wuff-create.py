import click
import requests
import csv
import datetime
import os
import random
import sys
from pathlib import Path


def fetchData():
    try:
        res = requests.get("https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002/download/KUL100OD1002.csv")     
        if not res:
            sys.exit('Error: Can not get Source CSV from data.stadt-zuerich.ch.')
        res.encoding = "utf-8-sig"
        return res.text.splitlines()
    except requests.exceptions.ConnectionError:
        sys.exit('Error: Could not connect to the API. The external service may be down. Please try again later.')

def getRandomDogPic(random_dog_name, random_dog_birth, picDir):
    response = requests.get('https://random.dog/woof.json')
    if not response.ok:
        sys.exit('Error: Could not connect to the API. The external service may be down. Please try again later.')
        raise ConnectionError
    json_data = response.json()
    url = json_data["url"]
    response = requests.get(url, stream=True, timeout=60)
    extension = str(json_data["url"]).rsplit('.', 1)[1]
    picture_name = picDir + '/wuff_' + random_dog_name + "_" + random_dog_birth + extension
    
    with open(str(picture_name), "wb") as f:
        f.write(response.content)
        print(f'The image of the new dog can be found here: {str(picture_name)}')
        return str(picture_name)

def randomNewDogs(file, picDir, year):
    names = []
    birthdays = []
    for row in file:
        names.append(row['HundenameText'])
        birthdays.append(row['GebDatHundJahr'])
    randomName = random.choice(names)
    randomBirthday = random.choice(birthdays)
    randomSex = random.choice(['w', 'm'])
    print(f"Name: {randomName}, Birthday: {randomBirthday}, Sex: {randomSex}")
    getRandomDogPic(randomName, randomBirthday, picDir)


def checkYear(year):
    if year and len(str(year)) != 4:
       sys.exit('Error: Invalid year. Please provide a four digit number.')
    elif not year:
        year = datetime.date.today().year
        print('No Year is provided, current year will be taken.')

    print(f'Inspecting year is: {year}')
    return year

def checkDir(givenDir):
    if Path(givenDir).is_file():
        sys.exit('Error: Given directory points to an existing file.')
    try:
        if givenDir.exists() and givenDir.is_dir():
            return givenDir
    except:
        print('The dog picture will be saved in the current directory')
        return os.getcwd()


@click.option('-y', '--year',  type=int, help='''From those years, a dog will be taken with their birthday for your new one!\n
It is optionally and not the birthdate and min year 2015. If it is empty the current year will be used.\n
''')
@click.option('-o', '--output-dir', type=str, help='Directory for the saved dog image. If no directory is given, the current directory will be taken')
@click.command()  
def main(year, output_dir):
    """ This tool creates a brand new dog for you!

    \b
    It'll print the year, a birthday and name, which is already in the database and saves pic from your new dog in given folder or in the current location.
    
    \b
    As example: python  wuff-create.py -y 2018
    """
    csvfile = csv.DictReader(fetchData())
    year = checkYear(year)
    picDir = checkDir(output_dir)
    randomNewDogs(csvfile, picDir, year)
    

if __name__ == '__main__':
    main()