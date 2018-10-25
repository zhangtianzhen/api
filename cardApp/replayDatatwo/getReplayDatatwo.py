import  json
from  jsonpath_rw import jsonpath,parse
from config.requestConfig import BaseConfig
from  DATA_BASE.sqlQuery import  BaseQuery
from replayData.ThroughCaseGet import ForApiget
class RePlayTwo(object):

    def __init__(self,getvaluemethod,replayid,keyValue,forApidata,username):
        self.replayid = replayid  # 获取依赖id
        self.getvaluemethod = int(getvaluemethod)#获取依赖数据的方式
        if keyValue:
            self.keyValue = eval(keyValue) # 依赖上一个接口的关键字 需要做数据类型转换 将excel里面的字符串转成列表
        else:
            self.keyValue = None
        if forApidata:
            self.forApiData = eval(forApidata) # # 放入本次接口的数据 需要做数据类型转换  将字符串转成字典
        else:
            self.forApiData = None
        self.username = username #依赖id所需的账号
        self.sql = BaseQuery()

    def finallyresult(self):
        if self.getvaluemethod == 1:
            return self.getforlocal()

        else:
            return self.getforApi()

    def getforlocal(self): #当依赖是从本地获取数据时
        try:
            if self.replayid:
                result = self.sql.selectByid_username(self.replayid,self.username)
        except Exception as e:
                print("依赖id不能为空或不存在或取值错误>>>>>依赖数据模块报错",e)
        else:
            try:
                if type(self.keyValue) == str and self.keyValue:
                    #print("str",self.keyValue)
                    self.forApiData[self.keyValue] = result[self.keyValue] #对api数据进行处理
                if type(self.keyValue) == list and self.forApiData:
                    for i in self.keyValue:
                        self.forApiData[i] = result[i]

            except Exception as e:
                print("本地返回数据异常>>>>",e)
            else:
                return self.forApiData
    def getforApi(self): #从接口返回获取数据
        apireturn = ForApiget(self.replayid) #通过上个接口动态返回的数据
        try:
            print(self.replayid)
        except  Exception as e:
            print("接口取值出现错误>>>>>>",e)




if __name__ == "__main__":
    t = RePlayTwo(1,"test01","HashedValue",{"HashedValue":""},"T2626")
    print(t.getforlocal())
