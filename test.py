import unittest
import os
import subprocess
import time
import requests

class ContainerTest(unittest.TestCase):
    def setUp(self):
        # self.suffix = os.environ['SUFFIX']
        # self.stamp = os.environ['STAMP']
        command = "docker port docker_igv_js | perl -pne 's/.*://'".format(**os.environ)
        os.environ['PORT'] = subprocess.check_output(command, shell=True).strip().decode('utf-8')
        url='http://localhost:{PORT}/'.format(**os.environ)
        while True:
            if 0 == subprocess.call('curl --fail --silent '+url+' > /dev/null', shell=True):
                break
            print('still waiting for server...')
            time.sleep(1)

    def test_server_up(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContainerTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    lines = [
        'browse:   http://localhost:{PORT}/',
        'clean up: docker ps -qa | xargs docker stop | xargs docker rm'
    ]
    for line in lines:
        print(line.format(**os.environ))
    if result.wasSuccessful():
        print('PASS!')
    else:
        print('FAIL!')
        exit(1)