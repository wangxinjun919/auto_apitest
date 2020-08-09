from configparser import ConfigParser
import os
from common.contants import CONF_DIR
class Myconf(ConfigParser):
    def __init__(self,filename,encoding="utf8"):
        #调用父类原来的__init__方法，self.read(filename,encoding)
        super().__init__()
        self.filename=filename
        self.encoding=encoding
        # 把文件里的数据放到文件解析器里
        self.read(filename,encoding)

    def write_data(self,section,option,value):
        self.set(section,option,value)
        self.write(open(self.filename,"w",encoding=self.encoding))
conf_path=os.path.join(CONF_DIR,"conf.ini")
conf=Myconf(conf_path)
#可以得到数据，方法父类里面有