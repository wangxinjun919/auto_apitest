'''
python操作mysql需要使用pymysql这个模块
主机：120.78.128.25
port:3306
用户：future
密码：123456

'''
import pymysql
#第一步：连接到mysql数据库
con=pymysql.connect(host="120.78.128.25",user="future",password="123456",port=3306,charset="utf8")
#第二步：创建一个游标对象，看作一个鼠标
cur=con.cursor()
#第三步：执行sql语句
#1.准备sql语句
# sql="SELECT*FROM futureloan.member WHERE mobile_phone='13895023459'"
sql="SELECT*FROM futureloan.member LIMIT 5"
#2.执行sql语句
res=cur.execute(sql)
print(res)
#第四步：提取sql语句查找内容
#fetchall：返回的是一个查询集(元组的形式，查询到的每一条数据为这个元组中的一个元素)
# datas=cur.fetchall()
# for i in datas:
#     print(i)
# print(datas)
# fatchone：获取查询的数据中的第一条
data=cur.fetchone()
print(data)
#增删改
sql=""
cur.excute(sql)
#执行增删改查的sql语句之后，需要用过commit提交
con.commit()