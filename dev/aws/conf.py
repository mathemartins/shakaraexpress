from botocore.client import Config


import datetime
AWS_ACCESS_KEY_ID = "AKIAITNYS3YVDUJNFKOA"
AWS_SECRET_ACCESS_KEY = "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"
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

DEFAULT_FILE_STORAGE = 'dev.aws.utils.MediaRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'shakara2'
S3DIRECT_REGION = 'us-east-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL

config = Config(signature_version='s3v4')

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = { 
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}
