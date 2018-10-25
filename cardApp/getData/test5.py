import  re
import json
import requests
import xmltodict
import re
import hashlib
from DATA_BASE.readTEXT  import TextManage
from  DATA_BASE.sqlQuery import BaseQuery
from config.requestConfig import BaseConfig
from jsonpath_rw import parse,jsonpath
from DATA_BASE.readExcel import Excel
from config.execlconfig import *
from handle.Request_distribute import  Distribution
from replayData.getReplayData import RePlay #依赖模块

class Login(object):

    def __init__(self):
        self.sql = BaseQuery()
        self.excl = Excel()
        self.req = BaseConfig()
        self.Dist = Distribution() #发送请求的类

    def request(self):
        case = self.excl.allCase()

        for i in range(1,case):
            self.req.method = self.excl.getValue(i, getMethod())  # 设置本次请求的方法 *********
            responseKey = self.excl.getValue(i,getresponseKey()) #获取存储 接口响应的关键字
            responseSave =  self.excl.getValue(i,getresponseSave()) #存储接口的方式
            key = self.excl.getValue(i, getInputKey()) #获取文本输入值
            value = self.excl.getValue(i, getInputValue()) #获取文本输入键
            url = self.excl.getValue(i, getUrl()) #获取每个用例的url
            testid = self.excl.getValue(i,getId()) #获取到case id
            replayid = self.excl.getValue(i,getRelyID()) #获取到依赖id
            getvaluemethod = self.excl.getValue(i, getValueMethod())  # 依赖取值方法
            keyValue = self.excl.getValue(i, getRelyData2())  # 依赖上一个接口的关键字
            forApidata = self.excl.getValue(i, getRelyFied())  # 放入本次接口的数据
            reqBody = self.excl.getValue(i, getRequestDate())  # 请求体放置的内容
            save = self.excl.getValue(i,getParameter()) #保存文本
            isrun = self.excl.getValue(i,getExecute()) #是否执行
            if isrun =="":
                print("发现第{0}测试用例是否执行栏出现空格现象".format(testid))
                break
            else:
                if isrun == "yes" or isrun == "Yes" or isrun == "YES":
                    if reqBody:  # 请求体放置的内容
                        reqBody = eval(self.excl.getValue(i, getRequestDate()))
                    replaydata = self.excl.getValue(i,getreplayaccount()) #获取依赖id所需的账号
                    if i == 1: #特殊逻辑 只对第一个用例id操作 用来生成密的字符串

                        body = self.req.body(reqBody)
                        header = self.req.Header()
                        result= self.Dist.Post(url,body,header) #发送请求

                        if result:
                            salt = result["Salt"] #获取加密数据
                            username = result["UserName"]
                            md5 = self.req.md5Function(salt,username,value) #加密
                            HashedValue = {"HashedValue":md5}
                            sqlRes = self.sql.selectByUsername(username) #查询sql的结果

                            if sqlRes:
                                sqlRes.update(result)
                                sqlRes.update(HashedValue)
                                self.sql.updateByUsername(username,json.dumps(sqlRes))
                            else:
                                result.update(HashedValue)
                                self.sql.insert(testid,username,json.dumps(result))
                    else:

                        if replayid: #如果需要依赖id 即需要上一个接口的数据
                            self.Rep = RePlay(getvaluemethod,replayid,keyValue,forApidata,replaydata) #调用依赖数据模块
                            replayback = self.Rep.finallyresult() #进行上次依赖数据的处理
                            if replayback: #如果获取到本地或接口返回的数据
                                if reqBody: #请求体需要携带数据 如果为空 则不加入请求体
                                   replayback.update(reqBody) #如果请求体与接口同时存在数据 则在本次接口请求数据上加入请求体数据
                                body = self.req.body(replayback) # 更新jsondata内容 将接口需要的输入加入到body里面 获取本次最新的请求体内容
                                header = self.req.Header()

                                result = self.Dist.Post(url, body, header)  # 发送请求
                                if responseSave != "":
                                    if int(responseSave) == 1  : #处理发送请求后 要保存接口响应的内容
                                        responseKey = eval(responseKey)
                                        save = eval(save)
                                        try:
                                            for i in responseKey:
                                                save[i] = result[i]

                                        except: #这里这么写的原因
                                            # 当依赖的接口过多时 有三种解决方案: 1.将某些数据存储在数据库 简化复杂度 2.写复杂代码 3一个接口对应一个方法  此处选择第一个解决方案
                                            for i in responseKey:
                                                jsonparse = parse("$..%s"%i)
                                                res = [match.value for match in jsonparse.find(result)][0]
                                                save[i]=res

                                        data = self.sql.selectByUsername(replaydata)
                                        data.update(save)
                                        self.sql.updateByUsername(replaydata,json.dumps(data))

                            else:
                                pass
                        else:
                            if reqBody:  #需要加入请求体
                                if replaydata =="" :#不需要依赖id所需的账号
                                    if responseSave == "": #不需要存储
                                        body = self.req.body(reqBody)
                                        header = self.req.Header()
                                        result = self.Dist.Post(url,body,header)
                                else:
                                    pass
                elif isrun == "no" or isrun == "No" or isrun == "NO":
                    print("第{0}跳过测试用例的执行".format(testid))
                else:
                    print("第{0}出现未知命令".format(testid))





    def httpContent(self, testid, responseKey, responseSave, url, method, replayid, getvaluemethod, keyValue,
                    forApidata, reqBody, save, key, value):
        # 进行内容逻辑处理
        function = hasattr(self.req, method)
        if function:
            ret = getattr(self.req, method)
            print(ret('{"UserName":"T2626"}'))

        else:
            print("没有该请求接口的存在")


if __name__ == "__main__":
    test = Login()
    test.request()
