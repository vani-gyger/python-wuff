import click
import requests
import csv
import datetime
import os
import random

def fetchData():
    try:
        res = requests.get("https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002/download/KUL100OD1002.csv")     
        if not res:
            return click.echo('Error: Can not get Source CSV from data.stadt-zuerich.ch')
        res.encoding = "utf-8-sig"
        return res.text.splitlines()
    except requests.exceptions.ConnectionError:
        return click.echo('Error: Could not connect to the API. The external service may be down. Please try again later.')
    except:
        return click.echo('Error: Something went wrong.')

def getRandomDogPic(random_dog_name, random_dog_birth, picDir):
    response = requests.get('https://random.dog/woof.json')
    if not response.ok
        click.echo('Error: Could not connect to the API. The external service may be down. Please try again later.')
        raise ConnectionError
    json_data = response.json()
    url = json_data["url"]
    response = requests.get(url, stream=True, timeout=60)
    extension = str(json_data["url"])[-len(json_data["url"].split('.')[-1])-1:]
    picture_name = picDir + '_' + random_dog_name + "_" + random_dog_birth + extension
    
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
       return click.echo('Error: Invalid year. Please provide a four digit number.')
    elif not year:
        year = datetime.date.today().year
        print('No Year is provided, current year will be taken.')

    print(f'Inspecting year is: {year}')
    return year

def checkDir(givenDir):
    try:
        if givenDir.exists() and givenDir.is_dir():
            return givenDir
        # elif givenDir.is_file(): CHECK THIS
            return click.echo('Error: Given directory points to an existing file.')
    except:
        print('The dog picture will be saved in the current directory')
        return os.getcwd()


@click.option('-y', '--year',  type=int, help='''From those years, a dog will be taken with their birthday for your new one!\n
It is optionally and not the birthdate and min year 2015. If it is empty the current year will be used.\n
As example: python  wuff-create.py -y 2018''')
@click.option('-o', '--output-dir', type=str, help='Directory for the saved dog image. If no directory is given, the current directory will be taken')
@click.command()  
def main(year, output_dir):
    try: # HOW TO DO NOT?
        csvfile = csv.DictReader(fetchData())
        year = checkYear(year)
        picDir = checkDir(output_dir)
        print(picDir)
        randomNewDogs(csvfile, picDir, year)
    except:
        return click.echo('Please try again later.')
    
    

if __name__ == '__main__':
    main()