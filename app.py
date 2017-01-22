#!/usr/local/bin/python
"""
# Author: Marc Condon
# Email: marc@fogtest.com
# Git repository: https://github.com/fogcitymarathoner/flask-file-uploader
# This work based on jQuery-File-Upload which can be found at
# https://github.com/blueimp/jQuery-File-Upload/
"""
import os
import re
import json
import boto

from boto.exception import S3ResponseError
from flask import Flask
from flask import request
from flask import render_template
from flask import abort
from flask.ext.bootstrap import Bootstrap
from lib.cors import PolicySigner
from lib.cors import starts_with_branch
from lib.cors import crossdomain

app = Flask(__name__, instance_relative_config=True)
# Load the default configuration
if os.environ.get('FUP_SETTINGS'):
    settings_file = os.environ.get('FUP_SETTINGS')
else:
    print('Environment Variable FUP_SETTINGS not set')
    quit(1)

if os.path.isfile(settings_file):
    try:
        app.config.from_envvar('FUP_SETTINGS')
    except Exception as e:
        print('something went wrong with config file %s' % settings_file)
        quit(1)
else:
    print('settings file %s does not exits' % settings_file)

print 'Using boto version %s' % boto.__version__

s3 = boto.connect_s3(
    app.config['AWS_ACCESS_KEY_ID'],
    app.config['AWS_SECRET_ACCESS_KEY'])

# test aws credentials
try:
    bucket = s3.get_bucket(app.config['HEALTHCHECK_TEST_BUCKET'])
except S3ResponseError:
    print('AWS credentials are bad')
    quit(1)

# test bucket
bucket = s3.lookup(app.config['AWS_BUCKET'])

if bucket is None:
    print "Creating Bucket %s" % app.config['AWS_BUCKET']
    s3.create_bucket(app.config['AWS_BUCKET'])

bootstrap = Bootstrap(app)


@app.route('/api/v1/make-s3-key-public', methods=['POST'])
@crossdomain(origin='*')
def make_s3_key_public():
    """
    makes access url returned after upload public
    """
    key = request.form['key']
    s3key = bucket.lookup(key)
    if s3key:
        print 'Making %s publicly accessible' % s3key
        s3key.set_acl('public-read')
    return '{}'


@app.route('/api/v1/cors-credentials', methods=['GET'])
@crossdomain(origin='*')
def s3_cors_credentials():
    """
    s3_cors_credentials - returns credentials that allow browser to post directly to S3
    """
    # 10 minute expiration
    signer = PolicySigner(
        600, app.config['AWS_BUCKET'], app.config['BRANCH'],
        app.config['AWS_ACCESS_KEY_ID'], app.config['AWS_SECRET_ACCESS_KEY'])
    return signer.to_json()


@app.route('/about', methods=['GET'])
def about():
    """
    static about page
    """
    # 10 minute expiration
    signer = PolicySigner(
        600, app.config['AWS_BUCKET'], app.config['BRANCH'],
        app.config['AWS_ACCESS_KEY_ID'], app.config['AWS_SECRET_ACCESS_KEY'])
    return render_template('about.html', about=signer)


@app.route('/api/v1/delete', methods=['OPTIONS', 'DELETE'])
@crossdomain(origin='*')
def delete():
    """
    Delete S3 key by boto
    curl -X DELETE localhost:9194/api/v1/delete?file=upload-s3-test/Portfile
    """
    print request.args.get('file')
    if request.args.get('file'):
        found = False
        for key in bucket.list():
            if key.name.encode('utf-8').split('/')[1] != '' and request.args.get('file') == key.name.encode('utf-8'):
                key.delete()
                message = 'Deleting %s' % key.name.encode('utf-8')
                print message
                found = True
        if not found:
            abort(404)
    else:
        abort(404)

    return '{"message": message}'


@app.route('/api/v1/list', methods=['GET'])
@crossdomain(origin='*')
def list():
    """
    file management page API end point
    """
    flist = []
    for key in bucket.list():
        if key.name.encode('utf-8').split('/')[1] != '' and re.match(starts_with_branch(app.config['BRANCH']),
                                                                     key.name.encode('utf-8')):
            flist.append((key.name.encode('utf-8'), key.last_modified))
    payload = {
        "bucket": app.config['AWS_BUCKET'],
        "folder": starts_with_branch(app.config['BRANCH']),
        "files": flist,
    }
    return json.dumps(payload)


@app.route('/', methods=['GET'])
def index():
    """
    home page - with jquery downloader
    """
    return render_template('index.html')


if __name__ == '__main__':
    print('Servicing S3 Bucket %s Branch %s' % (app.config['AWS_BUCKET'], app.config['BRANCH']))
    print('Uploading to S3 Folder %s' % starts_with_branch(app.config['BRANCH']))
    app.run(debug=True, host='0.0.0.0', port=int(app.config['FUP_PORT']))
