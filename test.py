import unittest
import os
import subprocess
import time
import requests
import sys

class ContainerTest(unittest.TestCase):
    def setUp(self):
        # self.suffix = os.environ['SUFFIX']
        # self.stamp = os.environ['STAMP']
        self.good_url = self.get_url(os.environ['GOOD_NAME'])
        self.bad_url = self.get_url(os.environ['BAD_NAME'])

    def tearDown(self):
        print('good url: ' + self.good_url)

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

    def test_home_page(self):
        response = requests.get(self.good_url)
        self.assertEqual(response.status_code, 200)
        self.assertRegexpMatches(response.text, r'>IGV<')

    def test_data_directory(self):
        response = requests.get(self.good_url + 'data/input.json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContainerTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print('PASS!')
    else:
        print('FAIL!')
        exit(1)