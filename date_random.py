from datetime import date
import random

'''
Create random date/
Input date format: yyyy-mm-dd
'''
def random_date(start_date_ = '1960-01-01', end_date_ = ''):
    if end_date_:
        end_date = date.fromisoformat(end_date_)
    else:
        end_date = date.today()
    start_date = date.fromisoformat(start_date_)
    return date.fromordinal(random.randint(start_date.toordinal(), end_date.toordinal())).isoformat()
