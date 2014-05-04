#!/usr/bin/env python
import csv
import sys, os
import argparse

sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.settings'

from sideproductcatalog.models import Product, Option, OptionValue, Category, SeasonCode, ColorCode


class CSVParser():

    file = None

    def __init__(self, *args, **kwargs):
        self.file = kwargs['file']

    def parse_file(self):

        with open(self.file, 'rU') as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            file_fields = csv_reader.fieldnames
            for index, row in enumerate(csv_reader):
                self.strip_whitespace(row)
                try:
                    product = Product.objects.get(sku=row['SKU'])
                except:
                    product = Product.objects.create(
                        name=row['NAME'],
                        sku=row['SKU'],
                        taxable=row['TAX'] == 'Y' and True or False,
                        price=row['PRICE'] and float(row['PRICE']) or 0.00,
                        quantity=row['ONHAND'],
                        season=row['SEASON'],
                        description=row['DESCRIPTION'],
                        sale_price=row['SALE PRICE'] and float(row['SALE PRICE']) or 0.00,
                        on_sale=row['ON SALE'] == 'Y' and True or False
                    )

                self.parse_category(product, row)
                self.parse_option(product, row)
                self.parse_codes(product, row)
                product.save()


    def parse_category(self, product, data):
        category = None
        # check category level one
        if data['CATEGORY 1']:
            try:
                category_1 = Category.objects.filter(name=data['CATEGORY 1'], level=1).get()
            except:
                category_1 = Category.objects.create(
                    name=data['CATEGORY 1'],
                    level=1
                )
            category = category_1

        # check category level two
        if data['CATEGORY 2']:
            try:
                category_2 = Category.objects.filter(name=data['CATEGORY 2'], level=2).get()
            except:
                category_2 = Category.objects.create(
                    name=data['CATEGORY 2'],
                    level=2,
                    parent=category_1.id
                )
            category = category_2

        # check category level three
        if data['CATEGORY 3']:
            try:
                category_3 = Category.objects.filter(name=data['CATEGORY 3'], level=3).get()
            except:
                category_3 = Category.objects.create(
                    name=data['CATEGORY 3'],
                    level=3,
                    parent=category_2.id
                )
            category = category_3

        product.category = category

    def parse_option(self, product, data):
        option = None
        # size-color combination option
        combo = 'size-color'
        try:
            option = Option.objects.filter(product=product, type=combo).get()
        except:
            option = Option.objects.create(
                product=product,
                type=combo,
                label='Size and Color'
            )
        # color option values
        types = ['SIZE', 'COLOR']
        for type in types:
            value = data[type].lower()
            if type == 'SIZE':
                label = data[type] == 'ONE' and 'One Size' or data[type]
            else:
                label = data[type].capitalize()

            try:
                code = ColorCode.objects.get(value=data['COLOR CODE'].lower())
            except:
                code = ColorCode.objects.create(
                    value=data['COLOR CODE'].lower(),
                    label=data['COLOR CODE']
                )

            try:
                optionvalue = OptionValue.objects.filter(option=option, upc=data['UPC'], value=value).get()
            except:
                optionvalue = OptionValue.objects.create(
                    option=option,
                    upc=data['UPC'],
                    color_code=code,
                    value=value,
                    label=label
                )

    def parse_codes(self, product, data):
        try:
            code = SeasonCode.objects.get(value=data['SEASON CODE'].lower())
        except:
            code = SeasonCode.objects.create(
                value=data['SEASON CODE'].lower(),
                label=data['SEASON CODE']
            )
        product.season_code = code

    def strip_whitespace(self, data):
        for key, value in data.items():
            data[key] = value.rstrip()


def GetArgs():
    parser = argparse.ArgumentParser(description='Parameters for Parser')
    parser.add_argument('--file', dest='file', help='CSV data file', default='feed.csv')
    return parser.parse_args()


if __name__ == '__main__':
    args = GetArgs()
    parser = CSVParser(file=args.file)
    parser.parse_file()
