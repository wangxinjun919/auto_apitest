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
if __name__=='__main__':
    unittest.main()
