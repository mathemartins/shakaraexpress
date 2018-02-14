import random
import string
import math
import datetime
import re

from django.utils.html import strip_tags


def shop_code_generator(size=8, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))