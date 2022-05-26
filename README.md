### 简单选主

一些任务只需要一个实例执行，由于高可用要求，需要多台实例。那么多实例通信就成问题，而一些情况下环境比较苛刻，没有组件可以借用。一个简单的选主提上日程。

### 介绍

采用UDP心跳通信，简化流程，特征如下：
1. 初始化时，各个节点均为Follower状态。
2. 开始选主时，所有节点的Follower状态转为Candidate状态，并向其他节点发送自身心跳。
3. 其他节点收到心跳，对比自己心跳，Term比自身小，或者相同是ID比自身大，则节点降为Follower，不在发送心跳。
4. 当Candidate持续心跳有效期时间N内未收到其他节点的心跳，则晋升为Leader，周期发送心跳。

### 安装

```
pip install simpleleader
```

### 使用
加入有三台实例，定义好各自通信端口，简单使用如下：
```commandline
import time
from simpleleader import PeerLeader
endpoint = '127.0.0.1:9001'
cluster = '127.0.0.1:9001,127.0.0.1:9002,127.0.0.1:9003'
peer = PeerLeader(endpoint, cluster)
peer.run()
while 1:
    if peer.is_leader():
        print("%s is leader" % endpoint)
    else:
        print("%s is follower" % endpoint)
    time.sleep(1)
```

### 测试验证

```commandline
python -m simpleleader.tests [实例总数] [当前实例ID,从0开始]
参考
python -m simpleleader.tests 3 0
python -m simpleleader.tests 3 1
python -m simpleleader.tests 3 2
```