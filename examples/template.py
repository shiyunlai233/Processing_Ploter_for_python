# "运行在普通的python3环境中，通过对画图器的rpc调用实现实时可视化"

import socket, json, pickle

class RPCProxy:
    def __init__(self, connection):
        self._connection = connection
        self.data = []

    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            self.data.append(json.dumps((name, args, kwargs)))
        return do_rpc

    def send_all(self):
        self._connection.send(pickle.dumps(self.data, protocol=0))
        self.data.clear()

import socket

address = ('127.0.0.1', 12345)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
rpc = RPCProxy(s)

############################################################
# 上面的程序是每一个使用processing画图器的python程序都会使用的
#  rpc就是我们的processing画图器的实例，后面的程序就都是对他进行“发号施令”了
