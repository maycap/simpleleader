import sys
import time

from simpleleader.leader import PeerLeader


def make_cluster(n):
    cluster_list = []
    port = 9000
    for _ in range(n):
        port += 1
        endpoint = '127.0.0.1:%s' % port
        cluster_list.append(endpoint)
    return cluster_list


def run(count, current):
    cluster_list = make_cluster(count)
    cluster = ','.join(cluster_list)
    endpoint = cluster_list[current]
    s = PeerLeader(endpoint, cluster)
    s.run()
    while True:
        if s.is_leader():
            print("%s is leader" % endpoint)
        else:
            print("%s is follower" % endpoint)
        time.sleep(1)


if __name__ == '__main__':
    args = sys.argv
    count = int(args[1])
    current = int(args[2])
    run(count, current)
