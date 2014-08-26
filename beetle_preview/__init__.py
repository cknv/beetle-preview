from http import server
from socketserver import TCPServer
import os


class Server:
    def __init__(self, own_config, config):
        self.directory = config.folders['output']
        self.port = own_config.get('port', 5000)

    def serve(self):
        os.chdir(self.directory)

        request_handler = server.SimpleHTTPRequestHandler

        httpd = TCPServer(('', self.port), request_handler)
        try:
            print('Preview available at http://0.0.0.0:{}/'.format(self.port))
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()


def register(plugin_config, config, commander, builder, content_renderer):
    server = Server(plugin_config, config)
    commander.add('preview', server.serve, 'Serve the rendered site')
