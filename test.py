import unittest
import os
import subprocess
import time
import requests


class ContainerTest(unittest.TestCase):

    def get_url(self, name_key):
        name = os.environ[name_key]
        command = "docker port {} | perl -pne 's/.*://'".format(name)
        port = subprocess.check_output(command, shell=True).strip().decode('utf-8')
        url = 'http://localhost:{}/'.format(port)
        for i in xrange(5):
            if 0 == subprocess.call('curl --fail --silent ' + url + ' > /dev/null', shell=True):
                return url
            print('Still waiting for server...')
            time.sleep(1)
        self.fail('Server never came up: ' + name)

    # Good configuration:

    def test_good_home_page(self):
        good_url = self.get_url('GOOD_NAME')
        response = requests.get(good_url)
        self.assertEqual(200, response.status_code)
        self.assertIn('>IGV<', response.text)

    def test_data_directory(self):
        good_url = self.get_url('GOOD_NAME')
        response = requests.get(good_url + 'data/input.json')
        self.assertEqual(200, response.status_code)

    # Bad configurations:

    def test_missing_assembly_home_page(self):
        missing_assembly_name = self.get_url('MISSING_ASSEMBLY_NAME')
        response = requests.get(missing_assembly_name)
        self.assertEqual(200, response.status_code)  # Not ideal, but ok for now.
        self.assertIn(
            'Unexpected 404 from https://s3.amazonaws.com/data.cloud.refinery-platform.org/data/igv-reference/hgFAKE/cytoBand.txt',
            response.text
        )


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContainerTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print('PASS!')
    else:
        print('FAIL!')
        exit(1)