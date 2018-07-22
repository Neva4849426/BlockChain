# -*- coding:utf-8 -*-
__author__ = 'yxy'
import zmq
import time
import timeutils
import _thread
import json
import threading
from Creat_blockchain import Blockchain
import os
from data.chain import chain
from data.hash import hash
from data.info import info


lastMessage = ''
#服务器状态 ： 1.等待区块加入请求 2.广播新区块信息 3.接收所有区块返回信息

#在每个线程中都新建一个socket的原因：ZMQ不允许一个SOCKET被多个线程共享。
#端口号不同的原因：程序运行时一个端口上不能绑定多个socket
def run_listen4add(delay):
    global state,if_run_pubNewBMessage,chainList
    #state：服务器所处阶段，if_run_pubNewBMessage:是否进行发布新信息的线程，lastestMessage：同步好的最新账本
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5001")
    while True:
        if state == 1:
            #  Get the reply.
            print("wait for client" )
            jsonMessage = socket.recv()
            state = 3
            jsonMessage = str(jsonMessage, encoding="utf-8")
            print("Receive Block Message:" + jsonMessage)
            socket.send_string('Server has recived.')
            if if_run_pubNewBMessage == 0:
                _thread.start_new_thread(run_pubNewBMessage, (jsonMessage,))
                if_run_pubNewBMessage = 1
        time.sleep(delay)

def run_listen4login(delay):
    global state,if_run_pubNewBMessage,chainList
    #state：服务器所处阶段，if_run_pubNewBMessage:是否进行发布新信息的线程，lastestMessage：同步好的最新账本
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5060")
    while True:
        jsonMessage = socket.recv()
        jsonMessage = str(jsonMessage, encoding="utf-8")
        Info = info()
        Info.login_valid(username)

        time.sleep(delay)


def run_pubNewBMessage(jsonMessage):
    global state,if_run_pubNewBMessage
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5010")
    while state==3:
        time.sleep(10)
        #数据库发布新信息
        socket.send_string(jsonMessage)
        print("Server has send NewBMessage")
    if_run_pubNewBMessage = 0



def run_pubSucMessage(message):
    global state,if_run_pubSucMessage
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5030")
    for request in range(10):
        time.sleep(10)
        socket.send_string(message)
        print("Server has send SuceMessage")

    if_run_pubSucMessage = 0


def run_listen4response(delay):
    global state,if_run_pubSucMessage,lastMessage
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5020")
    while True:
        #  Get the reply.
        since = time.time()
        responseList = []
        i= 0
        while time.time() - since < 10:                              #将10s内传递过来的信息全部保存到临时队列中
            print(time.time() - since)
            message = socket.recv()
            message = str(message, encoding="utf8")
            responseList.append(message)
            i+=1
        print("State 3: Server had recieved ")
        print(i)
        print(" response of blocks!")

        #防篡改检验
        Hash = hash()
        Chain = chain()
        ID = get_chainID(message)
        message_sql = Chain.read(ID)
        hash_mysql = Hash.read(ID)

        index = 0
        print(len(responseList))
        while index < len(responseList):
            message = responseList[index]
            print("message" + message)
            print(index)
            result = check_all(message_sql, message, hash_mysql)
            print(result)
            if result == "数据库信息未被修改，且客户端信息正确":

                # 数据库本地更新
                if (message != lastMessage):
                    print("服务器数据库文件更新啦！")
                    print(message)
                    saveNewBlock2home(message, ID)
                    lastMessage = message
                break
            else:
                if index + 1 < len(responseList):
                    index += 1
                    message = responseList[index]
                else:
                    message = "error"
                    break



        state = 1
        # 广播加入成功信息
        if if_run_pubSucMessage == 0:
            _thread.start_new_thread(run_pubSucMessage, (message,))  # 返回json格式的整个链
            if_run_pubSucMessage = 1
        socket.send_string('Server has recived.')

        time.sleep(delay)

def run_listen4UpdatePub(delay):                             #向游客端和参与者端不断发布最新的账本
    global chainList
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5040")
    rootDir = "D:\configFiles_Server"
    while True:
        #print("正在同步。。。" )
        print(state)
        time.sleep(5)
        if state == 1:                                       #当state=1时，服务器数据库的数据已更新到最新，可以发送


            #遍历所有chain表中所有链并发送
            Chain = chain()
            allchains = Chain.readall()
            for jsonm in allchains:
                #print(jsonm)
                #jsonm.replace("u", '\u')
                socket.send_string(jsonm)

        print("Server has send update message")

def run_listen4edit(delay):
    global state, if_run_pubEditBMessage, chainList
    # state：服务器所处阶段，if_run_pubNewBMessage:是否进行发布新信息的线程，lastestMessage：同步好的最新账本
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5050")
    while True:
        if state == 1:
            #  Get the reply.
            print("wait for client")
            jsonMessage = socket.recv()
            state = 3
            jsonMessage = str(jsonMessage, encoding="utf-8")
            print("Receive Block Message:" + jsonMessage)
            socket.send_string('Server has recived.')
            if if_run_pubNewBMessage == 0:
                _thread.start_new_thread(run_pubNewBMessage, (jsonMessage,))
                if_run_pubNewBMessage = 1
        time.sleep(delay)

def saveNewBlock2home(jsonMessage,ID):                        #将新区块链的信息加入文件：服务器文件每个chain文件只有一行
    c =chain()
    oldMessage = c.read(ID)                                               #读取旧数据
    print(oldMessage)
    if oldMessage == '':
        c.add(ID,jsonMessage)
    else:
        c.modify(ID,oldMessage+jsonMessage)                                   #将新数据加入数据库
    print("将" + jsonMessage + "加入数据库中")



def get_chainID(jsonMessage):                                            #传入某一条链的json串，返回此商品编号
    print(jsonMessage)
    jsonMessages = jsonMessage.split('\8')
    block = json.loads(jsonMessages[1].replace("'", '"'))
    return block['information']['id']


def check_all(message_sql, message_client, hash_mysql):
    if message_sql == '':
        return "数据库信息未被修改，且客户端信息正确"
    chain_sql = Blockchain()
    chain_sql.check_info_and_hash(message_sql)
    is_chain_sql = chain_sql.inspect_chain_form()  # 检验数据库中存储区块链是否成链
    if not is_chain_sql:
        length = len(chain_sql.chain)
        i = 1
        while i < length - 1:
            if chain_sql.chain[i + 1]['previous_hash'] != chain_sql.chain[i]['hash']:
                chain_sql.chain[i + 1]['previous_hash'] = chain_sql.chain[i]['hash']
            i += 1
    is_same_sql = chain_sql.inspect_hash(hash_mysql)  # 检验数据库中哈希值数组与数据库中区块链中哈希值是否相同

    chain_client = Blockchain()
    chain_client.check_info_and_hash(message_client)
    is_chain_client = chain_client.inspect_chain_form()  # 检验客户端传过来的区块链是否成链
    if not is_chain_client:
        length = len(chain_client.chain)
        i = 1
        while i < length - 1:
            if chain_client.chain[i + 1]['previous_hash'] != chain_client.chain[i]['hash']:
                chain_client.chain[i + 1]['previous_hash'] = chain_client.chain[i]['hash']
            i += 1
    is_same_clnsql = chain_client.inspect_hash(hash_mysql)

    re_1 = "数据库区块链信息被修改，但客户端信息正确"
    re_2 = "数据库区块链信息被修改，且客户端信息无法判断虚实"
    re_3 = "数据库信息未被修改，且客户端信息正确"
    re_4 = "数据库信息未被修改，但客户端信息被修改"
    if not is_same_sql:
        if is_same_clnsql:
            return re_1
        if not is_same_clnsql:
            return re_2
    if is_same_sql:
        if is_same_clnsql:
            return re_3
        if not is_same_clnsql:
            return re_4






state = 1
if_run_pubSucMessage = 0
if_run_pubNewBMessage = 0


print("Server weak up!")

try:
    _thread.start_new_thread(run_listen4add, (2,))  #虽然线程函数中只有一个参数，但是逗号必加。因为函数名和参数列表分开传的话参数列表必须是个元组
    _thread.start_new_thread(run_listen4response, (2,))
    _thread.start_new_thread(run_listen4UpdatePub, (2,))
except:
    print("Error: unable to start thread")
while True:
    time.sleep(100)


