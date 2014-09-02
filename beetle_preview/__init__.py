from beetle.context import commander, writer

from http import server
from socketserver import TCPServer
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from hashlib import md5
import os

class Updater(FileSystemEventHandler):
    def __init__(self, serve_directory, writer):
        self.directory = serve_directory
        self.writer = writer
        self.cache = {}

    def on_any_event(self, event):
        # Urgh, ugly directory hack.
        # Could not find an easy way to serve files from a subfolder.
        os.chdir('..')
        for destination, content in self.writer.files():
            digest = md5(content).hexdigest()
            full_destination = os.path.join(self.directory, destination)
            if destination not in self.cache:
                self.writer.write_file(full_destination, content)
                self.cache[destination] = digest
                print('written', destination)
            elif self.cache[destination] != digest:
                    self.writer.write_file(full_destination, content)
                    self.cache[destination] = digest
                    print('updated', destination)

        os.chdir(self.directory)

class Server:
    def __init__(self, own_config, config, updater):
        self.directory = config.folders['output']
        self.content = config.folders['content']
        self.port = own_config.get('port', 5000)
        self.updater = updater

    def monitor(self):
        observer = Observer()
        observer.schedule(self.updater, self.content, recursive=True)
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
    updater = Updater(beetle_config.folders['output'], writer)
    server = Server(plugin_config, beetle_config, updater)
    commander.add('preview', server.serve, 'Serve the rendered site')
