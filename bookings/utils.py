import random
import string
import math
import datetime
import re

from django.utils.html import strip_tags


def booking_code_generator(size=5, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def statistics_average_calculator(stats):
	stat_values = []
	total = 0
	for stat in stats:
		stat_values.append(stat)

	for value in stat_values:
		total = value + total

	num_of_values = len(stat_values)
	avg = total / num_of_values

	return math.ceil(avg)


def count_words(html_string):
	word_string = strip_tags(html_string)
	matching_words = re.findall(r'\w+', word_string)
	count = len(matching_words)
	return count

def get_read_time(html_string):
	count = count_words(html_string)
	read_time_min = math.ceil(count/200.0) #using 200wpm for an average reader
	read_time = str(datetime.timedelta(minutes=read_time_min))
	return read_time