import unittest
import os
from common.contants import DATA_DIR
from common.readexcel import ReadExcel
from library.ddt import ddt,data
from common.handle_request import HandleRequest
from common.mylogger import my_log
from common.myconfig import conf
from common.handle_db import HandleDB
import jsonpath
import decimal
from common.handle_data import replace_data,TestData
@ddt
class TestInvest(unittest.TestCase):
    excel7=ReadExcel(os.path.join(DATA_DIR,"apicases.xlsx"),"invest")
    case7=excel7.read_data()
    http=HandleRequest()
    db=HandleDB()
    @data(*case7)
    def test_invest(self,cases):
        #第一步：准备用例数据
        #获取url
        url=conf.get("env","url")+cases["url"]
        #获取data
        cases["data"]=replace_data(cases["data"])
        data=eval(cases["data"])
        #获取method
        method=cases["method"]
        #请求头
        header=eval(conf.get("env","header"))
        if cases["interface"]!="login":
           #添加请求头里的token
           header["Authorization"] = getattr(TestData,"token_data")
        #预期结果
        expected=eval(cases["expected"])
        #用例所在行
        row=cases["case_id"]+1
        #获取投资之前的钱
        if cases["check_sql"]:
            sql = replace_data(cases["check_sql"])
            start_invest=self.db.get_one(sql)[0]

        #第二步：发送请求
        res = self.http.send(url=url, method=method, headers=header, json=data)
        result = res.json()
        print(result)
        if cases["interface"]=="login":
            #获取用户id和token
            id = jsonpath.jsonpath(result, "$..id")[0]
            setattr(TestData, "member_id", str(id))
            token_type = jsonpath.jsonpath(result, "$..token_type")[0]
            token = jsonpath.jsonpath(result, "$..token")[0]
            token_data = token_type + " " + token
            setattr(TestData, "token_data", token_data)

        elif cases["interface"]=="add":
            #提取项目id
            loan_id = jsonpath.jsonpath(result, "$..id")[0]
            setattr(TestData, "loan_id", str(loan_id))
        #第三步：断言
        try:
            self.assertEqual(expected["code"], result["code"])
            self.assertEqual(expected["msg"], result["msg"])
            if cases["check_sql"]:
                sql=replace_data(cases["check_sql"])
                #获取这个标的状态
                end_invest=self.db.get_one(sql)[0]
                # 把浮点数转换成decimal类型，记得转换之前先转换成字符串（不然浮点数会有精度问题）
                invest_money = decimal.Decimal(str(data["amount"]))
                my_log.info("投资之前的金额为：{}\n,投资之后的金额为:{}".format(start_invest, end_invest))
                # 进行断言（开始的金额减去结束金额=投资的前）
                self.assertEqual(invest_money,start_invest-end_invest)

        except AssertionError as e:
            self.excel7.write_data(row=row, column=8, value='未通过')
            # 抛出异常，不抛出，认为用例通过
            my_log.info("用例：{}---执行未通过".format(cases["title"]))
            print("预期结果:{}".format(expected))
            print("实际结果:{}".format(result))
            raise e
            # 用例执行通过
        else:
            my_log.info("用例：{}---执行通过".format(cases["title"]))
            self.excel7.write_data(row=row, column=8, value='通过')
    @classmethod
    def tearDownClass(cls):
        #关闭数据库得连接和游标对象
        cls.db.close()
if __name__=='__main__':
    unittest.main()

