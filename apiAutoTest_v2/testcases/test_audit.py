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
from common.handle_data import replace_data,TestData

@ddt
class AuditTestCase(unittest.TestCase):
    #获取表格数据
    excel6=ReadExcel(os.path.join(DATA_DIR,"apicases.xlsx"),"audit")
    #读取表格数据
    case6=excel6.read_data()
    http=HandleRequest()
    db=HandleDB()
    @classmethod
    def setUpClass(cls):
        #---执行所有用例之前登录，此过程也可以直接写在数据库中---
        url=conf.get("env","url")+"/member/login"
        data={
            "mobile_phone":conf.get("test_data","admin_mobile_phone"),
            "pwd":conf.get("test_data","admin_pwd")
        }
        header = eval(conf.get("env", "header"))
        response=cls.http.send(url=url,headers=header,method="post",json=data)
        json_data=response.json()
        #用户登录之后提取id和token
        member_id=jsonpath.jsonpath(json_data,"$..id")[0]
        setattr(TestData,"admin_member_id",str(member_id))
        token_type=jsonpath.jsonpath(json_data,"$..token_type")[0]
        token=jsonpath.jsonpath(json_data,"$..token")[0]
        token_data=token_type+" "+token
        setattr(TestData,"token_data",token_data)
    def setUp(self):
        #----执行每一条审核用例之前执行加标
        url = conf.get("env", "url") + "/loan/add"
        data = {
            "member_id":getattr(TestData,"admin_member_id"),
            "title":"cindy python自动化",
            "amount":2000.00,
            "loan_rate":12.0,
            "loan_term":6,
            "loan_date_type":1,
            "bidding_days":5
        }
        header = eval(conf.get("env", "header"))
        header["Authorization"]=getattr(TestData,"token_data")
        #发送加标请求
        response = self.http.send(url=url, headers=header, method="post", json=data)
        json_data = response.json()
        #提取加标返回的loan_id
        print(json_data)
        loan_id=jsonpath.jsonpath(json_data,"$..id")[0]
        setattr(TestData,"loan_id",str(loan_id))#setattr支持字符串
    @data(*case6)
    def test_audit(self,cases):
    #第一步：准备数据
        #获取url
        url=conf.get("env","url")+cases["url"]
        #获取data
        cases["data"]=replace_data(cases["data"])
        data=eval(cases["data"])
        #请求头
        header=eval(conf.get("env","header"))
        header["Authorization"] = getattr(TestData, "token_data")
        #请求方法
        method=cases["method"]
        #预期结果
        expected = eval(cases["expected"])
        row = cases["case_id"] + 1
    #第二步：发送审核请求
        response = self.http.send(url=url, headers=header, method=method, json=data)
        result = response.json()
        #如果审核通过的项目返回ok,说明该项目已审核
        if cases["title"]=="审核通过" and result["msg"]=="OK":
            pass_loan_id=getattr(TestData,"loan_id")
            #将该项目的id保存起来
            setattr(TestData,"pass_loan_id",pass_loan_id)
    #第三步：断言
        try:
            self.assertEqual(expected["code"], result["code"])
            self.assertEqual(expected["msg"], result["msg"])
            if cases["check_sql"]:
                sql=replace_data(cases["check_sql"])
                #获取这个标的状态
                status=self.db.get_one(sql)[0]
                self.assertEqual(expected["status"],status)


        except AssertionError as e:
            self.excel6.write_data(row=row, column=8, value='未通过')
            # 抛出异常，不抛出，认为用例通过
            my_log.info("用例：{}---执行未通过".format(cases["title"]))
            print("预期结果:{}".format(expected))
            print("实际结果:{}".format(result))
            raise e
            # 用例执行通过
        else:
            my_log.info("用例：{}---执行通过".format(cases["title"]))
            self.excel6.write_data(row=row, column=8, value='通过')

if __name__=='__main__':
    unittest.main()
