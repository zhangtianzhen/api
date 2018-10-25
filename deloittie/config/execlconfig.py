id = 0 #用例id
page = 1 #页面
name = 2 # 用例名称
client= 3 #客户端类型
url = 4 #url地址
apiName  = 5 #接口名字
execute = 6 #是否执行
functionName = 7  #执行的方法名字
header = 8 #请求头
keys = 9 #依赖参数的关键字
thisapi= 10 #放入到本次接口请求的参数
add1 = 11 #额外的参数
add2 = 12#额外的参数
Expect = 13

getvaluemethod = 130 #依赖取值方法
relyData2 = 14 #依赖上一个接口的关键字
relyFied = 15#放入本次接口的数据
requestDate = 16 #请求体放置的内容
inputkey = 17 #输入框输入的键
inputvalue = 18 #输入内容的值
replayaccount = 19 #账号




def getId():
    return id

def getPage():
    return page

def getNmae():
    return name

def getClien():
    return client

def getApiName():
    return apiName

def getUrl():
    return url

def getFunctionName():
    return functionName

def getKeys():
    return keys

def getExecute():
    return execute

def getThisapi():
    return thisapi

def getHeader():
    return header


def getAdd1():
    return add1

def getAdd2():
    return add2


def getExpect():
    return Expect













def getValueMethod():
    return getvaluemethod


def getRequestDate():
    return requestDate


def getInputKey():
    return  inputkey

def getInputValue():
    return  inputvalue

def getreplayaccount():
    return replayaccount
