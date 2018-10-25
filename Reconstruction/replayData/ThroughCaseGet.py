""""
如果是通过接口取值的 那么对上一个接口再次执行一次 这里的主要逻辑就是执行单个用例
"""

"""
 例如: 这次执行的是 test09 且依赖test08 而test08又依赖上个接口的数据 那么 本模块的执行的最主要的逻辑是
 通过获取test08的依赖数据 即 token 与 userid ,将其放入test08的jsondata数据里面 发送到后台 获取到test08的数据 并返回给test09使用
"""
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

class ForApiget(object):

    def __init__(self,id):
        self.testid = id #获取到上个测试用例id 通过该id执行用例
        self.excl = Excel()
        self.req = BaseConfig()
        self.sql = BaseQuery()
        self.Dist = Distribution()  # 发送请求的类
    def runTestid(self): #执行该用例
        i=self.excl.get_row_num(self.testid) #找到该id 所在的行
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
        if reqBody:  # 请求体放置的内容
            reqBody = eval(self.excl.getValue(i, getRequestDate()))
        replaydata = self.excl.getValue(i, getreplayaccount())  # 获取依赖id所需的账号
        return self.execute(url,getvaluemethod,replayid,keyValue,forApidata,replaydata,responseKey,responseSave,key,value,testid,save,reqBody)


    def execute(self,url,getvaluemethod,replayid,keyValue,forApidata,replaydata,responseKey,responseSave,key,value,testid,save,reqBody):
        if keyValue:
            keyValue = eval(keyValue) # 依赖上一个接口的关键字 需要做数据类型转换 将excel里面的字符串转成列表
        else:
            keyValue = None
        if forApidata:
            forApiData = eval(forApidata) # # 放入本次接口的数据 需要做数据类型转换  将字符串转成字典
        else:
            forApiData = None

        if replayid:  # 如果本次请求需要依赖id 即需要上一个接口的数据

            respose = self.finallyresult(getvaluemethod, replayid, keyValue, forApiData, replaydata)  # 调用取得依赖数据模块
            replayback = respose  # 从本地或者接口上次接口获取到的数据 进行请求处理 最终目的是获取到本次接口的所需数据

            if replayback:  # 如果获取到本地或接口返回的数据
                if reqBody:  # 请求体需要携带数据 如果为空 则不加入请求体
                    replayback.update(reqBody)  # 如果请求体放置的内容与放入本次接口的数据同时存在数据 则在本次接口请求数据上加入请求体数据
                body = self.req.body(replayback)  # 更新jsondata内容 将接口需要的输入加入到body里面 获取本次最新的请求体内容
                header = self.req.Header() #本次请求体的头部信息

                result = self.Dist.Post(url, body, header)  # 将本地或接口获取到的数据 进行发送请求

                if responseSave !="":
                    if int(responseSave)==2 :  # 处理发送请求后 要保存接口响应的内容
                        responseKey = eval(responseKey) #对excel读取到的数据进行格式化处理 转换成字典
                        save = eval(save)
                        try:
                            for i in responseKey:
                                save[i] = result[i]

                        except:  # 这里这么写的原因
                            # 当依赖的接口过多时 有三种解决方案: 1.将某些数据存储在数据库 简化复杂度 2.写复杂代码 3一个接口对应一个方法  此处选择第一个解决方案
                            for i in responseKey:
                                jsonparse = parse("$..%s" % i)
                                res = [match.value for match in jsonparse.find(result)][0]
                                save[i] = res
                        data = self.sql.selectByUsername(replaydata) #查询数据库内容

                        data.update(save)
                        self.sql.updateByUsername(replaydata, json.dumps(data)) #将数据更新到数据库里面 对应的账号信息里面
                result.update(replayback) #这里做特殊处理在上个接口处理完后 在里面加入usertoken 与userid  用来返回每次必要参数 userid 与 token 只有调用 上次接口返回数据时候 才做的处理
                #用于加入token,userid
                return result #返回本次接口执行后 获取到的数据
            else:
                pass
        else:
            if reqBody:  # 需要加入请求体则执行这里
                if replaydata == "":  # 依赖id 不需要账号
                    if responseSave == "":  # 不需要存储
                        body = self.req.body(reqBody)
                        header = self.req.Header()
                        result = self.Dist.Post(url, body, header)
                else:
                    pass



    def finallyresult(self,getvaluemethod, replayid, keyValue, forApidata, replaydata): #获取到本地 或接口数据处理的结果
        if getvaluemethod == 1:#如果依赖取值的方式是本地数据库获取
            return self.getforlocal(getvaluemethod, replayid, keyValue, forApidata, replaydata)

        else:##如果依赖取值的方式是接口返回的数据获取 则执行这里
            return self.getforApi(replayid)

    def getforlocal(self,getvaluemethod, replayid, keyValue, forApidata, replaydata):  # 当依赖是从本地获取数据时 进行本地数据获取
        try:
            if replayid:
                result = self.sql.selectByid_username(replayid, replaydata)

        except Exception as e:
            print("依赖id不能为空或不存在或取值错误>>>>>依赖数据模块报错", e)
        else:
            try:
                if type(keyValue) == str and keyValue:
                    forApidata[keyValue] = result[keyValue]  # 对api数据进行处理
                if type(keyValue) == list and forApidata: #对列表取值的处理
                    for i in keyValue:
                        forApidata[i] = result[i]

            except Exception as e:
                print("本地返回数据异常>>>>", e)
            else:
                return forApidata #返回本地数据库获取到的数据 例如 token userid

    def getforApi(self,replayid):  # 从接口返回获取数据 进行处理 获取想要的数据
        apireturn = ForApiget(replayid)  # 通过上个接口动态返回的数据
        try:
            print(replayid)
        except  Exception as e:
            print("接口取值出现错误>>>>>>", e)
if __name__ == "__main__":
    t=ForApiget("test08")
    t.runTestid()
