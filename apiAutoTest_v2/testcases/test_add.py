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
class AddTestCase(unittest.TestCase):
    excel5=ReadExcel(os.path.join(DATA_DIR,"apicases.xlsx"),"add")
    case5=excel5.read_data()
    http=HandleRequest()
    db = HandleDB()
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

        if cases["check_sql"]:
            sql = replace_data(cases["check_sql"])
            s_loan_num = self.db.count(sql)
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
            if cases["check_sql"]:
                sql=replace_data(cases["check_sql"])
                end_loan_num=self.db.count(sql)
                self.assertEqual(end_loan_num-s_loan_num,1)
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
    @classmethod
    def tearDownClass(cls):
        #关闭数据库得连接和游标对象
        cls.db.close()
if __name__=='__main__':
    unittest.main()
