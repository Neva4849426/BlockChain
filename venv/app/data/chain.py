import pymysql
import json

class chain(object):
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306  # 端口号
        self.user = 'root'  # 用户名
        self.password = "123456"  # 密码
        self.db = "mydatabase"  # 库

        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                passwd=self.password, db=self.db, charset='utf8')
        self.cursor = self.conn.cursor()

    def add(self, number,chaincode):
            chaincode = chaincode.replace("'", '"')
            #obj = json.loads(chaincode)
            obj = json.dumps(chaincode)
            sql = "INSERT INTO blockchain values(%s,%s)"%(number,obj)
            self.cursor.execute(sql)
            self.conn.commit()
            '''
            try :
                self.cursor.execute(sql)
                self.conn.commit()
            except:
                print("database add error")
                '''


    def read(self, number):
        #sql = "select * from blockchain"
        #self.cursor.execute(sql)
        #rr = self.cursor.fetchall()
        #print(len(rr))
        r = ''
        sql = "select id from blockchain"
        self.cursor.execute(sql)
        rs = self.cursor.fetchall()
        number = int(number)
        for i in range(0, len(rs)):
            if rs[i][0] == number:
                r = '1'
                break
            else:
                r = ''
        print("r 为：")
        print(r)
        if r == '1':
            sql = "select chain_code from blockchain where id = %s"
            param = [number]
            self.cursor.execute(sql, number)
            rs = self.cursor.fetchall()
            row = rs[0]
            return row[0]
        else:
            return r

    def readall(self):
        sql = "select chain_code from blockchain"
        self.cursor.execute(sql)
        rr = self.cursor.fetchall()
        length = len(rr)
        if length != 0:
            ch = [0] * length
            for i in range(0, length):
                ch[i] = rr[i][0]
        else:
            ch = ''
        return ch

    def modify(self, number, chaincode):

        chaincode = chaincode.replace("'", '"')
        obj = json.dumps(chaincode)
        sql = "update blockchain set chain_code =%s where id =%s"% (obj,number)
        self.cursor.execute(sql)
        self.conn.commit()
        '''
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print("database modify error")
        '''
"""newchain = chain()
ja_son = newchain.read('1003')
newchain.add('1004','{"number": 0, "timst": 1531838408.7642026, "information": [], "proof": 5, "previous_hash": 1111, "hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"}\8{"number": 1, "timst": 1532015278.9769127, "information": {"id": "1003", "tim": "2018-6-19 19:10:5", "address": "", "character": "魏婴", "contact_info": "180810311031", "description": "对成品竹笛进行流水线装配作业"}, "proof": 5, "previous_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945", "hash": "00ac38378c66db3fb3d5ec60566b04e5a466138b4cb28036099135788f620acf"}')
print(ja_son)"""
newchain =chain()
newchain .read('1')
