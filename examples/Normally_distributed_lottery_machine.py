# "运行在普通的python3环境中，通过对画图器的rpc调用实现实时可视化"
# 这里的例子展示了使用画图器模拟一个“正态分布抽奖机”

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

import time
import math
from random import random
from copy import  deepcopy

class Bi_tree():
    def __init__(self, root_x, root_y, grid_len, ceng_n):
        self.root_x = root_x
        self.root_y = root_y
        self.grid_len = grid_len
        self.ceng_n = ceng_n
        self.nodes = [(m, n) for m in range(ceng_n) for n in range(m+1)]
        self.ans_n = [1] * ceng_n
        self.ans_pos = [self.mn_to_xy(ceng_n, i+0.5)[0] for i in range(ceng_n+1)]

    
    def mn_to_xy(self, m, n):
        "第m行， n列"
        x = self.root_x + (-0.5 * m + n) * self.grid_len
        y = self.root_y + m * self.grid_len
        return x, y
    
    def display(self):
        for m, n in self.nodes:
            x, y = self.mn_to_xy(m, n)
            rpc.fill(200)
            rpc.circle(x, y, 5)
        for n, pos in zip(self.ans_n, self.ans_pos):
            rpc.rect(pos, 600, self.grid_len-4, n*5)



class Ball():
    def __init__(self, loc_x, loc_y, v):
        self.loc_tar = loc_x, loc_y
        self.loc_bef = loc_x, loc_y
        self.loc_now = loc_x, loc_y
        self.v = v
        self.move = False
        self.move_call = None

    def set_move_tar(self, tar_x, tar_y):
        self.loc_tar = tar_x, tar_y
        self.move = True
        
    def update(self):
        out = None
        if self.move:
            dis_x = self.loc_tar[0] - self.loc_now[0]
            dis_y = self.loc_tar[1] - self.loc_now[1]
            dis = math.sqrt(dis_x ** 2 + dis_y ** 2)
            if dis <= self.v:
                self.loc_now = self.loc_tar
                if self.move_call:
                    # print("move_call")
                    self.move = False
                    self.loc_bef = self.loc_tar
                    out = self.move_call(self)
            else:
                move_x = self.v / dis * dis_x
                move_y = self.v / dis * dis_y
                self.loc_now = self.loc_now[0] + move_x, self.loc_now[1] + move_y
        return out
            
    def display(self):
        rpc.fill(250,50,50)
        rpc.circle(self.loc_now[0], self.loc_now[1], 10)
        # rpc.stroke(120)
        # rpc.line(self.loc_bef[0], self.loc_bef[1], self.loc_tar[0], self.loc_tar[1])



k = 30 
def set_ball_move_tar(ball):
    m, n = ball.mn
    if m < k-1:
        ball.mn = (m+1, n+1) if random() < 0.5 else (m+1 ,n)
        ball.set_move_tar(*bt.mn_to_xy(*ball.mn))
    elif m == k-1:
        ball.v += 10
        x, _ = bt.mn_to_xy(*ball.mn)
        ball.set_move_tar(x, 600)
        ball.mn = m+1, n
    else:
        bt.ans_n[n] += 0.2
        del ball

bt = Bi_tree(300, 20, 13, k)
ball = Ball(*bt.mn_to_xy(0, 0), 2)
ball.set_move_tar(*bt.mn_to_xy(0, 0))
ball.move_call = set_ball_move_tar
ball.mn = (0, 0)

balls = []





for i in range(3000):
    rpc.clear_all()
    if i % 1 == 0:
        balls.append(deepcopy(ball))
    if i % 20 == 0:
        print(len(balls))
    rpc.background(0)
    bt.display()
    for b in balls:
        b.display()
    for b in reversed(balls):
        out = b.update()
        if out:
            del balls[i]
            print("out")
    rpc.send_all()
    time.sleep(0.02)
