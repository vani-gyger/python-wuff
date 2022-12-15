import click
import requests
import csv
import argparse
import datetime



def fetchData():
    res = requests.get("https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002/download/KUL100OD1002.csv")
    if not res:
        return
    res.encoding = "utf-8-sig"
    return res.text.splitlines()


def find(name, year):
    file = csv.DictReader(fetchData())
    print(f'Year: {year} with name: {name}')
    foundOne = False
    for row in file:
        if row["StichtagDatJahr"] == str(year) and row["HundenameText"] == name:
            birthdate = 'w' if row["SexHundLang"] == 'weiblich' else 'm'
            print(f'{name} {row["GebDatHundJahr"]}, {birthdate}')
            foundOne = True
    if not foundOne:
        return click.echo(f'No dog found in the database with the name \'{name}\' and the year \'{year}\'')

@click.argument('name', type=str)
@click.option('-y', '--year',  type=int, help='The year to search for your dog. Not birthdate and min 2015')
@click.command()
def run(name, year):
    if year and len(str(year)) != 4:
       return click.echo('Error: Invalid year. Please provide a four digit number.')
    elif not year:
        year = datetime.date.today().year
    find(name, year)

if __name__ == '__main__':
    run()