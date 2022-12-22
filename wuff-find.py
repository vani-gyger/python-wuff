import click
import requests
import csv
import argparse
import datetime
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


def find(file, name, year):
    
    print(f'Year: {year} with name: {name}')
    foundOne = False
    for row in file:
        if row["StichtagDatJahr"] == str(year) and row["HundenameText"] == name:
            sex = 'w' if row["SexHundLang"] == 'weiblich' else 'm'
            print(f'Name: {name}, with birthday {row["GebDatHundJahr"]} and sex: {sex}')
            foundOne = True
    if not foundOne:
        sys.exit(f'No dog found in the database with the name \'{name}\' and the year \'{year}\'')

def checkYear(year):
    if year and len(str(year)) != 4:
       sys.exit('Error: Invalid year. Please provide a four digit number.')
    elif not year:
        year = datetime.date.today().year
        print('No Year is provided, current year will be taken.')

    print(f'Inspecting year is: {year}')
    return year

@click.argument('name', type=str)
@click.option('-y', '--year',  type=int, help='''The year to search for your dog.\n
It is optionally and not the birthdate and min year 2015. If it is empty the current year will be used.\n
''')
@click.command()
def main(name, year):
    """
    This tool'll find the dogs with the name you give in a certain year!

    \b
    As example: python wuff-find.py Luna -y 2018
    """
    year = checkYear(year)
    file = csv.DictReader(fetchData())
    find(file, name, year)

if __name__ == '__main__':
    main()