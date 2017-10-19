import json
import SimpleHTTPServer
import SocketServer


def populate_igv_configuration():
    with open("data/input.json") as f:
        config_data = json.loads(f.read())

    tracks = []
    assembly = "hg19"
    url_base = "https://s3.amazonaws.com/data.cloud.refinery-platform.org/data/igv-reference/{}/".format(
        assembly
    )

    for url in config_data["file_relationships"]:
        tracks.append({
            "name": url.split("/")[-1],
            "url":  url,
        })
    reference = {
        "fastaURL": url_base + assembly + ".fa",
        "indexURL": url_base + assembly + ".fa.fai",
        "cytobandURL": url_base + "cytoBand.txt",
    }

    options = {
        "reference": reference,
        "tracks": tracks
    }

    with open('data/options.json', 'w') as options_file:
        options_file.write(json.dumps(options))


def start_server():
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    SocketServer.TCPServer(("", 80), Handler).serve_forever()


if __name__ == '__main__':
    populate_igv_configuration()
    start_server()
