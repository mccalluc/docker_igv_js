import SimpleHTTPServer
import SocketServer
import json
import os
import requests

from cgi import escape


def get_refinery_input():
    """ Make a GET request to acquire the input data for the container"""
    input_json_url = os.environ.get('INPUT_JSON_URL')
    if input_json_url:
        return requests.get(input_json_url).json()
    return json.loads(os.environ['INPUT_JSON'])


def write_igv_configuration():
    config_data = get_refinery_input()

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
        file_url = node_data["file_url"]
        track = {
            "name": "{} - {}".format(
                node_data["node_solr_info"]["name"],
                file_url
            ),
            "url": file_url
        }
        (base, ext) = os.path.splitext(file_url)
        if '.bam' == ext:
            # Assume that there is only one auxiliary file for bam igv and it's
            # the .bai file.
            track['type'] = 'alignment'
            track['format'] = 'bam'
            track['indexURL'] = node_data['auxiliary_file_list'][0]
        tracks.append(track)
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
    with open('options.json', 'w') as options_file:
        options_file.write(json.dumps(options))


def validate_urls(urls):
    url_status = {}
    for url in urls:
        try:
            # byte-range so we don't download the file; S3 does not support
            # HEAD.
            status = requests.get(
                url,
                headers={'Range': 'bytes=0-0'}
            ).status_code
        except requests.exceptions.RequestException as e:
            status = e.message
        url_status[url] = status
    messages = [
        'Unexpected {} from {}'.format(status, url)
        for url, status in url_status.iteritems()
        if status != 206  # If byte-ranges are handled, should be 206, not 200.
    ]
    if messages:
        raise Exception('\n'.join(messages))


def start_server():
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    SocketServer.TCPServer(("", 80), Handler).serve_forever()


if __name__ == '__main__':
    try:
        write_igv_configuration()
    except Exception as e:
        html = '<html><body><pre>{}</pre></body></html>'.format(
            # Print whole error if message too short
            escape(e.message if ' ' in e.message else repr(e))
        )
        with open('index.html', 'w') as index_file:
            index_file.write(html)
    start_server()
