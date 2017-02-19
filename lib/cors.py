"""
CORS - Cross Origin Resource Sharing
functions that generate matterials for S3 uploads
base on browser upload to S3 - https://aws.amazon.com/articles/1434/
"""
import os
import json
import re
import base64
import hmac
import hashlib
from functools import update_wrapper
from datetime import datetime as dt
from datetime import timedelta as td

from flask import jsonify
from flask import make_response
from flask import current_app
from flask import request
from tabulate import tabulate

def starts_with_branch(branch):
    """
    calculates picky starts-with key for policy
    different for each branch
    :return:
    """
    if branch != 'master':
        starts_with = 'upload-%s' % branch
    else:
        starts_with = 'upload'

    return starts_with


def generate_simple_policy(expiry_seconds, bucket, branch):
    """
    timestamp_policy - return json string policy for encoding
    with expiration set expiry seconds ahead
    returns policy in json string
    """
    expiration = (dt.now() + td(seconds=expiry_seconds)).strftime('%Y-%m-%dT%H:%M:%SZ')

    policy = {"expiration": expiration,
              "conditions": [
                  {"bucket": bucket},
                  ["starts-with", "$key", starts_with_branch(branch)],
                  {"acl": "private"},
                  {"success_action_status": '201'},
              ],
              }
    return json.dumps(policy)


class PolicySigner(object):
    payload = {}

    def __init__(self, expire_seconds, bucket, branch, aws_key, secret_key):
        policy = base64.b64encode(generate_simple_policy(int(expire_seconds), bucket, branch))
        signature = base64.b64encode(
            hmac.new(secret_key, policy, hashlib.sha1).digest())

        self.payload = {
            'policy': policy,
            'signature': signature,
            'aws_key': aws_key,
            'bucket': bucket,
            'key': '%s/${filename}' % starts_with_branch(branch),
        }

    def to_table(self):
        return tabulate([(k, self.payload[k])] for k in self.payload.keys())

    def to_json(self):
        """
        return json dictionary so get request gets data filled because jsonify puts the right mime type on return
        """
        return jsonify(self.payload)

def bucket_folder_stats(app, bucket):
    flist = []
    total_use = 0
    for key in bucket.list():
        if key.name.encode('utf-8').split('/')[1] != '' and re.match(starts_with_branch(app.config['BRANCH']), key.name.encode('utf-8') ):
            filename, extension = os.path.splitext(key.name.encode('utf-8'))
            total_use += key.size
            flist.append((key.name.encode('utf-8'), key.last_modified, key.size, extension ))
    return flist, total_use

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    """
    decorator that adjusts CORS permissions of controllers
    :param origin:
    :param methods:
    :param headers:
    :param max_age:
    :param attach_to_all:
    :param automatic_options:
    :return:
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, td):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
