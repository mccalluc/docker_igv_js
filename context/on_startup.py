from os import listdir

# Create any necessary files in data/:

files = ' '.join(listdir('data'))
with open('data/hello_world_generated.txt', 'w') as file:
    file.write('Hello '+ files)

# TODO: config.json

# Start a static file server:

import SimpleHTTPServer
import SocketServer

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
SocketServer.TCPServer(("", 80), Handler).serve_forever()