id = 0 #用例id
page = 1 #页面
name = 2 # 用例名称
client= 3 #客户端类型
response_save = 4 #接口响应内容存储文本(1:不存储,2:存储)
response_key = 5
parameter = 6 #接口响应内容存储文本
url = 7  #url地址
method = 8 #方法名
execute = 9 #是否执行
request_method= 10 #请求方式
header = 11 #请求头
relyID = 12#依赖id
getvaluemethod = 13 #依赖取值方法
relyData2 = 14 #依赖上一个接口的关键字
relyFied = 15#放入本次接口的数据
requestDate = 16 #请求体放置的内容
inputkey = 17 #输入框输入的键
inputvalue = 18 #输入内容的值
replayaccount = 19 #账号
Expect = 20



def getId():
    return id

def getPage():
    return page

def getNmae():
    return name

def getClien():
    return client

def getParameter():
    return parameter

def getUrl():
    return url

def getresponseSave():
    return response_save

def getresponseKey():
    return response_key

def getMethod():
    return method

def getExecute():
    return execute

def getRequest_Method():
    return request_method

def getHeader():
    return header

def getRelyID():
    return relyID

def getValueMethod():
    return getvaluemethod


def getRelyData2():
    return relyData2
def getRelyFied():
    return relyFied

def getRequestDate():
    return requestDate

def getInputKey():
    return  inputkey

def getInputValue():
    return  inputvalue

def getreplayaccount():
    return replayaccount

def getExpect():
    return Expect