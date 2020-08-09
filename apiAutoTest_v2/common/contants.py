'''
该模块用来处理整个项目目录的路径
'''
import os
#获取当前文件的绝对路径
#dir=os.path.abspath(__file__)

#项目目录的路径   如果运行的时候项目目录路径出错，使用上面abspath的方式来获取当前文件的绝对路径
BASEDIR=os.path.dirname(os.path.dirname(__file__))
print(BASEDIR)
#配置文件目录的路径
CONF_DIR=os.path.join(BASEDIR,"conf")
#用例数据的目录
DATA_DIR=os.path.join(BASEDIR,"data")
#日志文件的目录
LOG_DIR=os.path.join(BASEDIR,"log")
#测试报告文件的目录
REPORT_DIR=os.path.join(BASEDIR,"reports")
#测试案例文件的目录
CASE_DIR=os.path.join(BASEDIR,"testcases")