import logging
from common.myconfig import conf
import os
from common.contants import LOG_DIR
#读取配置文件中的数据
level=conf.get("logging","level")
f_level=conf.get("logging","f_level")
s_level=conf.get("logging","s_level")
filename=conf.get("logging","filename")
class Mylogger(object):
    @staticmethod
    def getLogger():
        # 一.创建一个名为：testcaseLog的日志收集器
        my_log=logging.getLogger("testcaseLog")
        # 二.设置日志收集器的等级
        my_log.setLevel(level)
        # 三.添加输出渠道
        # 1.创建一个输出控制台的输出渠道
        sh=logging.StreamHandler()
         # 2.设置输出等级
        sh.setLevel(s_level)
        # 3.将输出渠道绑定到日志收集器上去
        my_log.addHandler(sh)
        #四.添加输出渠道（输出到文件）
        fh=logging.FileHandler((os.path.join(LOG_DIR,filename)),encoding="utf8")
        fh.setLevel(f_level)
        #五.设置日志输出格式
        #创建一个日志输出格式
        my_log.addHandler(fh)
        formatter=logging.Formatter("'%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'")
        #将输出格式和输出渠道进行绑定
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)
        return my_log
#调用类的静态方法，创建一个日志收集器
my_log=Mylogger.getLogger()