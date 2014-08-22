import SimpleHTTPServer
import SocketServer
import os


class Server:
    def __init__(self, own_config, config, builder):
        self.directory = config.folders['output']
        self.port = own_config['port']
        self.builder = builder

    def serve(self):
        os.chdir(self.directory)

        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

        httpd = SocketServer.TCPServer(('', self.port), Handler)

        httpd.serve_forever()


def register(plugin_config, config, commander, builder, content_renderer):
    server = Server(plugin_config, config, builder)
    commander.add('serve', server.serve, 'Serve the rendered site')
