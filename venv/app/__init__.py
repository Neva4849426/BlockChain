from flask import Flask, render_template,send_from_directory,redirect,url_for,flash,request,json
from flask_bootstrap import Bootstrap
from app.Client import Client
from app.data.info import info
import cgi, cgitb
import zmq
import sys
import time
import _thread
import json
import os
import qrcode
import random
from flask import jsonify
import importlib
import time
# from app.data.info import info

identity=''
client = None
import json
from app.Creat_blockchain import Blockchain

if_init = 0
#time.sleep(100)
#client.sendResult("I have worked out!")
'''
chain.new_information'001', '8102年41月7日', '潍坊', '朱一凡', '18801039357', '醪糟很好吃嘻嘻嘻')
client.sendNewBlock(chain.get_information))
'''

# 创建一个flask 实例
app = Flask(__name__)
Bootstrap(app)



@app.route('/')
@app.route('/login.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    global identity,client

    client = Client()
    # client.start()
    _thread.start_new_thread(client.run_listen4UpdatePub, (2,))

    if request.method == 'GET':
        return render_template("login.html")

    elif request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        # 调用操作数据库的类
        newinfo = info()
        rs = newinfo.login_valid(username)
        if rs == None:
            return render_template("login_error.html")
        else:
            row = rs[0]
            id = row[0]
            name = row[1]
            pwd = row[2]
            identity = row[3]
        # if email in User.users and password == User.users[email]['password']:
        # user = User()


        if username == name and password == pwd:
            return render_template("home.html" )
        else:
            return render_template("login_fail.html")


    # return render_template("login.html",title_name = '欢迎，请登录！')

@app.route('/register', methods=['GET', 'POST'])
def register():
        if request.method == 'GET':
            return render_template("register.html")

        elif request.method == 'POST':
            data = request.get_json()
            print(data)
            username = data['username']
            password = data['password']
            password2 = data['password2']
            identity = data['city']
            newinfo = info()
            rs = newinfo.login_valid(username)
            if rs != None:
                result = {'if': '0'}
                return jsonify(result)
            elif username == '' or password == '' or password2 == '':
                result = {'if': '1'}
                return jsonify(result)
            elif password != password2:
                result = {'if': '2'}
                return jsonify(result)
            else:
                newinfo.add(username, password, identity)
                result = {'if': '3'}
                return jsonify(result)


@app.route('/home')
@app.route('/home.html')
def home():
    global identity, client
    newid = identity
    return render_template("home.html", identity=newid)


@app.route('/edit')
@app.route('/edit/search', methods=['GET', 'POST'])
def edit():
    global identity,client
    newid = identity
    if request.method == 'POST':
        type = request.content_type
        if(type=='application/json; charset=UTF-8'):
            temp={'id':'',
                  'time':'',
                  'address':'',
                  'character':'',
                  'contact_info':'',
                  'description':'',
                  'add_chain':''}
            data = request.get_json()
            if(data['type']=='1'):
                path = os.getcwd() + "\\app\\static\\products\\" + newid + data['id'] + ".json"
                if (data['id'] == ''):
                    result = {'if': '0'}
                    return jsonify(result)

                if not (os.path.isfile(path)):
                    f = open(path, 'w',errors='ignore')
                    f.close()
                    data['add_chain'] = "0"
                else:
                    with open(path, 'r') as f:
                        line = f.readline()
                        temp = json.loads(line)
                        data['add_chain'] = temp['add_chain']
                    f.close()

                temp['id']=data['id']
                temp['time']=data['time']
                temp['address'] = data['address']
                temp['character'] = data['character']
                temp['contact_info'] = data['contact_info']
                temp['description'] = data['description']
                temp['add_chain'] = data['add_chain']

                with open(path, 'w',errors='ignore') as f:
                    f.write(json.dumps(temp, ensure_ascii=False))
                f.close()

                result = {'if': '1'}
                return jsonify(result)
            else:
                if (data['id'] != ""):
                    path = os.getcwd() + "\\app\\static\\products\\"  + newid + data['id'] + ".json"
                    if not (os.path.isfile(path)):
                        result = {'if': '2'}
                        return jsonify(result)
                    else:
                        os.remove(path)
                        result = {'if': '1'}
                        return jsonify(result)
                else:
                    result = {'if': '0'}
                    return jsonify(result)

            return render_template("edit.html", identity=newid)
			
        goodID = request.form['goodID']
        path = os.getcwd() + "\\app\\static\\products\\" + newid  + goodID + ".json"
    if request.method == 'GET':
        testid = request.args.get('id')
        if (testid == None):
            return render_template("edit.html", identity=newid)
        path = os.getcwd() + "\\app\\static\\products\\" + newid  + testid + ".json"

    # 检验该编号的文件是否存在
    if not (os.path.isfile(path)):
        warning = "不存在该编号的商品，您可以输入并保存新的信息。"
        return render_template("edit.html", warning=warning, identity=newid)
    with open(path, 'r') as f:
        line = f.readline()
        data = json.loads(line)
    f.close()
    #data = client.utf82uni(data)
    id = data['id']
    time = data['time']
    address = data['address']
    character = data['character']
    contact_info = data['contact_info']
    description = data['description']

    return render_template("edit.html", identity=newid, 
							goodsid=id,id=id, time=time,
                           address=address, character=character,
                           contact_info=contact_info,
                           description=description)



@app.route('/show')
@app.route('/show/search', methods=['GET', 'POST'])
def show():
    time1 = '时间'
    pre1 = '前哈希值'
    place1 = '地点'
    person1 = '人物'
    tele1 = '联系方式'
    desc1 = '描述'
    time2 = '时间'
    pre2 = '前哈希值'
    place2 = '地点'
    person2 = '人物'
    tele2 = '联系方式'
    desc2 = '描述'
    time3 = '时间'
    pre3 = '前哈希值'
    place3 = '地点'
    person3 = '人物'
    tele3 = '联系方式'
    desc3 = '描述'
    time4 = '时间'
    pre4 = '前哈希值'
    place4 = '地点'
    person4 = '人物'
    tele4 = '联系方式'
    desc4 = '描述'
    time5 = '时间'
    pre5 = '前哈希值'
    place5 = '地点'
    person5 = '人物'
    tele5 = '联系方式'
    desc5 = '描述'
    goodID=''
    if request.method == 'POST':
        goodID = request.form['goodID']
        path = os.getcwd() + "\\app\\static\\chains\\chain" + goodID + ".json"

        # 检验该编号的区块链文件是否存在
        if not (os.path.isfile(path)):
            warning = "不存在该编号的商品区块链。"
            return render_template("show.html", warning=warning, 
									time1=time1,pre1=pre1, place1=place1, person1=person1, tele1=tele1, desc1=desc1,
                                   time2=time2,pre2=pre2, place2=place2, person2=person2, tele2=tele2, desc2=desc2,
                                   time3=time3, pre3=pre3,place3=place3, person3=person3, tele3=tele3, desc3=desc3,
                                   time4=time4, pre4=pre4,place4=place4, person4=person4, tele4=tele4, desc4=desc4,
                                   time5=time5,pre5=pre5, place5=place5, person5=person5, tele5=tele5, desc5=desc5)
        else:
            with open(path, 'r',errors='ignore') as f:   #,'utf-8'
                for line in f.readlines():
                    if (line == '\n'):
                        continue
                    print(line)
                    dict = json.loads(line.replace("'", '"'),encoding="utf-8")
                    new_dic = dict['information']
                    #new_dic = client.utf82uni(new_dic)
                    if (dict['nb'] == 0):
                        continue
                    if (dict['nb'] == 1):
                        time1 = new_dic['time']
                        pre1=dict['previous_hash']
                        place1 = new_dic['address']
                        person1 = new_dic['character']
                        tele1 = new_dic['contact_info']
                        desc1 = new_dic['description']
                    if (dict['nb'] == 2):
                        time2 = new_dic['time']
                        pre2 = dict['previous_hash']
                        place2 = new_dic['address']
                        person2 = new_dic['character']
                        tele2 = new_dic['contact_info']
                        desc2 = new_dic['description']
                    if (dict['nb'] == 3):
                        time3 = new_dic['time']
                        pre3 = dict['previous_hash']
                        place3 = new_dic['address']
                        person3 = new_dic['character']
                        tele3 = new_dic['contact_info']
                        desc3 = new_dic['description']
                    if (dict['nb'] == 4):
                        time4 = new_dic['time']
                        pre4 = dict['previous_hash']
                        place4 = new_dic['address']
                        person4 = new_dic['character']
                        tele4 = new_dic['contact_info']
                        desc4 = new_dic['description']
                    if (dict['nb'] == 5):
                        time5 = new_dic['time']
                        pre5 = dict['previous_hash']
                        place5 = new_dic['address']
                        person5 = new_dic['character']
                        tele5 = new_dic['contact_info']
                        desc5 = new_dic['description']
            return render_template("show.html", id=goodID, time1=time1, place1=place1, person1=person1, tele1=tele1,
                                   desc1=desc1,
                                   time2=time2, place2=place2, person2=person2, tele2=tele2, desc2=desc2,
                                   time3=time3, place3=place3, person3=person3, tele3=tele3, desc3=desc3,
                                   time4=time4, place4=place4, person4=person4, tele4=tele4, desc4=desc4,
                                   time5=time5, place5=place5, person5=person5, tele5=tele5, desc5=desc5,
                                   pre1=pre1,pre2=pre2,pre3=pre3,pre4=pre4,pre5=pre5)

    return render_template("show.html",time1=time1, place1=place1, person1=person1, 								tele1=tele1, desc1=desc1,
                                   time2=time2, place2=place2, person2=person2, tele2=tele2, desc2=desc2,
                                   time3=time3, place3=place3, person3=person3, tele3=tele3, desc3=desc3,
                                   time4=time4, place4=place4, person4=person4, tele4=tele4, desc4=desc4,
                                   time5=time5, place5=place5, person5=person5, tele5=tele5, desc5=desc5,
                                   pre1=pre1,pre2=pre2,pre3=pre3,pre4=pre4,pre5=pre5)


@app.route('/blockList')
@app.route('/blockList/search', methods=['GET', 'POST'])
def blockList():
    img1='../static/images/detail-2.jpg'
    if request.method == 'POST':
        book = [0,0,0,0,0,0,0,0,0,0]
        goodID = request.form['goodID']

        path = os.getcwd() + "\\app\\static\\chains\\chain" + goodID + ".json"
        # 检验该编号的区块链文件是否存在
        if not (os.path.isfile(path)):
            warning = "不存在该编号的商品区块链。"
            return render_template("blockList.html",img1=img1,warning=warning,block="区块不存在")
        else:
            string = ''
            with open(path, 'r',encoding="utf-8") as load_f:
                for line in load_f:
                    if (line == '\n'):
                        continue
                    data = json.loads(line.replace("'", '"'))
                    #data['information'] = client.utf82uni(data['information'])
                    if (data['nb'] == 0):
                        continue
                    # 二维码
                    if (data['nb'] == 1):
                        block_identity = '原产地'
                        if (book[1]==0):
                            string += '商品编号：' + data['information'][
                                'id'] + '\n' + '身份：' + block_identity + '\n' + '发生时间：' + \
                                      data['information'][
                                          'time'] + '\n' + '商品信息：' + '\n' + '地点：' + data['information'][
                                          'address'] + '\n' + '人物:' + \
                                      data['information']['character'] + '\n' + '联系方式：' + data['information'][
                                          'contact_info'] + '\n' + '描述：' + data['information'][
                                          'description'] + '\n' + '------------------------------' + '\n'

                        book[1] = 1

                    if (data['nb'] == 2):
                        block_identity = '加工厂'
                        if(book[2]==0):
                            string += '商品编号：' + data['information'][
                                'id'] + '\n' + '身份：' + block_identity + '\n' + '发生时间：' + \
                                      data['information'][
                                          'time'] + '\n' + '商品信息：' + '\n' + '地点：' + data['information'][
                                          'address'] + '\n' + '人物:' + \
                                      data['information']['character'] + '\n' + '联系方式：' + data['information'][
                                          'contact_info'] + '\n' + '描述：' + data['information'][
                                          'description'] + '\n' + '------------------------------' + '\n'
                        book[2] = 1

                    if (data['nb'] == 3):
                        block_identity = '运输'
                        if(book[3]==0):
                            string += '商品编号：' + data['information'][
                                'id'] + '\n' + '身份：' + block_identity + '\n' + '发生时间：' + \
                                      data['information'][
                                          'time'] + '\n' + '商品信息：' + '\n' + '地点：' + data['information'][
                                          'address'] + '\n' + '人物:' + \
                                      data['information']['character'] + '\n' + '联系方式：' + data['information'][
                                          'contact_info'] + '\n' + '描述：' + data['information'][
                                          'description'] + '\n' + '------------------------------' + '\n'
                        book[3] = 1

                    if (data['nb'] == 4):
                        block_identity = '入库'
                        if(book[4]==0):
                            string += '商品编号：' + data['information'][
                                'id'] + '\n' + '身份：' + block_identity + '\n' + '发生时间：' + \
                                      data['information'][
                                          'time'] + '\n' + '商品信息：' + '\n' + '地点：' + data['information'][
                                          'address'] + '\n' + '人物:' + \
                                      data['information']['character'] + '\n' + '联系方式：' + data['information'][
                                          'contact_info'] + '\n' + '描述：' + data['information'][
                                          'description'] + '\n' + '------------------------------' + '\n'
                        book[4] = 1

                    if (data['nb'] == 5):
                        block_identity = '销售'
                        if (book[4] == 0):
                            string += '商品编号：' + data['information'][
                                'id'] + '\n' + '身份：' + block_identity + '\n' + '发生时间：' + \
                                      data['information'][
                                          'time'] + '\n' + '商品信息：' + '\n' + '地点：' + data['information'][
                                          'address'] + '\n' + '人物:' + \
                                      data['information']['character'] + '\n' + '联系方式：' + data['information'][
                                          'contact_info'] + '\n' + '描述：' + data['information'][
                                          'description'] + '\n' + '------------------------------' + '\n'
                        book[5] = 1


                    print(type(data['nb']))
                    print(data)
            load_f.close()
            img = qrcode.make(string)
            img.save(os.getcwd() + "\\app\\static\\img\\Some" + data['information']['id'] + ".png")
            img1 = '../static/img/Some' + data['information']['id'] + '.png?' + ''.join(
                ['%.2X' % random.randint(0, 255) for i in range(8)])
            return render_template("blockList.html", id="商品编号：" + goodID, img1=img1, block="区块")

    return render_template("blockList.html",img1=img1,block="区块")





@app.route('/blockEdit')
@app.route('/blockEdit/addtochain', methods=['GET', 'POST'])
def blockEdit():
    global identity
    newid = identity

    return render_template("blockEdit.html",identity = newid,
                           time="时间",
                           address="地点", character="人物",
                           contact_info="联系方式",
                           description="描述",
                           button1="修改区块",button2="加入区块链",btntype="btn btn-primary disabled"
                           ,btntype2="btn btn-primary disabled")


@app.route('/blockEdit/search', methods=['GET', 'POST'])
def blockSearch():
    global identity
    newid = identity
    if request.method == 'POST':
        goodID = request.form['goodID']
        path = os.getcwd()+"\\app\\static\\products\\" + newid  + goodID + ".json"
        #path = "D:/configFiles/" + goodID + ".json"
        # 检验该编号的文件是否存在
        if not (os.path.isfile(path)):
            warning = "不存在该编号的商品！"
            return render_template("blockEdit.html",identity = newid,
									warning=warning,id=goodID,
                                   time="时间",
                                   address="地点", character="人物",
                                   contact_info="联系方式",
                                   description="描述",
                                   button1="修改区块",button2="加入区块链",
                                   btntype="btn btn-primary disabled",
                                    btntype2="btn btn-primary disabled")
        with open(path, 'r') as f:
            line = f.readline()
            data = json.loads(line)
        f.close()
        #data = client.utf82uni(data)
		
        id = data['id']
        time = data['time']
        add_chain = data['add_chain']
        if(add_chain=="1"):
            button2 = "已加入区块链"
            btntype="btn btn-primary disabled"
            btntype2="btn btn-primary"
        else:
            button2 = "加入区块链"
            btntype = "btn btn-primary"
            btntype2 = "btn btn-primary disabled"
        address = data['address']
        character = data['character']
        contact_info = data['contact_info']
        description = data['description']

        return render_template("blockEdit.html", identity = newid,
                               id=id, time=time,
                               address=address, character=character,
                               contact_info=contact_info,
                               description=description,button1="修改区块",button2=button2
                               , btntype=btntype,
                               btntype2=btntype2)


    return render_template("blockEdit.html",identity = newid,
                           time="时间",
                           address="地点", character="人物",
                           contact_info="联系方式",
                           description="描述",
                           button1="修改区块",button2="加入区块链",btntype=btntype,
                           btntype2=btntype2)

@app.route('/blockEdit/waitToAdd', methods=['GET', 'POST'])
def waitToAdd():
    global identity,if_init,client
    newid = identity
    href="javascript: window.location.href = 'http://127.0.0.1:5000/blockEdit'"
    text1='加入区块链'
    if request.method == 'GET':
        testid = request.args.get('id')
        if(testid==None or testid==''):
            return render_template("blockEdit.html",identity=newid, warning="请输入商品编号！", id=testid,
                           button1="修改区块",button2="加入区块链",btntype="btn btn-primary",btntype2="btn btn-primary")
        return render_template('wait.html',text1=text1,
                               text2='您将要把编号为'+ testid + '的商品加入区块链。点击确认发送请求。',goodID=testid,href=href)
    if request.method == 'POST':
        goodID = request.args.get('id')
        path = os.getcwd() + "\\app\\static\\products\\" + newid  + goodID + ".json"


        # 检验该编号的文件是否存在
        if not (os.path.isfile(path)):
            warning = "不存在该编号的商品！"
            return render_template("blockEdit.html", identity=newid, warning=warning, id=goodID,
                           button1="修改区块",button2="加入区块链",btntype="btn btn-primary",btntype2="btn btn-primary")
        with open(path, 'r') as f:
            line = f.readline()
            data = json.loads(line)
        f.close()

        information = {
            'id': data['id'],
            'time': data['time'],
            'address': data['address'],
            'character': data['character'],
            'contact_info': data['contact_info'],
            'description': data['description'],
        }

        #data = client.utf82uni(data)
        id = data['id']
        time = data['time']
        address = data['address']
        character = data['character']
        contact_info = data['contact_info']
        description = data['description']

        # 加入区块链的操作，向服务器发请求。
        _thread.start_new_thread(client.run_listen4SucPub, (2,))
        _thread.start_new_thread(client.run_listen4NewPub, (2,))

        newblock = client.newBlock(information, data['id'],"00")
        print(newblock)
        client.sendNewBlock(newblock)


        # 如果请求成功，改写本地商品信息文件('add_chain'改为'1')
        data['add_chain'] = "1"

        with open(path, 'w',errors='ignore') as f:
            f.write(json.dumps(data, ensure_ascii=False))
        f.close()

        return jsonify(data)

@app.route('/blockEdit/waitToEdit', methods=['GET', 'POST'])
def waitToEdit():
    global identity,client
    newid = identity
    href="javascript: window.location.href = 'http://127.0.0.1:5000/blockEdit'"
    text1 = '修改区块链'
    if request.method == 'GET':
        testid = request.args.get('id')
        if(testid==None or testid==''):
            return render_template("blockEdit.html",identity=newid, warning="请输入商品编号！", id=testid,
                           button1="修改区块",button2="加入区块链",btntype="btn btn-primary",btntype2="btn btn-primary")
        return render_template('wait.html',text1=text1,
                               text2='您将要修改编号为'+ testid + '，'+ newid +'的区块链信息。点击确认发送请求。',goodID=testid,href=href)
    if request.method == 'POST':
        goodID = request.args.get('id')
        path = os.getcwd() + "\\app\\static\\products\\" + newid  + goodID + ".json"
        #path = "D:/configFiles/" + goodID + ".json"

        # 检验该编号的文件是否存在
        if not (os.path.isfile(path)):
            warning = "不存在该编号的商品！"
            return render_template("blockEdit.html", identity=newid, warning=warning, id=goodID,
                           button1="修改区块",button2="加入区块链",btntype="btn btn-primary",btntype2="btn btn-primary")
        with open(path, 'r') as f:
            line = f.readline()
            data = json.loads(line)
        f.close()

        # 修改区块链的操作，计算修改后哈希。
        information = {
            'id': data['id'],
            'time': data['time'],
            'address': data['address'],
            'character': data['character'],
            'contact_info': data['contact_info'],
            'description': data['description'],
        }


        #data = client.utf82uni(data)
        id = data['id']
        time = data['time']
        address = data['address']
        character = data['character']
        contact_info = data['contact_info']
        description = data['description']

        newblock = client.newBlock(information, data['id'],"000000")
        _thread.start_new_thread(client.sendEditBlock, (newblock,))

        return jsonify(data)
@app.route('/productList/waitToAdd', methods=['GET', 'POST'])
def waitToAdd2():
    global identity,client
    newid = identity
    href = "javascript: window.location.href = 'http://127.0.0.1:5000/productList'"
    text1 = '加入区块链'
    if request.method == 'GET':
        testid = request.args.get('id')
        return render_template('wait.html',text1=text1,
                               text2='您将要把编号为'+ testid + '的商品加入区块链。点击确认发送请求。',goodID=testid,href=href)
    if request.method == 'POST':
        goodID = request.args.get('id')
        path = os.getcwd() + "\\app\\static\\products\\" + newid  + goodID + ".json"

        with open(path, 'r') as f:
            line = f.readline()
            data = json.loads(line)
        f.close()

        data = client.utf82uni(data)
        id = data['id']
        time = data['time']
        address = data['address']
        character = data['character']
        contact_info = data['contact_info']
        description = data['description']


        # 加入区块链的操作，向服务器发请求。





        # 如果请求成功，改写本地商品信息文件('add_chain'改为'1')

        data['add_chain']="1"

        with open(path, 'w',errors='ignore') as f:
            f.write(json.dumps(data, ensure_ascii=False))
        f.close()



        return jsonify(data)

@app.route('/productList')
def productList():
    global identity
    newid=identity
    path2 = os.getcwd() + '\\app\\templates\\productList.html'
    with open(path2, 'w',encoding="utf8", errors='ignore') as file:
        line='<!DOCTYPE html><html><!-- Head --><head><title>商品信息</title>' \
             '\r\n<!-- Meta-Tags --><meta name="viewport" content="width=device-width, initial-scale=1">' \
             '\r\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8">' \
             '\r\n<meta name="keywords" content=""><script type="application/x-javascript"> ' \
             '\r\naddEventListener("load", function() { setTimeout(hideURLbar, 0); }, false); function hideURLbar(){ window.scrollTo(0,1); } </script>' \
             '\r\n<!-- //Meta-Tags --><link rel="stylesheet" href="../static/css/bootstrap.min.css"	type="text/css" media="all">' \
             '\r\n<link rel="stylesheet" href="../static/css/style.css?v=2018" 		type="text/css" media="all">' \
             '\r\n<link rel="stylesheet" href="../static/css/smoothbox.css" 	type="text/css" media="all">' \
             '\r\n<link rel="stylesheet" href="../static/css/font-awesome.min.css" 	 type="text/css" media="all">' \
             '\r\n<link rel="stylesheet" href="../static/fonts/fontawesome-webfont.ttf" type="text/css" media="all">' \
             '\r\n<script type="text/javascript" src="../static/js/jquery-2.1.4.min.js"></script></head><!-- //Head -->' \
             '\r\n<!-- Body --><body><!-- Header --><div class="header-aits" id="home">' \
             '\r\n<div class="header-info-w3ls"><div class="top-contact-aits-w3l container">' \
             '\r\n<p>Call us directly @ +001813799371820 or mail us to ' \
             '\r\n<a class="mail" href="mailto:mail@example.com">992999406@qq.com</a> between 10:00 and 16:00</p></div>' \
             '\r\n<!-- Navigation --><nav class="navbar container navbar-inverse navbar-default"><div class="navbar-header">' \
             '\r\n<button type="button" class="navbar-toggle collapsed" ' \
             '\r\ndata-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">' \
             '\r\n<span class="sr-only">Toggle navigation</span><span class="icon-bar"></span>' \
             '\r\n<span class="icon-bar"></span> <span class="icon-bar"></span></button><!-- Logo -->' \
             '\r\n<div class="logo"><a class="navbar-brand logo-w3l button">商品追踪溯源系统</a></div><!-- //Logo -->' \
             '\r\n</div><div id="navbar" class="navbar-collapse navbar-right collapse">' \
             '\r\n<ul class="nav navbar-nav navbar-right cross-effect" id="cross-effect">' \
             '\r\n<li><a class="cross-effect nav-link" href="http://127.0.0.1:5000/home">首页</a></li>' \
             '\r\n<li><a class="cross-effect nav-link" href="http://127.0.0.1:5000/blockList">区块二维码</a></li>' \
             '\r\n<li><a class="cross-effect nav-link" href="http://127.0.0.1:5000/show">区块信息</a></li>' \
             '\r\n<li><a class="cross-effect nav-link" href="http://127.0.0.1:5000/productList">商品信息</a></li>' \
             '\r\n<li><a class="cross-effect nav-link" href="http://127.0.0.1:5000/edit">商品编辑</a></li>' \
             '\r\n<li><a class="cross-effect nav-link" href="http://127.0.0.1:5000/blockEdit">区块编辑</a></li>' \
             '\r\n<li><a class="cross-effect nav-link" href="http://127.0.0.1:5000/">退出</a></li></ul>' \
             '\r\n</div><!-- //Navbar-Collapse --></nav><!-- //Navigation --></div>' \
             '\r\n<div class="details-w3lsagile" id="details">' \
             '\r\n<div class="container"></div><div class="clearfix"></div></div></div><!-- //Header -->' \
             '\r\n<!-- Details --><div class="details-w3lsagile" id="details">' \
             '\r\n<div class="container">' \
             '\r\n<div class = "row">' \
             '\r\n<div class="col-md-7" style="inset:1px -1px 1px #444, inset -1px 1px 1px #444;">' \
             '\r\n<h4 class="text-danger">{{warning}}</h4>' \
             '\r\n</div><div class="col-md-4 " style="inse: 1px -1px 1px #444, inset -1px 1px 1px #444;">' \
             '\r\n</div>' \
             '<br><br></div>'\
             '\r\n<div class = "row"><br><br></div><div class="details-grids-w3lsagile">'
        file.write(line)
    file.close()
    path=os.getcwd()+'\\app\\static\\products\\'
    files = os.listdir(path)
    for file in files:
        if not(file.startswith(newid)):
            continue
        new_path = path + file
        with open(new_path, 'r',errors='ignore') as f:
            line = f.readline()
            print(line)
            data = json.loads(line)
        f.close()
        with open(path2, 'a',encoding='utf8',errors='ignore') as file:
            string='\r\n<div class="col-md-4 col-sm-4 details-grid-w3lsagile details-grid-1-w3lsagile">\r\n' \
                   '<div class=" details-grid1-w3lsagile">\r\n	' \
                   '<div class="details-grid-info-w3lsagile">\r\n' \
                   '<table class="table table-bordered">\r\n' \
                   '<thead>\r\n' \
                   '<tr class = "info">\r\n' \
                   '<th scope="row">商品编号：</th>\r\n' \
                   '<th class = "text-center" id="productID">'
            string+=data['id']+'\r\n</th>\r\n' \
                               '</tr>\r\n' \
                               '</thead>\r\n' \
                               '<tbody>\r\n' \
                               '<tr>\r\n' \
                               '<th scope="row">时间：</th>\r\n' \
                               '<td class = "text-center" type="text"  id="time" name="time">'
            string+=data['time']+'\r\n</td>\r\n' \
                                 '</tr>\r\n' \
                                 '<tr>\r\n' \
                                 '<th scope="row">身份：</th>\r\n' \
                                 '<td class = "text-center" type="text"  id="identity" name="identity">'
            string+='{{identity}}'+'\r\n</td>\r\n' \
                                   '</tr>\r\n' \
                                   '<tr>\r\n' \
                                   '<th scope="row">\r\n' \
                                   '地点：</th>\r\n' \
                                   '<td class = "text-center" type="text"  id="place" name="place">'
            string+=data['address']+'\r\n</td>\r\n' \
                                    '</tr>\r\n<tr>\r\n' \
                                    '<th scope="row">人物：</th>\r\n' \
                                    '<td class = "text-center"  type="text"  id="person" name="person">'
            string+=data['character']+'\r\n</td>\r\n' \
                                      '</tr>\r\n' \
                                      '<tr>\r\n' \
                                      '<th scope="row">联系方式：</th>\r\n' \
                                      '<td class = "text-center" type="text"  id="tele" name="tele">'
            string+=data['contact_info']+'\r\n</td>\r\n' \
                                         '</tr>\r\n' \
                                         '<tr>\r\n' \
                                         '<th scope="row">描述：</th>\r\n' \
                                         '<td class = "text-center" type="text"  id="desc" name="desc">'
            string+=data['description']+'\r\n</td>\r\n' \
                                        '</tr>\r\n' \
                                        '</tbody>\r\n</table>'
            if (data['add_chain']=='0'):
                add_chain='加入区块链'
                state='"'
            else:
                add_chain='已加入区块链'
                state = ' disabled"'
            string += '\r\n<button class="btn btn-primary'+state+' type="button" id="button1" onclick="javascript:window.location.href='
            string += "'http://127.0.0.1:5000/productList/waitToAdd?id=" + data['id'] + "'" + '">'+add_chain+'</button>\r\n'
            string+='\r\n<button class="btn btn-primary" type="button" style="margin-left:40px" id="button1" onclick="javascript:window.location.href='
            string+="'http://127.0.0.1:5000/edit/search?id="+ data['id']+"'"+'">编辑</button>\r\n'
            string+= '</div>\r\n</div>\r\n</div>\r\n'
            file.write(string)
            file.close()
    with open(path2, 'a',encoding='utf8',errors='ignore') as file:
        string='\r\n</div>\r\n</div>\r\n<div class="clearfix"></div>\r\n</div>\r\n<!-- //Details -->' \
               '\r\n<!-- Footer -->\r\n<div class="footerw3layouts" id="footer">\r\n' \
               '<div class="container">\r\n' \
               '<div class="col-md-offset-8 col-sm-offset-8 col-md-2 col-sm-2 footer-grid footer-grid-1">\r\n' \
               '<ul>\r\n<li><a class="navbar-link" href="http://127.0.0.1:5000/home">首页</a></li>\r\n' \
               '<li><a class="navbar-link" href="http://127.0.0.1:5000/">退出</a></li>\r\n</ul>\r\n</div>\r\n' \
               '<div class="col-md-2 col-sm-2 footer-grid footer-grid-2">\r\n<ul>' \
               '\r\n<li>基于区块链的</li>\r\n<li>商品追踪溯源系统</li>\r\n</ul>\r\n</div>' \
               '\r\n<div class="clearfix"></div>\r\n<!-- Copyright -->' \
               '\r\n<div class="copyright">' \
               '\r\n<p>Copyright &copy; 2018.Team 332 All rights reserved.</p>\r\n</div>' \
               '\r\n<!-- //Copyright -->\r\n</div>\r\n</div>' \
               '\r\n<!-- Footer -->\r\n</body>\r\n<!-- //Body -->\r\n</html>'
        file.write(string)
        file.close()

    return render_template("productList.html",identity=newid)


# 游客模式

@app.route('/home2')
def home2():
    return render_template("home2.html")

@app.route('/blockList2')
@app.route('/blockList2/search', methods=['GET', 'POST'])
def blockList2():
    img1 = '../static/images/detail-2.jpg'
    if request.method == 'POST':
        book = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        goodID = request.form['goodID']

        #向服务器发送请求

        path = path = os.getcwd() + "\\app\\static\\chains\\chain" + goodID + ".json"
        # 检验该编号的区块链文件是否存在
        if not (os.path.isfile(path)):
            warning = "不存在该编号的商品区块链。"
            return render_template("blockList2.html", img1=img1,
                                   warning=warning, block="区块不存在")
        else:
            string = ''
            with open(path, 'r',encoding="utf-8") as load_f:
                for line in load_f:
                    if (line == '\n'):
                        continue
                    #data = json.loads(line)
                    data = json.loads(line.replace("'", '"'), encoding="utf-8")
                    if (data['nb'] == 0):
                        continue
                    # 二维码
                    if (data['nb'] == 1):
                        block_identity = '原产地'
                        if (book[1]==0):
                            string += '商品编号：' + data['information'][
                                'id'] + '\n' + '身份：' + block_identity + '\n' + '发生时间：' + \
                                      data['information'][
                                          'time'] + '\n' + '商品信息：' + '\n' + '地点：' + data['information'][
                                          'address'] + '\n' + '人物:' + \
                                      data['information']['character'] + '\n' + '联系方式：' + data['information'][
                                          'contact_info'] + '\n' + '描述：' + data['information'][
                                          'description'] + '\n' + '------------------------------' + '\n'

                        book[1] = 1

                    if (data['nb'] == 2):
                        block_identity = '加工厂'
                        if(book[2]==0):
                            string += '商品编号：' + data['information'][
                                'id'] + '\n' + '身份：' + block_identity + '\n' + '发生时间：' + \
                                      data['information'][
                                          'time'] + '\n' + '商品信息：' + '\n' + '地点：' + data['information'][
                                          'address'] + '\n' + '人物:' + \
                                      data['information']['character'] + '\n' + '联系方式：' + data['information'][
                                          'contact_info'] + '\n' + '描述：' + data['information'][
                                          'description'] + '\n' + '------------------------------' + '\n'
                        book[2] = 1

                    if (data['nb'] == 3):
                        block_identity = '运输'
                        if(book[3]==0):
                            string += '商品编号：' + data['information'][
                                'id'] + '\n' + '身份：' + block_identity + '\n' + '发生时间：' + \
                                      data['information'][
                                          'time'] + '\n' + '商品信息：' + '\n' + '地点：' + data['information'][
                                          'address'] + '\n' + '人物:' + \
                                      data['information']['character'] + '\n' + '联系方式：' + data['information'][
                                          'contact_info'] + '\n' + '描述：' + data['information'][
                                          'description'] + '\n' + '------------------------------' + '\n'
                        book[3] = 1

                    if (data['nb'] == 4):
                        block_identity = '入库'
                        if(book[4]==0):
                            string += '商品编号：' + data['information'][
                                'id'] + '\n' + '身份：' + block_identity + '\n' + '发生时间：' + \
                                      data['information'][
                                          'time'] + '\n' + '商品信息：' + '\n' + '地点：' + data['information'][
                                          'address'] + '\n' + '人物:' + \
                                      data['information']['character'] + '\n' + '联系方式：' + data['information'][
                                          'contact_info'] + '\n' + '描述：' + data['information'][
                                          'description'] + '\n' + '------------------------------' + '\n'
                        book[4] = 1

                    if (data['nb'] == 5):
                        block_identity = '销售'
                        if (book[4] == 0):
                            string += '商品编号：' + data['information'][
                                'id'] + '\n' + '身份：' + block_identity + '\n' + '发生时间：' + \
                                      data['information'][
                                          'time'] + '\n' + '商品信息：' + '\n' + '地点：' + data['information'][
                                          'address'] + '\n' + '人物:' + \
                                      data['information']['character'] + '\n' + '联系方式：' + data['information'][
                                          'contact_info'] + '\n' + '描述：' + data['information'][
                                          'description'] + '\n' + '------------------------------' + '\n'
                        book[5] = 1
            load_f.close()
            img = qrcode.make(string)
            img.save(os.getcwd() + "\\app\\static\\img\\Some" + data['information']['id'] + ".png")
            img1 = '../static/img/Some' + data['information']['id'] + '.png?' + ''.join(
                ['%.2X' % random.randint(0, 255) for i in range(8)])
            return render_template("blockList2.html", img1=img1,
                                   id="商品编号：" + goodID, block="区块")

    return render_template("blockList2.html", img1=img1, block="区块")

@app.route('/show2')
@app.route('/show2/search', methods=['GET', 'POST'])
def show2():
    time1 = '时间'
    place1 = '地点'
    person1 = '人物'
    tele1 = '联系方式'
    desc1 = '描述'
    time2 = '时间'
    place2 = '地点'
    person2 = '人物'
    tele2 = '联系方式'
    desc2 = '描述'
    time3 = '时间'
    place3 = '地点'
    person3 = '人物'
    tele3 = '联系方式'
    desc3 = '描述'
    time4 = '时间'
    place4 = '地点'
    person4 = '人物'
    tele4 = '联系方式'
    desc4 = '描述'
    time5 = '时间'
    place5 = '地点'
    person5 = '人物'
    tele5 = '联系方式'
    desc5 = '描述'
    goodID=''
    if request.method == 'POST':
        goodID = request.form['goodID']

        #向服务器发送请求



        path = os.getcwd()+"\\app\\static\\chains\\chain" + goodID + ".json"

        # 检验该编号的区块链文件是否存在
        if not (os.path.isfile(path)):
            warning = "不存在该编号的商品区块链。"
            return  render_template("show2.html", warning=warning,time1=time1, place1=place1, person1=person1, tele1=tele1, desc1=desc1,
                                   time2=time2, place2=place2, person2=person2, tele2=tele2, desc2=desc2,
                                   time3=time3, place3=place3, person3=person3, tele3=tele3, desc3=desc3,
                                   time4=time4, place4=place4, person4=person4, tele4=tele4, desc4=desc4,
                                   time5=time5, place5=place5, person5=person5, tele5=tele5, desc5=desc5)
        else:
            with open(path, 'r',encoding="utf-8") as f:
                for line in f:
                    if (line=='\n'):
                        continue
                    #dict=json.loads(line)
                    dict = json.loads(line.replace("'", '"'), encoding="utf-8")
                    new_dic = dict['information']
                    if (dict['nb']==0):
                        continue
                    if (dict['nb']==1):
                        time1=new_dic['time']
                        place1=new_dic['address']
                        person1=new_dic['character']
                        tele1=new_dic['contact_info']
                        desc1=new_dic['description']
                    if (dict['nb']==2):
                        time2=new_dic['time']
                        place2=new_dic['address']
                        person2=new_dic['character']
                        tele2=new_dic['contact_info']
                        desc2=new_dic['description']
                    if (dict['nb']==3):
                        time3=new_dic['time']
                        place3=new_dic['address']
                        person3=new_dic['character']
                        tele3=new_dic['contact_info']
                        desc3=new_dic['description']
                    if (dict['nb']==4):
                        time4=new_dic['time']
                        place4=new_dic['address']
                        person4=new_dic['character']
                        tele4=new_dic['contact_info']
                        desc4=new_dic['description']
                    if (dict['nb']==5):
                        time5=new_dic['time']
                        place5=new_dic['address']
                        person5=new_dic['character']
                        tele5=new_dic['contact_info']
                        desc5=new_dic['description']
            return render_template("show2.html", id="商品编号："+goodID,time1=time1, place1=place1, person1=person1, tele1=tele1, desc1=desc1,
                                   time2=time2, place2=place2, person2=person2, tele2=tele2, desc2=desc2,
                                   time3=time3, place3=place3, person3=person3, tele3=tele3, desc3=desc3,
                                   time4=time4, place4=place4, person4=person4, tele4=tele4, desc4=desc4,
                                   time5=time5, place5=place5, person5=person5, tele5=tele5, desc5=desc5)

    return render_template("show2.html",time1=time1, place1=place1, person1=person1, tele1=tele1, desc1=desc1,
                                   time2=time2, place2=place2, person2=person2, tele2=tele2, desc2=desc2,
                                   time3=time3, place3=place3, person3=person3, tele3=tele3, desc3=desc3,
                                   time4=time4, place4=place4, person4=person4, tele4=tele4, desc4=desc4,
                                   time5=time5, place5=place5, person5=person5, tele5=tele5, desc5=desc5)



