from datetime import datetime, timedelta
import pandas as pd
from random import randint
## can be two datetime data types minus (datetime - datetime ).days
from dateutil import rrule
from datetime import datetime

list(rrule.rrule(rrule.DAILY,count=100,dtstart=datetime.now()))

num = 10
base = datetime.today()
data_range = [base - timedelta[days=x] for x in range(num)]
data_range = [base - timedelta[seconds=(x*60 + randint(-30, 30))] for x in range(num)]

datelist = pd.date_range(end = pd.datetime.today(), periods = 100).tolist()
# datelist = pd.date_range(pd.datetime.today(), periods = 100).to_pydatetime().tolist()
## change date_range format
# datelist.format(formatter=lambda x: x.strftime('%Y%m%d'))

def date_generator():
	start_date = datetime.today()
	while True:
		yield start_date
		start_date = start_date - timedelta(days = 1)


import itertools
dates = itertools.islice(date_generator(), 3)


def date_range(start_date, end_date):
	for ordinal in range(start_date.toordinal(), end_date.toordinal()):
		yield datetime.date.fromordinal(ordinal)