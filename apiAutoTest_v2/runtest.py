import unittest
from library.HTMLTestRunnerNew import HTMLTestRunner
import os
from common.contants import CASE_DIR,REPORT_DIR
#第一步：创建测试套件
suite=unittest.TestSuite()
#第二步：将测试用例加载到测试套件中
loader=unittest.TestLoader()
# suite.addTest(loader.discover(r"D:\python install\homework\homework_20191126\testcases"))
suite.addTest(loader.discover(CASE_DIR))
#第三步：创建一个测试用例运行程序
# report_path=r"D:\python install\homework\homework_20191126\reports\report.html"
report_path=os.path.join(REPORT_DIR,'report.html')
with open(report_path,"wb") as f:
    runner=HTMLTestRunner(stream=f,tester="cindy",description="前程贷测试报告测试",title="前程贷测试报告")
    runner.run(suite)


