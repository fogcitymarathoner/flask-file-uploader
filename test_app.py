import os
import unittest

from app import app


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.config.from_object('config')

    def tearDown(self):
        pass

    def test_app_config_aws(self):
        print(self.app.config)
        assert 1 == 2

if __name__ == '__main__':
    unittest.main()
