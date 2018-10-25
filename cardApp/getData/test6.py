
import json
import requests
import xmltodict
import re
import hashlib
from DATA_BASE.readTEXT  import TextManage
from  DATA_BASE.sqlQuery import BaseQuery

from config.requestConfigtest import API
from jsonpath_rw import parse,jsonpath
from DATA_BASE.readExcel import Excel
from config.execlconfig import *
from handle.Request_distribute import  Distribution
from replayData.newReplay import RePlay #依赖模块


class TestCase(object):

    def __init__(self):
        self.sql = BaseQuery() #sql查询
        self.excel = Excel() #excel操作
        self.req = API() #接口基本信息
        self.post = Distribution() #发送请求的类


    def startCase(self): #执行测试用例
        self.caseNum = self.excel.allCase()
        self.Pass = 0
        self.no = 0
        for i in range(1,self.caseNum):
            #self.req.method = self.excel.getValue(i, getMethod())  # 设置本次请求的方法 *********
            #self.req.url = self.excel.getValue(i, getUrl())  #设置本次请求url
            self.method = self.excel.getValue(i,getMethod()) #请求方法
            self.responseKey = self.excel.getValue(i, getresponseKey())  # 获取存储 接口响应的关键字
            self.responseSave = self.excel.getValue(i, getresponseSave())  # 存储接口的方式
            self.key = self.excel.getValue(i, getInputKey())  # 获取输入框输入值
            self.value = self.excel.getValue(i, getInputValue())  # 获取文本输入键
            self.url = self.excel.getValue(i, getUrl())  # 获取每个用例的url
            self.testid = self.excel.getValue(i, getId())  # 获取到case id
            self.replayid = self.excel.getValue(i, getRelyID())  # 获取到依赖id
            self.getvaluemethod = self.excel.getValue(i, getValueMethod())  # 依赖取值方法
            self.keyValue = self.excel.getValue(i, getRelyData2())  # 依赖上一个接口的关键字
            self.forApidata = self.excel.getValue(i, getRelyFied())  # 放入本次接口的数据
            self.reqBody = self.excel.getValue(i, getRequestDate())  # 请求体放置的内容
            self.save = self.excel.getValue(i, getParameter())  # 保存文本
            self.expect =self.excel.getValue(i,getExpect())
            isrun = self.excel.getValue(i, getExecute())  # 是否执行


            if isrun == "":
                print("发现第{0}测试用例是否执行栏出现空格现象".format(self.testid))
                break
            else:
                if isrun == "yes" or isrun == "Yes" or isrun == "YES":
                   #testid,responseKey,responseSave,url,method,replayid,getvaluemethod,keyValue,forApidata,reqBody,save,key,value
                    self.httpContent()

                elif isrun == "no" or isrun == "No" or isrun == "NO":
                    pass
                    #print("{0}跳过测试用例的执行".format(self.testid))
                else:
                    print("{0}出现未知命令".format(self.testid))
        print("通过%d个接口测试,未通过%d个接口测试"%(self.Pass,self.no))
    def httpContent(self):
        #进行内容逻辑处理
        function = hasattr(self.req,self.method)
        """
        self.req 请求体内容
        self.method 接口地址
        """

        if function:
            if self.replayid =="":
                result = getattr(self.req, self.method)(self.url, method=self.method, thisApi=self.forApidata,args=self.reqBody, extract=self.keyValue, lastApi=self.key)
                expect = eval(self.expect)
                try:
                    if result["StateCode"] == expect[0] and result["StateMsg"] == expect[1]:
                        if len(expect) == 3:

                            if result["ResultType"] == expect[2]:
                                print("接口:%s 测试通过 编号:%s" %(self.method,self.testid))
                                self.Pass += 1
                            elif result["ResultType"] != expect[2]:

                                print("接口:%s 测试不通过 编号:%s 响应状态:%s" % (self.method, self.testid, result["ResultType"]))
                                self.no += 1
                        else:
                            print("接口:%s 测试通过 编号:%s" %(self.method,self.testid))
                            self.Pass += 1
                    else:
                        print("接口:%s 测试未通过 编号:%s" %(self.method,self.testid))
                        self.no += 1
                except Exception as e:
                    print("主运行模块报错>>>>>\t",e)
            else:
                self.replay = RePlay(self.replayid)
                self.replay.runTest()


                result = getattr(self.req, self.method)(self.url, method=self.method, thisApi=self.forApidata,args=self.reqBody, extract=self.keyValue, lastApi=self.key)
                print(result)
                if type(result) == list:
                    result = result[-1]
                expect = eval(self.expect)
                try:
                    if result["StateCode"] == expect[0] and result["StateMsg"] == expect[1]:
                        if len(expect) == 3:
                            if result["ResultType"] == expect[2]:
                                print("接口:%s 测试通过 编号:%s" %(self.method,self.testid))
                                self.Pass += 1
                            elif result["ResultType"] != expect[2]:
                                print("接口:%s 测试不通过 编号:%s 响应状态:%s" %(self.method,self.testid,result["ResultType"]))
                                self.no += 1
                        else:

                            print("接口:%s 测试通过 编号:%s" %(self.method,self.testid))
                            self.Pass += 1
                    else:

                        print("接口:%s 测试未通过 编号:%s" %(self.method,self.testid))
                        self.no += 1
                except Exception as e:
                    print("主运行模块报错>>>>>\t", e)


if __name__ == "__main__":

    p = TestCase()
    p.startCase()