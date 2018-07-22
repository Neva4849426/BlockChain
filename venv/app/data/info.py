import pymysql

class info(object):
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306  # 端口号
        self.user = 'root'  # 用户名
        self.password = "123456"  # 密码
        self.db = "mydatabase"  # 库
        # self.table = "nlp_weibo_data"  # 表

        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                passwd=self.password, db=self.db, charset='utf8')
        self.cursor = self.conn.cursor()

    def login_valid(self,username):
        self.username =username
        param = [username]
        sql = "select username from info"
        self.cursor.execute(sql)
        rs = self.cursor.fetchall()
        for i in range(0,len(rs)):
            if rs[i][0] == username:
                r = 1
                break
            else:
                r = 0
        sql= "SELECT * FROM info where username =%s "
        self.cursor.execute(sql,param)
        if r == 1:
            rr = self.cursor.fetchall()
        else:
            rr = None
        return rr

    def add(self,name,password,identi):
        sql = "INSERT INTO info (username,pwd,identity) values('%s','%s','%s')" % (name,password,identi)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print("error")

