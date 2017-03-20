# Create any necessary files on in data/:

# TODO

# Start a static file server:

import SimpleHTTPServer
import SocketServer

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
SocketServer.TCPServer(("", 80), Handler).serve_forever()