from os import listdir
import json
import SimpleHTTPServer
import SocketServer

def populate_data_directory():
    # files.txt is for testing rather than production use.
    files = '\n'.join(listdir('data'))
    with open('data/files.txt', 'w') as file:
        file.write(files)

    # config.json is actually used by IGV.js.
    options = {
        "palette": ["#00A0B0", "#6A4A3C", "#CC333F", "#EB6841"],
        "locus": "7:55,085,725-55,276,031",

        "reference": {
            "id": "hg19",
            "fastaURL": "//igv.broadinstitute.org/genomes/seq/1kg_v37/human_g1k_v37_decoy.fasta",
            "cytobandURL": "//igv.broadinstitute.org/genomes/seq/b37/b37_cytoband.txt"
        },

        "trackDefaults": {
            "bam": {
                "coverageThreshold": 0.2,
                "coverageQualityWeight": "true"
            }
        },

        "tracks": [
            {
                "name": "Genes",
                "url": "//igv.broadinstitute.org/annotations/hg19/genes/gencode.v18.collapsed.bed",
                "index": "//igv.broadinstitute.org/annotations/hg19/genes/gencode.v18.collapsed.bed.idx",
                "displayMode": "EXPANDED"
            }
        ]
    }
    with open('data/options.json', 'w') as options_file:
        options_file.write(json.dumps(options))

def start_server():
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    SocketServer.TCPServer(("", 80), Handler).serve_forever()

if __name__ == '__main__':
    populate_data_directory()
    start_server()