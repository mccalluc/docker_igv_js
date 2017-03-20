from os import listdir
import json
import SimpleHTTPServer
import SocketServer
import re

def as_track(file):
    return {
        "name": re.sub(r'.*\/', '', file),
        "url": 'data/' + file,
        "format": re.sub(r'.*\.', '', file)
        # TODO: indexURL if BAM
    }

def populate_data_directory():
    # files.txt is really for testing rather than production use.
    files = '\n'.join(listdir('data'))
    with open('data/files.txt', 'w') as list_file:
        list_file.write(files)

    # options.json is actually used by IGV.js.
    # TODO: How does Refinery communicate the genome assembly?
    assembly = "hg19"
    url_base = "https://s3.amazonaws.com/data.cloud.refinery-platform.org/data/igv-reference/{}/".format(assembly)

    tracks = [as_track(f) for f in listdir('data') if f not in ["files.txt", "hello_world.txt"]]
    tracks.append({
        "name": "Genes",
        "type": "annotation",
        "format": "bed",
        "sourceType": "file",
        "url": url_base + "refGene.bed",
        "indexURL": url_base + "refGene.bed.tbi",
        "visibilityWindow": 300000000,
        "displayMode": "EXPANDED"
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
    populate_data_directory()
    start_server()