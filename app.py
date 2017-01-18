#!/usr/local/bin/python
'''
# Author: Ngo Duy Khanh
# Email: ngokhanhit@gmail.com
# Git repository: https://github.com/ngoduykhanh/flask-file-uploader
# This work based on jQuery-File-Upload which can be found at
# https://github.com/blueimp/jQuery-File-Upload/
'''
import os
import json
import base64
import hmac
import hashlib
from PIL import Image
import PIL
import simplejson
import traceback
import boto
from boto.exception import S3ResponseError
from botocore.client import ClientError
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import send_from_directory
from flask.ext.bootstrap import Bootstrap
from werkzeug import secure_filename

from lib.upload_file import uploadfile
from lib.cors import PolicySigner

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
print bucket
if bucket is None:
    print "Creating Bucket %s" % app.config['AWS_BUCKET']
    s3.create_bucket(app.config['AWS_BUCKET'])

ALLOWED_EXTENSIONS = set(
    ['txt', 'gif', 'png', 'jpg', 'jpeg', 'bmp', 'rar', 'zip', '7zip', 'doc', 'docx'])
IGNORED_FILES = set(['.gitignore'])

bootstrap = Bootstrap(app)


def allowed_file(filename):
    '''
    check to see if file extenstion is allowed
    '''
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """

    i = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i = i + 1

    return filename


def create_thumbnai(image):
    '''
    make thumbnail of incoming pic
    '''
    try:
        basewidth = 80
        img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], image))
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        img.save(os.path.join(app.config['THUMBNAIL_FOLDER'], image))

        return True
    except:
        print traceback.format_exc()
        return False


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    '''
    perform the download locally
    '''
    if request.method == 'POST':
        file = request.files['file']
        #pprint (vars(objectvalue))

        if file:
            filename = secure_filename(file.filename)
            filename = gen_file_name(filename)
            mimetype = file.content_type


            if not allowed_file(file.filename):
                result = uploadfile(
                    name=filename, type=mimetype, size=0, not_allowed_msg="Filetype not allowed")

            else:
                # save file to disk
                uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(uploaded_file_path)

                # create thumbnail after saving
                if mimetype.startswith('image'):
                    create_thumbnai(filename)
                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = uploadfile(name=filename, type=mimetype, size=size)
            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        # get all file in ./data directory
        files = [
            f for f in os.listdir(
                app.config['UPLOAD_FOLDER']) \
                    if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f)) and \
                        f not in IGNORED_FILES]
        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], f))
            file_saved = uploadfile(name=f, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})

    return redirect(url_for('index'))


@app.route("/delete/<string:filename>", methods=['DELETE'])
def delete(filename):
    '''
    removed file locally
    '''
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)

            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)
            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})


# serve static files
@app.route("/thumbnail/<string:filename>", methods=['GET'])
def get_thumbnail(filename):
    '''
    deliver thumbnail
    '''
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename=filename)


@app.route("/data/<string:filename>", methods=['GET'])
def get_file(filename):
    '''
    deliver file name
    '''
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename=filename)

@app.route('/api/v1/cors-credentials', methods=['GET'])
def s2_cors_credentials():
    '''
    s3_cors_credentials
    '''
    # 10 minute expiration
    signer = PolicySigner( \
                 600, app.config['AWS_BUCKET'], app.config['BRANCH'], \
                 app.config['AWS_ACCESS_KEY_ID'], app.config['AWS_SECRET_ACCESS_KEY'])
    return signer.to_json()


@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    home page
    '''
    return render_template('index.html')


if __name__ == '__main__':
    print('Servicing S3 Bucket %s Branch %s' % (app.config['AWS_BUCKET'], app.config['BRANCH']))
    app.run(debug=True, host='0.0.0.0', port=int(app.config['FUP_PORT']))
