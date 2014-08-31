from beetle import Commander, Writer

from http import server
from socketserver import TCPServer
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from hashlib import md5
import os

class Updater(FileSystemEventHandler):
    cache = {}
    writer = Writer()

    def __init__(self, serve_directory):
        self.directory = serve_directory

    def on_any_event(self, event):
        # Urgh, ugly directory hack.
        # Could not find an easy way to serve files from a subfolder.
        os.chdir('..')

        for destination, content in self.writer.files():
            digest = md5(content).hexdigest()
            if destination not in self.cache:
                self.writer.write_file(destination, content)
                self.cache[destination] = digest
                print('written')
            elif self.cache[destination] != digest:
                    self.writer.write_file(destination, content)
                    self.cache[destination] = digest
                    print('updated')

        os.chdir(self.directory)

class Server:
    def __init__(self, own_config, config):
        self.directory = config.folders['output']
        self.content = config.folders['content']
        self.port = own_config.get('port', 5000)

    def monitor(self):
        updater = Updater(self.directory)

        observer = Observer()
        observer.schedule(updater, self.content, recursive=True)
        observer.start()

    def serve(self):
        self.monitor()
        os.chdir(self.directory)

        request_handler = server.SimpleHTTPRequestHandler

        httpd = TCPServer(('', self.port), request_handler)
        try:
            print('Preview available at http://0.0.0.0:{}/'.format(self.port))
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()


def register(plugin_config, beetle_config):
    server = Server(plugin_config, beetle_config)
    Commander.add('preview', server.serve, 'Serve the rendered site')
