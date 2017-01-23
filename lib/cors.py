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
from datetime import datetime as dt
from datetime import timedelta as td

from flask import jsonify
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
