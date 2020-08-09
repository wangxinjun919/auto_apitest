import unittest
import os
from common.contants import DATA_DIR
from common.readexcel import ReadExcel
from library.ddt import ddt,data
from common.handle_request import HandleRequest
from common.mylogger import my_log
from common.myconfig import conf
from common.module import random_phone
from common.handle_db import HandleDB
import jsonpath
import decimal
from common.handle_data import replace_data,TestData
#定义登录的测试用例
@ddt
class RegisterTestCase(unittest.TestCase):
    excel1=ReadExcel(os.path.join(DATA_DIR,"apicases.xlsx"),"register")
    case1 = excel1.read_data()
    http=HandleRequest()
    db=HandleDB()
    @data(*case1)
    def test_register(self, cases):  # 将case1的数据传到cases
#----------第一步:准备用例数据-------------------
        #拼接完整的接口地址
        url=conf.get("env","url")+cases['url']
        #获取请求方法
        case_method=cases["method"]
        #判断是否有手机号进行替换
        if "#phone#" in cases["data"]:
            phone=random_phone()
            cases["data"]=cases["data"].replace("#phone#",phone) #为什么不赋值给其他重新定义的参数,要赋值给cases["data"]，因为查找出来phone可能是数字,获取请求参数就找不到了
        #获取请求参数
        data=eval(cases["data"])
        #获取请求头
        header=eval(conf.get("env","header"))
        #预期结果
        expected=eval(cases["expected"])
        row=cases["case_id"]+1
        #----第二步：发送请求接口
        response=self.http.send(url=url,method=case_method,json=data,headers=header)
        result=response.json()
        try:
            self.assertEqual(expected["code"],result["code"])
            self.assertEqual(expected["msg"], result["msg"])
            if result["msg"]=="ok":
                #数据库查询是否有数据
                sql="SELECT*FEOM futureloan.member WHERE mobile_phone={}".format(phone)
                #获取数据库中有没有改用户的信息
                count=self.db.count(sql)
                #数据库中返回的数据做断言，判断是否有一个数据
                self.assertEqual(1,count)
        #用例执行未通过
        except AssertionError as e:
            self.excel1.write_data(row=row,column=8,value='未通过')
            #抛出异常，不抛出，认为用例通过
            my_log.info("用例：{}---执行未通过".format(cases["title"]))
            print("预期结果:{}".format(expected))
            print("实际结果:{}".format(result))
            print(data)
            raise e
        #用例执行通过
        else:
            my_log.info("用例：{}---执行通过".format(cases["title"]))
            self.excel1.write_data(row=row,column=8, value='通过')
    @classmethod
    def tearDownClass(cls):
        #关闭数据库得连接和游标对象
        cls.db.close()
@ddt
class LoginTestCase(unittest.TestCase):
    excel2=ReadExcel(os.path.join(DATA_DIR,"apicases.xlsx"),"login")
    case2 = excel2.read_data()
    http = HandleRequest()
    @data(*case2)
    def test_login(self,cases):  # 将case2的数据传到cases
        # ----------第一步:准备用例数据-------------------
        # 拼接完整的接口地址
        url = conf.get("env", "url") + cases['url']
        # 获取请求方法
        case_method = cases["method"]
        # 获取请求参数
        data = eval(cases["data"])
        # 获取请求头
        header = eval(conf.get("env", "header"))
        # 预期结果
        expected = eval(cases["expected"])
        row = cases["case_id"] + 1
        # ----第二步：发送请求接口-------------------
        response = self.http.send(url=url, method=case_method, json=data, headers=header)
        result = response.json()
        try:
            self.assertEqual(expected["code"],result["code"])
            self.assertEqual(expected["msg"], result["msg"])
            #用例执行未通过
        except AssertionError as e:
            self.excel2.write_data(row=row,column=8,value='未通过')
            #抛出异常，不抛出，认为用例通过
            my_log.info("用例：{}---执行未通过".format(cases["title"]))
            print("预期结果:{}".format(expected))
            print("实际结果:{}".format(result))
            raise e
        #用例执行通过
        else:
            my_log.info("用例：{}---执行通过".format(cases["title"]))
            self.excel2.write_data(row=row, column=8, value='通过')
@ddt
class RechargeTestCase(unittest.TestCase):
    #获取数据
    excel3=ReadExcel(os.path.join(DATA_DIR,"apicases.xlsx"),"recharge")
    #读取数据
    case3=excel3.read_data()
    #获取发送请求
    http=HandleRequest()
    db = HandleDB()
    @classmethod
    #所有用例执行之前执行此步骤
    def setUpClass(cls):
        url=conf.get("env","url")+"/member/login"
        data={
            "mobile_phone":conf.get("test_data","mobile_phone"),
            "pwd":conf.get("test_data","pwd")
        }
        header=eval(conf.get("env","header"))
        response=cls.http.send(url=url,method="post",json=data,headers=header)
        json_data=response.json()
    # -------登录之后，从响应数据中提取用户id和token--------
        #1.用户id
        member_id=jsonpath.jsonpath(json_data,"$..id")[0]
        setattr(TestData,"member_id",str(member_id))
        #2.提取token
        token_type=jsonpath.jsonpath(json_data,"$..token_type")[0]
        token=jsonpath.jsonpath(json_data,"$..token")[0]
        token_data=token_type+" "+token
        setattr(TestData, "token_data", token_data)

    @data(*case3)
    def test_recharge(self, cases):  # 将case2的数据传到cases
        #------第一步准备测试数据-----
        #获取请求地址
        url=conf.get("env","url")+cases['url']
        #获取请求方法
        method=cases["method"]
        # 判断是否有member_id，替换memberid
        cases["data"]=replace_data(cases["data"])
        data=eval(cases["data"])
        #获取请求头
        header=eval(conf.get("env", "header"))
        header["Authorization"]=getattr(TestData,"token_data")
        # 预期结果
        expected = eval(cases["expected"])
        row = cases["case_id"] + 1

        # ----第二步：发送请求接口-------------------
        if cases["check_sql"]:
            sql = cases["check_sql"].format(conf.get("test_data", "mobile_phone"))
            # 获取充值之前的余额
            start_money = self.db.get_one(sql)[0]
        response=self.http.send(url=url,method=method,json=data,headers=header)
        result=response.json()

#---------------第三步：断言----------------
        try:
            self.assertEqual(expected["code"], result["code"])
            self.assertEqual(expected["msg"],result["msg"])
            if cases["check_sql"]:
                sql=cases["check_sql"].format(conf.get("test_data","mobile_phone"))
                #获取充值之后的余额
                end_money=self.db.get_one(sql)[0]
                #把浮点数转换成decimal类型，记得转换之前先转换成字符串（不然浮点数会有精度问题）
                recharge_money=decimal.Decimal(str(data["amount"]))
                my_log.info("充值之前的金额为：{}\n,充值之后的金额为:{}".format(start_money,end_money))
                #进行断言（开始的金额减去结束的金额）
                self.assertEqual(recharge_money,end_money-start_money)
            #用例执行未通过

        except AssertionError as e:
            self.excel3.write_data(row=row, column=8, value='未通过')
            # 抛出异常，不抛出，认为用例通过
            my_log.info("用例：{}---执行未通过".format(cases["title"]))
            print("预期结果:{}".format(expected))
            print("实际结果:{}".format(result))
            raise e
            # 用例执行通过
        else:
            my_log.info("用例：{}---执行通过".format(cases["title"]))
            self.excel3.write_data(row=row, column=8, value='通过')






'''
方法一：
setupclasee中提取的用户id和token,如何在用例方法中的使用？
1.设为全局变量
2.保存为类属性
3.写入到配置文件
4.保存到临时变量的类中（后面讲）
方法二：
在excel中，第一条用例设计为登录
#然后在用例方法中，请求之后去判断是否是登录的用例：如果是的就去提取数据，对数据进行保存
1.设为全局变量
2.保存为类属性
3.写入到配置文件
4.保存在临时变量的类中

'''

@ddt
class WithdrawTestCase(unittest.TestCase):
    #获取数据
    excel4=ReadExcel(os.path.join(DATA_DIR,"apicases.xlsx"),"withdraw")
    #读取数据
    case4=excel4.read_data()
    #获取发送请求
    http=HandleRequest()
    db = HandleDB()
    @classmethod
    #所有用例执行之前执行此步骤
    def setUpClass(cls):
        url=conf.get("env","url")+"/member/login"
        data={
            "mobile_phone":conf.get("test_data","mobile_phone"),
            "pwd":conf.get("test_data","pwd")
        }
        header=eval(conf.get("env","header"))
        response=cls.http.send(url=url,method="post",json=data,headers=header)
        json_data=response.json()

    # -------登录之后，从响应数据中提取用户id和token--------
        #1.用户id
        member_id = jsonpath.jsonpath(json_data, "$..id")[0]
        setattr(TestData, "member_id", str(member_id))
        #2.提取token
        token_type = jsonpath.jsonpath(json_data, "$..token_type")[0]
        token = jsonpath.jsonpath(json_data, "$..token")[0]
        token_data = token_type + " " + token
        setattr(TestData, "token_data", token_data)
    @data(*case4)
    def test_withdraw(self, cases):  # 将case2的数据传到cases
        #------第一步准备测试数据-----
        #获取请求地址
        url=conf.get("env","url")+cases['url']
        #获取请求方法
        method=cases["method"]
        # 判断是否有member_id，替换memberid
        cases["data"] = replace_data(cases["data"])
        data = eval(cases["data"])
        #获取请求头
        header=eval(conf.get("env", "header"))
        header["Authorization"]=getattr(TestData,"token_data")
        # 预期结果
        expected = eval(cases["expected"])
        row = cases["case_id"] + 1

        # ----第二步：发送请求接口-------------------
        if cases["check_sql"]:
            sql = cases["check_sql"].format(conf.get("test_data", "mobile_phone"))
            # 获取取现之前的余额
            start_money = self.db.get_one(sql)[0]
        response=self.http.send(url=url,method=method,json=data,headers=header)
        result=response.json()
        response=self.http.send(url=url,method=method,json=data,headers=header)
        result=response.json()
#---------------第三步：断言----------------
        try:
            self.assertEqual(expected["code"],result["code"])
            self.assertEqual(expected["msg"],result["msg"])
            if cases["check_sql"]:
                sql=cases["check_sql"].format(conf.get("test_data","mobile_phone"))
                #获取取现之后的余额
                end_money=self.db.get_one(sql)[0]
                #把数据转换成decimal类型
                withdraw_money=decimal.Decimal(str(data["amount"]))
                my_log.info("取现之前的金额为：{}\n,取现之后的金额为:{}".format(start_money,end_money))
                #进行断言（开始的金额减去结束的金额）
                self.assertEqual(withdraw_money,start_money-end_money)
            #用例执行未通过
        except AssertionError as e:
            self.excel4.write_data(row=row, column=8, value='未通过')
            # 抛出异常，不抛出，认为用例通过
            my_log.info("用例：{}---执行未通过".format(cases["title"]))
            print("预期结果:{}".format(expected))
            print("实际结果:{}".format(result))
            raise e
            # 用例执行通过
        else:
            my_log.info("用例：{}---执行通过".format(cases["title"]))
            self.excel4.write_data(row=row, column=8, value='通过')
            
@ddt
class AddTestCase(unittest.TestCase):
    excel5=ReadExcel(os.path.join(DATA_DIR,"apicases.xlsx"),"add")
    case5=excel5.read_data()
    http=HandleRequest()
    @data(*case5)
    def test_add(self,cases):
    #第一步：准备用例数据
        #获取URL
        url=conf.get("env","url")+cases["url"]
        #获取数据
        cases["data"]=replace_data(cases["data"])
        data=eval(cases["data"])
        #请求头
        header=eval(conf.get("env","header"))
        if cases["interface"]!="login":
            header["Authorization"]=getattr(TestData,"token_data")
        #预期结果
        expected=eval(cases["expected"])
        #请求方法
        method=cases["method"]
        #用例所在的行
        row=cases["case_id"]+1
        #发送请求
        res=self.http.send(url=url,headers=header,json=data,method=method)
        result=res.json()
        if cases["interface"]=="login":
            #如果是登陆的用例，提取对应的token和用户id
            token_type=jsonpath.jsonpath(result,"$..token_type")[0]
            token=jsonpath.jsonpath(result,"$..token")[0]
            token_data=token_type+" "+token
            setattr(TestData,"token_data",token_data)
            id=jsonpath.jsonpath(result,"$..id")[0]
            setattr(TestData,"admin_member_id",str(id))
        #第三步：断言
        try:
            self.assertEqual(expected["code"],result["code"])
            self.assertEqual(expected["msg"], result["msg"])
            #用例执行未通过
        except AssertionError as e:
            self.excel5.write_data(row=row,column=8,value='未通过')
            #抛出异常，不抛出，认为用例通过
            my_log.info("用例：{}---执行未通过".format(cases["title"]))
            print("预期结果:{}".format(expected))
            print("实际结果:{}".format(result))
            raise e
        #用例执行通过
        else:
            my_log.info("用例：{}---执行通过".format(cases["title"]))
            self.excel5.write_data(row=row, column=8, value='通过')
if __name__=='__main__':
    unittest.main()

