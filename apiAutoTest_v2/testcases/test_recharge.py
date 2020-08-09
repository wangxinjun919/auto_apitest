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
if __name__=='__main__':
    unittest.main()