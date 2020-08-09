import pymysql
from common.myconfig import conf
class HandleDB:
    def __init__(self):
        #连接数据库
        self.con=pymysql.connect(host=conf.get("mysql","host"),user=conf.get("mysql","user"),password=conf.get("mysql","password"),port=conf.getint("mysql","port"),charset="utf8")
        #创建游标
        self.cur=self.con.cursor()
    def get_one(self,sql):
      #获取查询到的第一条数据
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchone()
    def get_all(self,sql):
        # 获取查询到的所有数据
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchall()
    def count(self,sql):
    # 获取查询到的所有数据的数量
        self.con.commit()
        res=self.cur.execute(sql)
        return res
    def close(self):
        #关闭游标对象
        self.cur.close()
        #断开连接
        self.con.close()