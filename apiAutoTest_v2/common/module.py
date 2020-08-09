"""
Author:cindy.wang
Time:2019/12/4
E-mail:273705350@qq.com

"""
import random
def random_phone():
    #生成随机号码
    phone="138"
    for i in range(8):
        phone+=str(random.randint(0,9))
    return phone
phone=random_phone()
print(phone)
