#!/usr/bin/python3 

""" return day of week from any date """
from datetime import datetime

def day_of_week(date_string):
    """ turn user input into date string """
    date = datetime.strptime(date_string, '%Y%m%d')
    return date.strftime('%A')

## prompt section ##

def validate_date(date_string):
    """ validate with try/except """
    try:
        date = datetime.strptime(date_string, '%Y%m%d')
        return True
    except ValueError:
        return False

def format_date(date_string):
    """ format """
    date = datetime.strptime(date_string, '%Y%m%d')
    return date.strftime('%B %d, %Y')

print('Please enter a date in the format YYYYMMDD:')
ISO_date = input()

if validate_date(ISO_date):
    print(format_date(ISO_date))
else:
    print('Invalid date format')

# Example usage
# DATE_STRING = '20230719'
print(ISO_date + " is a " + day_of_week(ISO_date)) # Output: Wednesday

# sys.exit("tmp stop")
