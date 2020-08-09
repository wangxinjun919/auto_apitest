import openpyxl
import os
from common.contants import DATA_DIR
#用来存储用例对象
class CaseData():
    pass
class ReadExcel(object):
    def __init__(self,filename,sheet_name):
        '''

        :param filename: 文件名
        :param sheet_name: 表单名
        '''
        self.filename=filename
        self.sheet_name=sheet_name

    def open(self):
        self.wb=openpyxl.load_workbook(self.filename)
        self.sh=self.wb[self.sheet_name]
    def save(self):
        self.wb.save(self.filename)
        self.close()
    def close(self):
        self.wb.close()
    def read_data(self):
        self.open()
        #按行获取所有格子对象
        rows=list(self.sh.rows)
        #获取第一行数据
        title=[]
        for i in rows[0]:
            title.append(i.value)
        #创建一个空列表，用来存储改行的数据
        cases = []
        #遍历第二行开始的数据
        for row in rows[1:]:
            data = []
            #再次遍历每一个格子
            for r in row:
                #格子里面的数据，添加到data里面
                data.append(r.value)
            #title和data聚合打包成字典
            case = dict(zip(title, data))
            cases.append(case)
        print(cases)
        self.close()
        return cases
    def read_data_object(self):
        self.open()

        #按行获取所有的格子对象
        rows=list(self.sh.rows)
        #获取第一行数据
        title=[]
        for i in rows[0]:
            title.append(i.value)
        #创建一个空列表
        cases=[]
        #遍历第二行开始的数据
        for row in rows[1:]:
            data = []
            # 再次遍历每一个格子
            for r in row:
                # 格子里面的数据，添加到data里面
                data.append(r.value)
            # title和data聚合打包成字典转换成列表
            case = list(zip(title, data))
            #创建一个对象用来保存该行的用例数据
            case_obj=CaseData()
            #遍历列表中该行用例数据，使用setarr设置成对象的属性和属性值
            for k,v in case:
                setattr(case_obj,k,v)
            #将对象添加到cases这个列表中
            cases.append(case_obj)
        #返回cases(包含所有用例数据对象的对象)
        return cases

    def write_data(self,row,column,value):
        #打开工作簿，写入数据
        self.open()
        #写入数据
        self.sh.cell(row=row,column=column,value=value)
        #保存文件
        self.wb.save(self.filename)
        self.close()
if __name__=='__main__':
    excel1=ReadExcel(os.path.join(DATA_DIR,"case.xlsx"),"login")
    excel2 = ReadExcel(os.path.join(DATA_DIR, "case.xlsx"), "register")
    data1=excel1.read_data()
    data2=excel2.read_data()
    print(data1)
    print(data2)
