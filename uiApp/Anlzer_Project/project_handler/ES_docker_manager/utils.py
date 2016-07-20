__author__ = 'mpetyx'

from docker import Client

class ESContainer:

    def create(self):
        cli = Client(base_url='tcp://127.0.0.1:2375')
        container = cli.create_container(image='elasticsearch:latest', command='/bin/sleep 30')
        print(container)
        