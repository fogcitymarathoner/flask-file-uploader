import os
import unittest

from app import app


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_app_config_aws(self):
        assert 'hi' == app.config['DUMB']
        assert 'AWS_ACCESS_KEY_ID' in app.config.keys()
        assert 'AWS_SECRET_ACCESS_KEY' in app.config.keys()
        assert 'AWS_BUCKET' in app.config.keys()
        assert 'FUP_PORT' in app.config.keys()
        assert 'UPLOAD_FOLDER' in app.config.keys()
        assert 'THUMBNAIL_FOLDER' in app.config.keys()
        assert 'MAX_CONTENT_LENGTH' in app.config.keys()
        assert 'HEALTHCHECK_TEST_BUCKET' in app.config.keys()

if __name__ == '__main__':
    unittest.main()
