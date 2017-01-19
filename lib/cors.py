"""
CORS - Cross Origin Resource Sharing
functions that generate matterials for S3 uploads
base on browser upload to S3 - https://aws.amazon.com/articles/1434/
"""
import json
import base64
import hmac
import hashlib
from datetime import datetime as dt
from datetime import timedelta as td

from flask import jsonify
from tabulate import tabulate


def generate_simple_policy(expiry_seconds, bucket, branch):
    """
    timestamp_policy - return json string policy for encoding
    with expiration set expiry seconds ahead
    returns policy in json string
    """
    expiration = (dt.now() + td(seconds=expiry_seconds)).strftime('%Y-%m-%dT%H:%M:%SZ')

    if branch != 'master':
        starts_with = 'upload-%s' % branch
    else:
        starts_with = 'upload'

    policy = {"expiration": expiration,
              "conditions": [
                  {"bucket": bucket},
                  ["starts-with", "$key", starts_with],
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
            'key': 'upload-%s/${filename}' % branch,
        }

    def to_table(self):
        return tabulate([(k, self.payload[k])] for k in self.payload.keys())

    def to_json(self):
        """
        return json dictionary so get request gets data filled because jsonify puts the right mime type on return
        """
        return jsonify(self.payload)
