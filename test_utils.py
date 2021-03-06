import _thread
import docker
import os
import socket

from http.server import HTTPServer, SimpleHTTPRequestHandler


class TestFixtureServer(object):

    def __init__(self):
        self.port = 9999
        self.ip = self.get_python_server_ip()

    def get_python_server_ip(self):
        # https://stackoverflow.com/a/166589
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        host_ip = s.getsockname()[0]
        s.close()
        return host_ip

    def _start_server(self):
        server = HTTPServer((self.ip, self.port), SimpleHTTPRequestHandler)
        server.serve_forever()

    def start_server_in_background(self):
        # start the server in a background thread
        _thread.start_new_thread(self._start_server, ())


class TestContainerRunner(object):

    def __init__(self):
        self.client = docker.from_env()
        self.image_name = "docker_igv_js"
        self.repository = "gehlenborglab/docker_igv_js"
        self.containers = []
        self.test_fixture_server = TestFixtureServer()
        self.test_fixture_server.start_server_in_background()

        self._pull_image()
        self._build_image()

    def __enter__(self):
        self.run()

    def __exit__(self, *args):
        if not os.environ.get("CONTINUOUS_INTEGRATION"):
            self.cleanup_containers()

    def _pull_image(self):
        self.client.images.pull(self.repository + ":latest")

    def _build_image(self):
        print("Building image: {}".format(self.image_name))
        self.client.images.build(
            path="context",
            tag=self.image_name,
            rm=True,
            forcerm=True,
            cache_from=[self.repository]
        )

    def run(self):
        print("Starting TestContainerRunner...")
        for test_fixture in os.listdir("input_fixtures"):
            print("Creating container: {}".format(test_fixture))
            container = self.client.containers.run(
                self.image_name,
                detach=True,
                name=test_fixture,
                environment={
                    "INPUT_JSON_URL":
                        "http://{}:{}/input_fixtures/{}/input.json".format(
                            self.test_fixture_server.ip,
                            self.test_fixture_server.port,
                            test_fixture
                        )
                },
                ports={"80/tcp": None},
                publish_all_ports=True,
                extra_hosts={socket.gethostname(): self.test_fixture_server.ip}
            )
            self.containers.append(container)

    def cleanup_containers(self):
        print("Cleaning up TestContainerRunner containers...")
        print(self.containers)
        for container in self.containers:
            container.remove(force=True, v=True)
