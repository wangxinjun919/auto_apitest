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
if __name__=='__main__':
    unittest.main()