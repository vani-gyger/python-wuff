import click
import requests
import csv
import argparse
import datetime

def fetchData():
    try:
        res = requests.get("https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002/download/KUL100OD1002.csv")     
        if not res:
            return click.echo('Error: Can not get Source CSV from data.stadt-zuerich.ch')
        res.encoding = "utf-8-sig"
        return res.text.splitlines()
    except requests.exceptions.ConnectionError:
        return click.echo('Error: Could not connect to the API. The external service may be down.')
    except:
        return click.echo('Error: Something went wrong.')


def find(file, name, year):
    
    print(f'Year: {year} with name: {name}')
    foundOne = False
    for row in file:
        if row["StichtagDatJahr"] == str(year) and row["HundenameText"] == name:
            birthdate = 'w' if row["SexHundLang"] == 'weiblich' else 'm'
            print(f'{name} {row["GebDatHundJahr"]}, {birthdate}')
            foundOne = True
    if not foundOne:
        return click.echo(f'No dog found in the database with the name \'{name}\' and the year \'{year}\'')

def checkYear(year):
    if year and len(str(year)) != 4:
       return click.echo('Error: Invalid year. Please provide a four digit number.')
    elif not year:
        year = datetime.date.today().year
        print('No Year is provided, current year will be taken.')

    print(f'Inspecting year is: {year}')
    return year

@click.argument('name', type=str)
@click.option('-y', '--year',  type=int, help='''The year to search for your dog.\n
It is optionally and not the birthdate and min year 2015. If it is empty the current year will be used.\n
As example: python wuff-find.py Luna -y 2018 ''')
@click.command()
def main(name, year):
    try:
        year = checkYear(year)
        file = csv.DictReader(fetchData())
        find(file, name, year)
    except:
        return click.echo('Please try again later.')

if __name__ == '__main__':
    main()