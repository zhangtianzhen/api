from config.execlconfig import *
from handle.Request_distribute import  Distribution
from  DATA_BASE.sqlQuery import BaseQuery
import json
from config.requestBase import API
from jsonpath_rw import parse,jsonpath
from DATA_BASE.readExcel import Excel
from config.execlconfig import *
from jsonpath_rw import jsonpath
import time
nowTime=time.strftime('%Y-%m-%d %H:%M:%S')

class TestCase(object):

    def __init__(self):
        self.sql = BaseQuery()  # sql查询
        self.excel = Excel()  # excel操作
        self.req = API()  # 接口基本信息


    def startCase(self): #执行测试用例
        self.caseNum = self.excel.allCase()
        self.Pass = 0
        self.no = 0
        for i in range(1,self.caseNum):
            self.testid = self.excel.getValue(i,getId())
            self.url = self.excel.getValue(i,getUrl())
            self.method = self.excel.getValue(i,getApiName()) #请求地址的名字
            self.function = self.excel.getValue(i,getFunctionName()) #执行的方法名字
            self.forApidata = self.excel.getValue(i,getThisapi()) #放入本次接口的名字
            self.add1 = self.excel.getValue(i,getAdd1()) #额外参数一
            self.add2 = self.excel.getValue(i,getAdd2()) #额外参数二
            isrun = self.excel.getValue(i,getExecute()).strip()#是否执行
            self.expect = self.excel.getValue(i,getExpect())
            self.other = self.excel.getValue(i,getHeader())
            self.expect =  self.excel.getValue(i,getExpect())
            self.key = self.excel.getValue(i,getKeys())#依赖参数的关键字

            if isrun == "":
                print("发现第{0}测试用例是否执行栏出现空格现象".format(self.testid))
                break
            else:
                if isrun == "yes" or isrun == "Yes" or isrun == "YES":
                    self.httpContent()

                elif isrun == "no" or isrun == "No" or isrun == "NO":
                    pass
                else:
                    print("{0}出现未知命令".format(self.testid))
        print("通过%d个接口测试,未通过%d个接口测试" % (self.Pass, self.no))

    def httpContent(self):
        selectResult  = self.sql.selecet(self.testid)
        function = hasattr(self.req, self.function)
        if function:
            result = getattr(self.req, self.function)(method=self.method,thisApi=self.forApidata,need =self.other,key=self.key,add1=self.add1)
            expects = eval(self.expect)
            flag = True
            try:
                for i in expects:
                    jsonparse = parse("$..%s" % i)
                    ret = [match.value for match in jsonparse.find(result)][0]
                    if ret == expects[i]:
                        pass
                    else:
                        flag = False
                        Pass = "接口测试不通过"
                        print(Pass)
                        if selectResult ==  None:
                            self.sql.insert(self.testid, self.expect,Pass,json.dumps(result),nowTime)
                        elif selectResult["testid"] == self.testid:
                            self.sql.update(self.testid, self.expect, Pass, json.dumps(result),nowTime)
                        break
                if flag:
                    Pass = "接口测试通过"
                    if selectResult == None:
                        self.sql.insert(self.testid,self.expect,Pass,json.dumps(result),nowTime)

                    elif selectResult["testid"] == self.testid:
                        self.sql.update(self.testid,self.expect,Pass,json.dumps(result),nowTime)

                    print(Pass)
            except Exception as e:
                print("getData模块",e)
if __name__ == "__main__":
    test = TestCase()
    test.startCase()
