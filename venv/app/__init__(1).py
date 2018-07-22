from flask import Flask, render_template,send_from_directory,redirect,url_for,flash,request,json
from flask_bootstrap import Bootstrap
from app.Client import Client
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
        '''
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
            '''

        if username == '' and password == '':
            return render_template("home.html")
        else:
            return render_template("login_fail.html")
    # return render_template("login.html",title_name = '欢迎，请登录！')


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
        goodID = request.form['goodID']
        path = os.getcwd() + "\\app\\static\\products\\" + goodID + ".json"
    if request.method == 'GET':
        testid = request.args.get('id')
        if (testid == None):
            return render_template("edit.html", identity=newid)
        path = os.getcwd() + "\\app\\static\\products\\" + testid + ".json"

    # 检验该编号的文件是否存在
    if not (os.path.isfile(path)):
        warning = "不存在该编号的商品，您可以输入并保存新的信息。"
        return render_template("edit.html", warning=warning, identity=newid)
    with open(path, 'r',encoding = "utf-8") as f:
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

    return render_template("edit.html", identity=newid, id=id, time=time,
                           address=address, character=character,
                           contact_info=contact_info,
                           description=description)


@app.route('/edit/save', methods=['GET', 'POST'])
def save():
    global identity
    newid = identity
    if request.method == 'POST':
        data = request.get_json()
        path = os.getcwd() + "\\app\\static\\products\\" + data['id'] + ".json"
        if (data['id'] == ''):
            warning = "请输入商品编号！"
            return render_template("edit.html", identity=newid, warning=warning)
        if not (os.path.isfile(path)):
            f = open(path, 'w',encoding = "utf-8")
            f.close()
            data['add_chain'] = "0"
        else:
            with open(path, 'r',encoding = "utf-8") as f:
                line = f.readline()
                temp = json.loads(line)
                data['add_chain'] = temp['add_chain']
            f.close()

        with open(path, 'w',encoding = "utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False))
        f.close()
        success = "保存成功！"

        return render_template("edit.html", identity=newid, success=success)
    else:
        return render_template("edit.html", identity=newid)


@app.route('/edit/delete', methods=['GET', 'POST'])
def delete():
    global identity
    newid = identity
    if request.method == 'POST':
        data = request.get_json()

        if (data['id'] != ""):
            path = os.getcwd() + "\\app\\static\\products\\" + data['id'] + ".json"
            if not (os.path.isfile(path)):
                return render_template("edit.html", identity=newid, warning="该编号的商品信息文件不存在！")
            else:
                os.remove(path)
                return render_template("edit.html", identity=newid, success="删除成功！")
        else:
            return render_template("edit.html", identity=newid, warning="商品编号栏不能为空！")

    return render_template("edit.html", identity=newid)


@app.route('/show')
@app.route('/show/search', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        goodID = request.form['goodID']
        path = os.getcwd() + "\\app\\static\\chains\\chain" + goodID + ".json"

        # 检验该编号的区块链文件是否存在
        if not (os.path.isfile(path)):
            warning = "不存在该编号的商品区块链。"
            return render_template("show.html", warning=warning, id=goodID)
        else:
            time1 = ''
            place1 = ''
            person1 = ''
            tele1 = ''
            desc1 = ''
            time2 = ''
            place2 = ''
            person2 = ''
            tele2 = ''
            desc2 = ''
            time3 = ''
            place3 = ''
            person3 = ''
            tele3 = ''
            desc3 = ''
            time4 = ''
            place4 = ''
            person4 = ''
            tele4 = ''
            desc4 = ''
            time5 = ''
            place5 = ''
            person5 = ''
            tele5 = ''
            desc5 = ''
            with open(path, 'r',encoding = "utf-8") as f:   #,'utf-8'
                for line in f.readlines():
                    if (line == '\n'):
                        continue
                    print(line)
                    dict = json.loads(line.replace("'", '"'))
                    new_dic = dict['information']
                    new_dic = client.utf82uni(new_dic)
                    if (dict['number'] == 0):
                        continue
                    if (dict['number'] == 1):
                        time1 = new_dic['time']
                        place1 = new_dic['address']
                        person1 = new_dic['character']
                        tele1 = new_dic['contact_info']
                        desc1 = new_dic['description']
                    if (dict['number'] == 2):
                        time2 = new_dic['time']
                        place2 = new_dic['address']
                        person2 = new_dic['character']
                        tele2 = new_dic['contact_info']
                        desc2 = new_dic['description']
                    if (dict['number'] == 3):
                        time3 = new_dic['time']
                        place3 = new_dic['address']
                        person3 = new_dic['character']
                        tele3 = new_dic['contact_info']
                        desc3 = new_dic['description']
                    if (dict['number'] == 4):
                        time4 = new_dic['time']
                        place4 = new_dic['address']
                        person4 = new_dic['character']
                        tele4 = new_dic['contact_info']
                        desc4 = new_dic['description']
                    if (dict['number'] == 5):
                        time5 = new_dic['time']
                        place5 = new_dic['address']
                        person5 = new_dic['character']
                        tele5 = new_dic['contact_info']
                        desc5 = new_dic['description']
            return render_template("show.html", id=goodID, time1=time1, place1=place1, person1=person1, tele1=tele1,
                                   desc1=desc1,
                                   time2=time2, place2=place2, person2=person2, tele2=tele2, desc2=desc2,
                                   time3=time3, place3=place3, person3=person3, tele3=tele3, desc3=desc3,
                                   time4=time4, place4=place4, person4=person4, tele4=tele4, desc4=desc4,
                                   time5=time5, place5=place5, person5=person5, tele5=tele5, desc5=desc5)

    return render_template("show.html")


@app.route('/blockList')
@app.route('/blockList/search', methods=['GET', 'POST'])
def blockList():
    if request.method == 'POST':
        goodID = request.form['goodID']

        path = os.getcwd() + "\\app\\static\\chains\\chain" + goodID + ".json"
        # 检验该编号的区块链文件是否存在
        if not (os.path.isfile(path)):
            warning = "不存在该编号的商品区块链。"
            return render_template("blockList.html", id="商品编号：" + goodID, warning=warning, block="区块不存在")
        else:
            string = ''
            with open(path, 'r',encoding = "utf-8") as load_f:
                for line in load_f:
                    if (line == '\n'):
                        continue
                    data = json.loads(line.replace("'", '"'))
                    data['information'] = client.utf82uni(data['information'])
                    if (data['number'] == 0):
                        continue
                    # 二维码
                    if (data['number'] == 1):
                        block_identity = '原产地'
                    if (data['number'] == 2):
                        block_identity = '加工厂'
                    if (data['number'] == 3):
                        block_identity = '运输'
                    if (data['number'] == 4):
                        block_identity = '入库'
                    if (data['number'] == 5):
                        block_identity = '销售'

                    print(type(data['number']))
                    print(data)
                    string += '商品编号：' + data['information']['id'] + '\n' + '身份：' + block_identity + '\n' + '发生时间：' + \
                              data['information'][
                                  'time'] + '\n' + '商品信息：' + '\n' + '地点：' + data['information'][
                                  'address'] + '\n' + '人物:' + \
                              data['information']['character'] + '\n' + '联系方式：' + data['information'][
                                  'contact_info'] + '\n' + '描述：' + data['information'][
                                  'description'] + '\n' + '------------------------------' + '\n'
            load_f.close()
            img = qrcode.make(string)
            img.save(os.getcwd() + "\\app\\static\\img\\Some" + data['information']['id'] + ".png")
            img1 = '../static/img/Some' + data['information']['id'] + '.png?' + ''.join(
                ['%.2X' % random.randint(0, 255) for i in range(8)])
            return render_template("blockList.html", id="商品编号：" + goodID, img1=img1, block="区块")

    return render_template("blockList.html")





@app.route('/blockEdit')
@app.route('/blockEdit/addtochain', methods=['GET', 'POST'])
def blockEdit():
    global identity
    newid = identity
    if request.method == 'POST':
        data = request.get_json()
        print(data)

        return render_template("blockEdit.html",identity = newid,
                               button1="修改区块",button2="已加入区块链",btntype="btn btn-primary disabled")

    else:
        return render_template("blockEdit.html",identity = newid,
                               button1="修改区块",button2="加入区块链",btntype="btn btn-primary"
                               ,btntype2="btn btn-primary")


    return render_template("blockEdit.html",identity = newid,
                           button1="修改区块",button2="加入区块链",btntype="btn btn-primary"
                           ,btntype2="btn btn-primary")


@app.route('/blockEdit/search', methods=['GET', 'POST'])
def blockSearch():
    global identity
    newid = identity
    if request.method == 'POST':
        goodID = request.form['goodID']
        path = os.getcwd()+"\\app\\static\\products\\" + goodID + ".json"
        #path = "D:/configFiles/" + goodID + ".json"
        # 检验该编号的文件是否存在
        if not (os.path.isfile(path)):
            warning = "不存在该编号的商品！"
            return render_template("blockEdit.html",identity = newid, warning=warning,id=goodID,
                           button1="修改区块",button2="加入区块链",btntype="btn btn-primary",
                            btntype2="btn btn-primary")
        with open(path, 'r',encoding = "utf-8") as f:
            line = f.readline()
            data = json.loads(line)
        f.close()
        data = client.utf82uni(data)
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
        path = os.getcwd() + "\\app\\static\\products\\" + goodID + ".json"


        # 检验该编号的文件是否存在
        if not (os.path.isfile(path)):
            warning = "不存在该编号的商品！"
            return render_template("blockEdit.html", identity=newid, warning=warning, id=goodID,
                           button1="修改区块",button2="加入区块链",btntype="btn btn-primary",btntype2="btn btn-primary")
        with open(path, 'r',encoding = "utf-8") as f:
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

        data = client.utf82uni(data)
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

        with open(path, 'w',encoding = "utf-8") as f:
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
        path = os.getcwd() + "\\app\\static\\products\\" + goodID + ".json"
        #path = "D:/configFiles/" + goodID + ".json"

        # 检验该编号的文件是否存在
        if not (os.path.isfile(path)):
            warning = "不存在该编号的商品！"
            return render_template("blockEdit.html", identity=newid, warning=warning, id=goodID,
                           button1="修改区块",button2="加入区块链",btntype="btn btn-primary",btntype2="btn btn-primary")
        with open(path, 'r',encoding = "utf-8") as f:
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


        data = client.utf82uni(data)
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
        path = os.getcwd() + "\\app\\static\\products\\" + goodID + ".json"

        with open(path, 'r',encoding = "utf-8") as f:
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

        with open(path, 'w',encoding = "utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False))
        f.close()

        return jsonify(data)

@app.route('/productList')
def productList():
    global identity,client
    newid=identity
    path2 = os.getcwd() + '\\app\\templates\\productList.html'
    with open(path2, 'w') as file:
        line="{% extends 'bootstrap/base.html' %}  #声明继承\r\n{% block title %}{{ title_name }}{% endblock %}\r\n{% block head %}\r\n{{ super() }}"
        line+='<head><script  src="https://cdn.bootcss.com/jquery/1.10.2/jquery.min.js"></script></head>\r\n{% endblock %}\r\n{% block styles %}\r\n{{ super() }}'
        line+='<link rel="stylesheet"\r\nhref="https://maxcdn.bootstrapcdn.com/bootswatch/3.3.7/darkly/bootstrap.min.css">\r\n{% endblock %}\r\n{% block navbar %}' \
              '\r\n<nav class="navbar navbar-expand-lg navbar-dark bg-primary">\r\n<a class="navbar-brand">商品追溯系统</a>\r\n' \
              '<div class="collapse navbar-collapse" id="navbarColor01">\r\n<ul class="nav navbar-nav navbar-left">\r\n' \
              '<li class="nav-item active">\r\n<a class="nav-link" href="http://127.0.0.1:5000/blockList">区块列表 <span class="sr-only">(current)</span></a>\r\n' \
              '</li>\r\n<li class="nav-item">\r\n<a class="nav-link" href="http://127.0.0.1:5000/show">区块信息</a>\r\n</li>\r\n' \
              '<li class="nav-item">\r\n<a class="nav-link" href="http://127.0.0.1:5000/productList">商品信息</a>\r\n</li>\r\n' \
              '<li class="nav-item">\r\n<a class="nav-link" href="http://127.0.0.1:5000/edit">商品编辑</a>\r\n</li>\r\n' \
              '<li class="nav-item">\r\n<a class="nav-link" href="http://127.0.0.1:5000/blockEdit">区块编辑</a>\r\n</li>\r\n</ul>\r\n' \
              '<ul class="nav navbar-nav navbar-right">\r\n<li class="nav-item active">\r\n' \
              '<a class="nav-link" a href="http://127.0.0.1:5000/">退出 <span class="sr-only">(current)</span></a>\r\n</li>\r\n</ul>\r\n</div>\r\n</nav>\r\n' \
              '{% endblock %}\r\n{% block content %}\r\n<div class="container">\r\n' \
              '<div class = "row">\r\n<br><br>\r\n</div>\r\n<div class="jumbotron">\r\n<div class = "row">\r\n<br>'
        file.write(line)
    file.close()
    path=os.getcwd()+'\\app\\static\\products\\'
    files = os.listdir(path)
    for file in files:
        new_path = path + file
        with open(new_path, 'r') as f:
            line = f.readline()
            data = json.loads(line)
        f.close()
        with open(path2, 'a') as file:
            string='<div class = "col-md-4"><table class="table table-bordered">\r\n<thead>\r\n<tr class = "info">\r\n<th scope="row">商品编号：</th>\r\n<th class = "text-center" id="productID">'
            string+=data['id']+'</th>\r\n</tr>\r\n</thead>\r\n<tbody>\r\n<tr>\r\n<th scope="row">时间：</th>\r\n<td class = "text-center" type="text"  id="time" name="time">'
            string+=data['time']+'</td>\r\n</tr>\r\n<tr>\r\n<th scope="row">身份：</th>\r\n<td class = "text-center" type="text"  id="identity" name="identity">'
            string+='{{identity}}'+'</td>\r\n</tr>\r\n<tr>\r\n<th scope="row">地点：</th>\r\n<td class = "text-center" type="text"  id="place" name="place">'
            string+=data['address']+'</td>\r\n</tr>\r\n<tr>\r\n<th scope="row">人物：</th>\r\n<td class = "text-center"  type="text"  id="person" name="person">'
            string+=data['character']+'</td>\r\n</tr>\r\n<tr>\r\n<th scope="row">联系方式：</th>\r\n<td class = "text-center" type="text"  id="tele" name="tele">'
            string+=data['contact_info']+'</td>\r\n</tr>\r\n<tr>\r\n<th scope="row">描述：</th>\r\n<td class = "text-center" type="text"  id="desc" name="desc">'
            string+=data['description']+'</td>\r\n</tr>\r\n</tbody>\r\n</table>'
            if (data['add_chain']=='0'):
                add_chain='加入区块链'
                state='"'
            else:
                add_chain='已加入区块链'
                state = ' disabled"'
            string += '\r\n<button class="btn btn-primary'+state+' type="button" style="margin-left:40px" id="button1" onclick="javascript:window.location.href='
            string += "'http://127.0.0.1:5000/productList/waitToAdd?id=" + data['id'] + "'" + '">'+add_chain+'</button>\r\n'
            string+='\r\n<button class="btn btn-primary" type="button" style="margin-left:40px" id="button1" onclick="javascript:window.location.href='
            string+="'http://127.0.0.1:5000/edit/search?id="+ data['id']+"'"+'">编辑</button>\r\n'
            string+= '</div>\r\n'
            file.write(string)
            file.close()
    with open(path2, 'a') as file:
        string='</div>\r\n</div>\r\n</div>\r\n\r\n{% endblock content %}'
        file.write(string)
        file.close()

    return render_template("productList.html",identity=newid)


# 游客模式

@app.route('/home2')
def home2():
    global client
    return render_template("home2.html")

@app.route('/blockList2')
def blockList2():
    global client
    return render_template("blockList2.html")

@app.route('/show2')
def show2():
    global client
    return render_template("show2.html")

