import csv
import pycountry
import codecs
from datetime import datetime
import operator
import logging


def crt_changing(impressions, crt, row_number):
    """
    Function that makes clicks of (impressions*crt/100) pattern
    :param impressions: goes from row .csv file
    :param crt: goes from row .csv file
    :param row_number: It is the row number where problem is found.
    :return: clicks
    """
    if isinstance(crt, str):
        crt = crt.replace('%', '')
    try:
        crt = float(crt)/100
        click = round(float(impressions)*crt)
        return click
    except ValueError:
        logging.error('Could not convert impression and crt to click.', row_number)


def get_alpha_3_code(city_name):
    """
    Function that checks if alpha_3_code in ISO_3166 dictionary is avaible
    :param city_name: goes from row .csv file
    :return: gets alpha_3_code if it exists if not it returns 'XXX'
    """
    cities_pycountry = list(pycountry.subdivisions)
    for p in cities_pycountry:
        if p.name == city_name:
            return pycountry.countries.get(alpha_2=p.country_code).alpha_3
    return 'XXX'


def add_impression_click(city, click, date, impressions, results):
    """
    Calculates results. Adds impressions and clicks for similiar alpha_3_code.
    :param city: goes from row .csv file
    :param click: is made by crt_changing function
    :param date: goes from row .csv file in format datetime.object (YYYY-MM-DD)
    :param impressions: goes from row .csv file
    :param results: is dictionary sorted like: {date: [alpha_3_code: [impressions, clicks]}}
    :return: calculated results. Adds impressions and clicks for similiar alpha_3_code
    """
    alpha_3_code = get_alpha_3_code(city)
    results[date][alpha_3_code].append([impressions, click])
    results[date][alpha_3_code][0][0] = int(results[date][alpha_3_code][0][0]) + int(results[date][alpha_3_code][1][0])
    results[date][alpha_3_code][0][1] += results[date][alpha_3_code][1][1]
    results[date][alpha_3_code].pop()
    return results


def agregated_data(file_name):
    """
        Goes into .csv extension file with day, city, impressions, crt per row
        and returns dictionary sorted like: {date: [alpha_3_code: [impressions, clicks]}}
    :param file_name: It is .csv extension file with day, city, impressions, crt per row
    :return: dictionary sorted like: {date: [alpha_3_code: [impressions, clicks]}}
    """
    results = {}
    if not csv_extension:
        return results
    try:
        with codecs.open(file_name, 'r', encoding='utf-8') as inputed_file:
            csv_reader = csv.reader(inputed_file)
            for row_number, row in enumerate(csv_reader):
                day, city, impressions, crt = row
                alpha_3_code = get_alpha_3_code(city)
                click = crt_changing(impressions, crt, row_number)
                date = str(datetime.strptime(day, '%m/%d/%Y').date())
                if results.get(date):
                    if results[date].get(alpha_3_code):
                        add_impression_click(city, click, date, impressions, results)
                    else:
                        results[date][alpha_3_code] = [[impressions, click]]
                else:
                    results[date] = {}
                    results[date][alpha_3_code] = [[impressions, click]]
                results[date] = dict(sorted(results[date].items(), key=operator.itemgetter(0)))
    except FileNotFoundError:
        logging.error('Could not manage to find file.')
    save_result_to_file(results)
    return results


def save_result_to_file(results):
    """
    Function that saves dictionary sorted like: {date: [alpha_3_code: [impressions, clicks]}} to output.csv
    :param results: dictionary sorted like: {date: [alpha_3_code: [impressions, clicks]}}
    :return: output.csv file with date, alpha_3_code, impressions, clicks per row
    """
    with open('output.csv', 'w', newline='') as output_file:
        output_writer = csv.writer(output_file)
        for date, data in results.items():
            for alpha_code, params in data.items():
                impressions_amount = params[0][0]
                clicks_amount = params[0][1]
                output_writer.writerow([date, alpha_code, impressions_amount, clicks_amount])
        return True


def csv_extension(filename):
    """
    :param filename: any file name
    :return: bool type. if file endswith .csv return true else false
    """
    return filename.endswith('.csv')


if __name__ == '__main__':

    agregated_data('data_to_change.csv')
