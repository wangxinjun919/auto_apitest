"""
Author:cindy.wang
Time:2019/12/11
E-mail:273705350@qq.com

"""
import re
from common.myconfig import conf
class TestData:
    """这个类的作用：专门用来保存一些替换的数据"""
    pass
def replace_data(data):
    r=r"#(.+?)#"  #匹配两个#之间的出现一次及以上的字符，关闭贪婪模式
    #判断是否需要替换的数据
    while re.search(r,data):
        #匹配出第一个要替换的数据
        res=re.search(r,data)
        #提取待替换的内容
        item=res.group()
        #获取替换内容中的数据项
        key=res.group(1)
        try:
            #根据替换内容中的数据项去配置文件中找到对应的内容，进行替换
            data=data.replace(item,conf.get("test_data",key))
        except:
            #如果配置文件里没找到，获取类里面的数据来替换
            data=data.replace(item,getattr(TestData,key))
    #返回替换好的数据
    return data

