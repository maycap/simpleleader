import queue
import threading
import time
from enum import Enum

from simpleleader.rpc import PeerSocket


class Role(Enum):
    follower = 1
    candidate = 2
    leader = 3


class PeerLeader(object):

    def __init__(self, endpoint, cluster, expire=7, vow_time=2):
        self.endpoint = endpoint
        self.cluster = cluster
        self.queue = queue.Queue(maxsize=10)
        self.peer = None
        self.lock = threading.Lock()
        self.expire = expire
        self.vow_time = vow_time
        self.id = None
        self.followers = None
        self.heartbeat = None
        self.status = None

    def reset(self):
        self.heartbeat = {
            "term": float('inf'),
            "current_ts": float('-inf'),
            'id': -255
        }
        self.status = Role.follower.value

    def vote(self):
        self.heartbeat = {
            "term": time.time(),
            "current_ts": time.time(),
            'id': self.id
        }
        self.status = Role.candidate.value

    @classmethod
    def str_to_addr(cls, info):
        info = info.split(':')
        return info[0], int(info[1])

    def init(self):
        cluster_list = self.cluster.split(',')
        cluster_list.sort()
        self.id = cluster_list.index(self.endpoint)
        self.peer = PeerSocket(self.str_to_addr(self.endpoint), self.queue)
        cluster_list.remove(self.endpoint)
        self.followers = list(self.str_to_addr(i) for i in cluster_list)
        self.reset()

    def update_heartbeat(self, data):
        if self.heartbeat['id'] == data['id']:
            return
        if self.heartbeat['term'] > data['term']:
            self.heartbeat = data
        if data['term'] == self.heartbeat['term'] and data['id'] > self.heartbeat['id']:
            self.heartbeat = data

        # update status
        if self.heartbeat['id'] != self.id:
            self.status = Role.follower.value

    def send_followers(self):
        self.heartbeat['current_ts'] = time.time()
        for follower in self.followers:
            self.peer.send(self.heartbeat, follower)

    def recv_leader(self):
        while not self.queue.empty():
            data = self.queue.get_nowait()
            self.update_heartbeat(data)

    def clean(self):
        if self.heartbeat['id'] == self.id:
            if self.heartbeat['term'] + self.expire < time.time():
                self.status = Role.leader.value
            return
        if self.heartbeat['current_ts'] + self.expire < time.time():
            self.vote()

    def watch(self):
        while True:
            with self.lock:
                if self.status == Role.leader.value:
                    self.send_followers()
                elif self.status == Role.candidate.value:
                    self.recv_leader()
                    self.send_followers()
                else:
                    self.recv_leader()
                self.clean()
            time.sleep(0.5)

    def is_leader(self):
        with self.lock:
            if self.status == Role.leader.value:
                return True
            return False

    def run(self):
        self.init()
        task = threading.Thread(target=self.watch)
        task.setDaemon(True)
        task.start()
