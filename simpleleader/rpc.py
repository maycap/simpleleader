import marshal
import socket
import threading


class PeerSocket(object):

    def __init__(self, endpoint, queue):
        self.endpoint = endpoint
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.queue = queue
        self.start()

    def listen(self):
        self.sock.bind(self.endpoint)
        while True:
            content = self.sock.recv(256)
            data = marshal.loads(content)
            self.queue.put(data)

    def send(self, data, addr):
        content = marshal.dumps(data)
        self.sock.sendto(content, addr)

    def start(self):
        task = threading.Thread(target=self.listen)
        task.setDaemon(True)
        task.start()
