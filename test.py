import unittest
import os
import subprocess
import time
import requests
import sys

class ContainerTest(unittest.TestCase):
    def setUp(self):
        # This is inefficient, but that doesn't matter: it's fast enough.
        self.good_url = self.get_url(os.environ['GOOD_NAME'])
        self.bad_url = self.get_url(os.environ['BAD_NAME'])

    def get_url(self, name):
        command = "docker port {} | perl -pne 's/.*://'".format(name)
        port = subprocess.check_output(command, shell=True).strip().decode('utf-8')
        url = 'http://localhost:{}/'.format(port)
        for i in xrange(5):
            if 0 == subprocess.call('curl --fail --silent ' + url + ' > /dev/null', shell=True):
                return url
            print('Still waiting for server...')
            time.sleep(1)
        self.fail('Server never came up: ' + name)

    def test_good_home_page(self):
        response = requests.get(self.good_url)
        self.assertEqual(200, response.status_code)
        self.assertIn('>IGV<', response.text)

    def test_bad_home_page(self):
        response = requests.get(self.bad_url)
        self.assertEqual(200, response.status_code)  # Not ideal, but ok for now.
        self.assertIn(
            'Unexpected 404 from https://s3.amazonaws.com/data.cloud.refinery-platform.org/data/igv-reference/hgFAKE/cytoBand.txt',
            response.text
        )

    def test_data_directory(self):
        response = requests.get(self.good_url + 'data/input.json')
        self.assertEqual(200, response.status_code)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContainerTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print('PASS!')
    else:
        print('FAIL!')
        exit(1)