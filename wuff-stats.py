import requests
import csv
import argparse

def fetchData():
    res = requests.get("https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002/download/KUL100OD1002.csv")
    res.encoding = "utf-8-sig"
    return res.text.splitlines()

# def findRandom(year):
#     file = csv.DictReader(fetchData())
#     for row in file:

#         if row["StichtagDatJahr"] == year and row["HundenameText"] == "Adonis":

#             print(row)

def run(args):
    if args.year:
        findRandom(args.year)
    else:
        findRandom('2022')

def get_parser():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--year',
        dest = 'year',
    )

    return parser

def main(args=None):
    parsed = get_parser().parse_args(args)
    run(parsed)

if __name__ == '__main__':
    main()