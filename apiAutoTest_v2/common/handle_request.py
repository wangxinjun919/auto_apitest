"""
封装的需求：
发送post请求，发送get请求，发送patch请求
代码中如何做到不通请求方式的接口去发送不同的请求   加判断

"""
import requests
class HandleRequest:
    def send(self,url,method,params=None,data=None,json=None,headers=None):   #def中定义None的含义：没有传参数，他就默认为None，如果传了参数，则取所传的参数
        #将请求中的方法转换成小写
        method=method.lower()
        if method=="post":
            return requests.post(url=url,json=json,data=data,headers=headers)
        elif method=="patch":
            return requests.patch(url=url,json=json,data=data,headers=headers)
        elif method=="get":
            return requests.get(url=url,params=params)
class HandleSessionRequest:
    #使用sesssion鉴权接口，使用这个类发送请求
    def __init__(self):
        self.se=requests.session()

    def send(self, url, method, params=None, data=None, json=None,headers=None):  # def中定义None的含义：没有传参数，他就默认为None，如果传了参数，则取所传的参数
        # 将请求中的方法转换成小写
        method = method.lower()
        if method == "post":
            return self.se.post(url=url, json=json, data=data, headers=headers)
        elif method == "patch":
            return self.se.patch(url=url, json=json, data=data, headers=headers)
        elif method == "get":
            return self.se.get(url=url, params=params)

