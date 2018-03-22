import json
import requests
import SimpleHTTPServer
import SocketServer
from cgi import escape


def write_igv_configuration():
    with open("data/input.json") as f:
        config_data = json.loads(f.read())

    tracks = []
    assemblies = [
        parameter['value'] for parameter in config_data['parameters']
            if parameter['name'] == 'Genome Build'
    ]
    assert len(assemblies) == 1
    assembly = assemblies[0]

    url_base = "https://s3.amazonaws.com/data.cloud.refinery-platform.org/data/igv-reference/{}/".format(
        assembly
    )
    for node_data in config_data["node_info"].values():
        tracks.append(
            {
                "name": "{} - {}".format(
                    node_data["node_solr_info"]["name"],
                    node_data["file_url"]
                ),
                "url":  node_data["file_url"]
            }
        )
    reference = {
        "fastaURL": url_base + assembly + ".fa",
        "indexURL": url_base + assembly + ".fa.fai",
        "cytobandURL": url_base + "cytoBand.txt",
    }

    validate_urls(reference.values())

    options = {
        "reference": reference,
        "tracks": tracks
    }
    with open('data/options.json', 'w') as options_file:
        options_file.write(json.dumps(options))


def validate_urls(urls):
    url_status = {}
    for url in urls:
        try:
            # byte-range so we don't download the file; S3 does not support HEAD.
            status = requests.get(url, headers={'Range': 'bytes=0-0'}).status_code
        except requests.exceptions.RequestException, e:
            status = e.message
        url_status[url] = status
    messages = [
        'Unexpected {} from {}'.format(status, url)
        for url, status in url_status.iteritems()
        if status != 206  # If byte-ranges are handled, should be 206, not 200.
    ]
    if messages:
        raise StandardError('\n'.join(messages))


def start_server():
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    SocketServer.TCPServer(("", 80), Handler).serve_forever()


if __name__ == '__main__':
    try:
        write_igv_configuration()
    except StandardError, e:
        html = '<html><body><pre>{}</pre></body></html>'.format(
            escape(e.message if ' ' in e.message else repr(e))  # Print whole error if message too short
        )
        with open('index.html', 'w') as index_file:
            index_file.write(html)
    start_server()
