import os

if os.environ.get('AWS_ACCESS_KEY_ID'):
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
else:
    print('Environment Variable AWS_ACCESS_KEY_ID not set')
    quit(1)


if os.environ.get('AWS_SECRET_ACCESS_KEY'):
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
else:
    print('Environment Variable AWS_SECRET_ACCESS_KEY not set')
    quit(1)


if os.environ.get('AWS_BUCKET'):
    AWS_BUCKET = os.environ.get('AWS_BUCKET')
else:
    print('Environment Variable AWS_BUCKET not set')
    quit(1)


if os.environ.get('FUP_PORT'):
    FUP_PORT = os.environ.get('FUP_PORT')
else:
    print('Environment Variable FUP_PORT not set')
    quit(1)

if os.environ.get('BRANCH'):
    BRANCH = os.environ.get('BRANCH')
else:
    print('Environment Variable BRANCH not set')
    quit(1)


if os.environ.get('HEALTHCHECK_TEST_BUCKET'):
    HEALTHCHECK_TEST_BUCKET = os.environ.get('HEALTHCHECK_TEST_BUCKET')
else:
    print('Environment Variable HEALTHCHECK_TEST_BUCKET not set')
    quit(1)


UPLOAD_FOLDER = 'data/'
THUMBNAIL_FOLDER = 'data/thumbnail/'
MAX_CONTENT_LENGTH = 50 * 1024 * 1024
