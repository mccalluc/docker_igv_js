import json
import SimpleHTTPServer
import SocketServer


def populate_igv_configuration():
    with open("data/input.json") as f:
        config_data = json.loads(f.read())

    tracks = []
    assembly = config_data['parameters']['assembly']
    url_base = "https://s3.amazonaws.com/data.cloud.refinery-platform.org/data/igv-reference/{}/".format(
        assembly
    )
    for node_data in config_data["node_info"].values():
        tracks.append(
            {
                "name": "{} - {}".format(
                    node_data["node_solr_info"][
                        "filename_Characteristics_generic_s"],
                    node_data["node_solr_info"]["name"]
                ),
                "url":  node_data["file_url"]
            }
        )
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
