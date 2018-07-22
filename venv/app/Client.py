# coding=utf-8
'''
Created on 2015-10-13
订阅模式，如果设置了过滤条件，那么只会接收到以过滤条件开头的消息
@author: kwsy2015
'''
import sys
import zmq
import _thread
import time
#from time import time
import timeutils
from app.Calculate import Calculate
import json
from app.Creat_blockchain import Blockchain
from hashlib import sha256
import os
from app.data import *


class Client(object):
    #客户端的三种状态：1.发送添加请求   2.接收添加广播  3.发送计算结果  4.接收更新广播  5.发送修改请求
    state = 2
    lastMessage = ''
    def __init__(self):
        #self.chain_demo = Blockchain()
        return None

    def run_listen4NewPub(self,delay):
        context = zmq.Context()
        #  Socket to talk to server
        print("State 2: Connecting to server...")
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://localhost:5010")
        socket.setsockopt_string(zmq.SUBSCRIBE, '')
        while True:
            #  Get the reply.
            if self.state == 2 :
                print("wait for new block publish")
                jsonmessage = socket.recv()
                jsonmessage = str(jsonmessage, encoding="utf8")
                block = json.loads(jsonmessage)
                print("Receive Public Message:" + jsonmessage)
                self.state = 3
                if jsonmessage != self.lastMessage:
                    self.sendResult(block)  # 发送计算结果
                    self.lastMessage = jsonmessage
            time.sleep(delay)
        return None

    def run_listen4SucPub(self,delay):
        context = zmq.Context()
        #  Socket to talk to server
        print("State 4: wait for suc from server...")
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://localhost:5030")
        socket.setsockopt_string(zmq.SUBSCRIBE, '')
        while True:
            #  Get the reply.
            if self.state == 3:
                print("wait for succeed publish")
                jsonmessage = socket.recv()
                jsonmessage = str(jsonmessage, encoding="utf8")
                if jsonmessage != "error":                                          #如果被篡改就不写入
                    ID = self.get_chainID(jsonmessage)
                    self.saveNewBlock2home(jsonmessage, ID)
                #追加区块到本地相应chain文件
                #path = "D:/configFiles/chain" + ID + ".json"
                #with open(path, 'a',encoding='gbk',errors='ignore') as f:
                    #f.write(jsonmessage)
                #f.close()

                self.state = 2
            time.sleep(delay)
        return None


    def run_listen4UpdatePub(self,delay):
        context = zmq.Context()
        #  Socket to talk to server
        print("State 5: wait for update from server...")
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://localhost:5040")
        socket.setsockopt_string(zmq.SUBSCRIBE, '')
        while True:
            #  Get the reply.
            if self.state == 2:                                     #非文件添加时再更新，防止同时打开文件造成读写冲突
                #print("等待更新。。。")
                jsonmessage = socket.recv()
                jsonmessage = str(jsonmessage, encoding="utf8")
                #print(jsonmessage)
                ID = self.get_chainID(jsonmessage)
                print(ID+"号商品更新啦！！")
                #jsonmessage.replace("u","\u")
                #print("添加反斜杠后的字符串：" + jsonmessage)
                print(jsonmessage)
                self.saveNewBlock2home(jsonmessage, ID)
            time.sleep(delay)
        return None


    def sendNewBlock(self,block):
        context = zmq.Context()
        print("State 1: Send new block to Server.")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5001")
        #socket.send_string('I want to new a block.')
        socket.send_json(block)
        print('I want to new a block.')
        response = socket.recv()
        print(response)
        return None

    def sendResult(self,block):
        cal = Calculate()
        print(block)

        data = str(block['information'])           ###朱一凡改
        num = 0
        y = -1
        while num != 5:
            y += 1
            while sha256(f'{data*y}'.encode()).hexdigest()[:2] != "00":
                y += 1
            print(sha256(f'{data*y}'.encode()).hexdigest())
            print(y)
            print(num)
            num += 1


        jsonMessage = json.dumps(block, ensure_ascii=False)
        ID = block['information']['id']
        oldMessage = self.readBlock2home(ID)
        path = os.getcwd() + "\\app\\static\\chains\\chain" + ID + ".json"
        if not (os.path.isfile(path)):                                   #如果文件不存在则创建
            f = open(path, 'w')
            f.close()
        if oldMessage == '':
            lastline = "{'nb': 0, 'timest': 1531838408.7642026, 'information': [], 'proof': 5, 'previous_hash': 001111, 'hash': '004f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b9'}"
            lastline = str(lastline, encoding="utf8")
            with open(path, 'w') as f:
                f.write(lastline)
            f.close()

        #发送
        context = zmq.Context()
        print("State 3: Send result to Server.")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5020")
        print("客户端发送整条链的信息！")
        print(oldMessage + jsonMessage)
        socket.send_string(oldMessage + jsonMessage)
        #socket.send_string(jsonMessage)
        response = socket.recv()
        print(response)
        return None

    def run_editBlock(self,block):                                          #修改区块，发送请求
        ID = block['transaction']['id']
        index = block['nb']
        path = os.getcwd() + "\\app\\static\\chains\\chain" + ID + ".json"
        if not (os.path.isfile(path)):  # 如果文件不存在则创建
            f = open(path, 'w')
            f.close()

        #寻找修改的区块并修改
        oldMessage = ''
        cal = Calculate()
        lasthash = block['hash']
        with open(path, 'r') as f:
            i = 0
            for line in f.readlines():
                if i<index:
                    line = str(line, encoding="utf8")
                    oldMessage += linestr
                elif i == index:
                    oldMessage += json.dumps(block, ensure_ascii=False) + '\n'
                elif i > index:
                    #修改前哈希
                    #line = line.decode("utf-8", "ignore")
                    line = str(line, encoding="utf8")
                    Block = json.loads(line.replace("'", '"'))
                    Block['previous_hash'] = lasthash
                    #计算当前区块新哈希
                    newHash = cal.proof_of_work_edit(Block['information'],lasthash)
                    Block['hash'] = newHash
                    lasthash = newHash
                    oldMessage += json.dumps(Block, ensure_ascii=False)
            print("区块"+ i + "修改完毕！")
            i+=1
        f.close()

        return None

    def saveNewBlock2home(self,jsonMessage,ID):                        #将新区块链的信息加入文件
        #path = "static/blockAndChain/Chain1.json"
        path = os.getcwd() + "\\app\\static\\chains\\chain" + ID + ".json"
        if not (os.path.isfile(path)):  # 如果文件不存在则创建
            f = open(path, 'w')
            f.close()

        jsonMessages = jsonMessage.split('\8')
        with open(path, 'w') as f:                                 #清空文件
            f.write('')
            f.close()
        i = 0
        length = len(jsonMessages)
        with open(path, 'a', encoding="utf8") as f:
            while i < length:
                if jsonMessages[i] != '' and jsonMessages[i] != '\n':
                    f.write(jsonMessages[i])
                    print(jsonMessages[i])
                    f.write("\n")
                i += 1
        f.close()

    def readBlock2home(self,ID):                        #读取相应文件中的旧信息
        path = os.getcwd() + "\\app\\static\\chains\\chain" + ID + ".json"
        if not (os.path.isfile(path)):  # 如果文件不存在则创建
            f = open(path, 'w')
            f.close()

        oldMessage = ''
        with open(path, 'r') as f:
            for line in f.readlines():
                if line != '':
                    #line = str(line, encoding="utf8")
                    line = line.strip("\n")
                    oldMessage += line + "\8"
        f.close()
        return oldMessage

    def set_chain(self,chain):
        self.chain_demo = chain

    def get_chainID(self,jsonMessage):                                            #传入某一条链的json串，返回此商品编号
        jsonMessages = jsonMessage.split('\8')
        block = json.loads(jsonMessages[1])
        return block['information']['id']

    def newBlock(self, information, ID,zeroString):
        #初始化区块
        from time import time
        block = {
            'nb': '',
            'timest': time(),
            'information': information,
            'proof': 5,
            'previous_hash': '',
            'hash': '',
        }
        #获取区块链末端:
        path = os.getcwd() + "\\app\\static\\chains\\chain" + ID + ".json"
        if not (os.path.isfile(path)):  # 如果文件不存在则创建
            f = open(path, 'w')
            f.close()

        lastline = ''
        with open(path, 'r') as f:
            for line in f:
                lastline = line
        if lastline == '':
            lastline = "{'nb': 0, 'timest': 1531838408.7642026, 'information': [], 'proof': 5, 'previous_hash': '0011', 'hash': '004f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b9'}"
            #lastline =  bytes(lastline, encoding="utf8")
            with open(path, 'w') as f:
                f.write(lastline)
            f.close()
        lastline = lastline.replace("'", '"')
        print(lastline)
        lastBlock = json.loads(lastline)
        #获取nb：
        block['nb'] = int(lastBlock['nb']) + 1
        # 获取previous_hash
        block['previous_hash'] = lastBlock['hash']
        #获取hash
        y = 0
        data = str(information) + lastBlock['hash']                                  #计算哈希值的参数是数据加前哈希值
        length = len(zeroString)
        while sha256(f'{data*y}'.encode()).hexdigest()[:length] != zeroString:
            y += 1
        block['hash'] = sha256(f'{data*y}'.encode()).hexdigest()
        block['proof'] = 5
        return block


    def utf82uni(self,data):
        data['id'] = data['id'].decode("utf-8")
        data['time'] = data['time'].decode("utf-8")
        data['address'] = data['address'].decode("utf-8")
        data['character'] = data['character'].decode("utf-8")
        data['contact_info'] = data['contact_info'].decode("utf-8")
        data['description'] = data['description'].decode("utf-8")
        return data