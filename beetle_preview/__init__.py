from http import server
from socketserver import TCPServer
import os


class Server:
    def __init__(self, own_config, config, builder):
        self.directory = config.folders['output']
        self.port = own_config['port']
        self.builder = builder

    def serve(self):
        os.chdir(self.directory)

        request_handler = server.SimpleHTTPRequestHandler

        httpd = TCPServer(('', self.port), request_handler)

        httpd.serve_forever()


def register(plugin_config, config, commander, builder, content_renderer):
    server = Server(plugin_config, config, builder)
    commander.add('preview', server.serve, 'Serve the rendered site')