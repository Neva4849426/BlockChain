import pymysql

'''
调用方法
newhash=hash()
number = '123'
rr = newhash.read(number)
len = len(rr)
print(len)
row = rr[1]
print("第一个哈希值=%s,"%row[0])
'''
class hash(object):
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306  # 端口号
        self.user = 'root'  # 用户名
        self.password = "123456"  # 密码
        self.db = "mydatabase"  # 库

        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                passwd=self.password, db=self.db, charset='utf8')
        self.cursor = self.conn.cursor()

    def add(self,number,hash_value):
        sql =  "INSERT INTO hash_table values(%s,%s)"%(number,hash_value)
        self.cursor.execute(sql)
        return 0

    def read(self, number):
        sql = "select hash from hash_table where number = %s"
        param = [number]
        self.cursor.execute(sql, number)
        rs = self.cursor.fetchall()
        lenth = len(rs)
        h = [0] * lenth
        for i in range(0, lenth):
            h[i] = rs[i][0]
        return h





