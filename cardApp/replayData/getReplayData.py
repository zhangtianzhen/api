import  json
from  jsonpath_rw import jsonpath,parse
from config.requestConfig import BaseConfig
from  DATA_BASE.sqlQuery import  BaseQuery
from replayData.ThroughCaseGet import ForApiget

class RePlay(object):

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

    def finallyresult(self): #获取到本地 或接口数据处理的结果
        if self.getvaluemethod == 1: #如果依赖取值的方式是本地数据库获取
            return self.getforlocal()

        else: ##如果依赖取值的方式是接口返回的数据获取 则执行这里
            return self.getforApi()

    def getforlocal(self): #当依赖是从本地获取数据时
        """
         例如: 这次执行的是 test04 且依赖test02 的token与userid 那么 本模块的执行的最主要的逻辑是
         通过获取test02的依赖数据 即 token 与 userid ,将其放入test04的jsondata数据里面 发送到后台 获取到test04的数据
        """
        try:
            if self.replayid:
                result = self.sql.selectByid_username(self.replayid,self.username)
        except Exception as e:
                print("依赖id不能为空或不存在或取值错误>>>>>依赖数据模块报错",e)
        else:
            try:
                if type(self.keyValue) == str and self.keyValue: #为字符串时 且不为空
                    #print("str",self.keyValue)
                    self.forApiData[self.keyValue] = result[self.keyValue] #对api数据进行处理
                if type(self.keyValue) == list and self.forApiData:
                    for i in self.keyValue: #这里可能隐含bug
                        self.forApiData[i] = result[i]

            except Exception as e:
                print("本地返回数据异常>>>>",e)
            else:
                return self.forApiData
    def getforApi(self): #从接口返回获取数据
        """
         例如: 这次执行的是 test09 且依赖test08 而test08又依赖上个接口的数据 那么 本模块的执行的最主要的逻辑是
         通过获取test08的依赖数据 即 token 与 userid ,将其放入test08的jsondata数据里面 发送到后台 获取到test08的数据 并返回给test09使用
         类似三级联动的效果
        """
        apireturn = ForApiget(self.replayid) #通过上个接口动态返回的数据
        result = apireturn.runTestid()
        try:

            for i in self.keyValue:#动态匹配接口返回数据 用于本次接口所用 例如本次接口是test09
                jsonTemplate = parse("$..%s"%i)
                res = [mach.value for mach in jsonTemplate.find(result)][0]
                self.forApiData[i]=res


        except  Exception as e:
            print("getReplayData模块的{0}方法出现接口取值出现错误>>>>>>".format(self.getvaluemethod),e)


        else:

            return self.forApiData

if __name__ == "__main__":
    t = RePlay(1,"test01","HashedValue",{"HashedValue":""},"T2626")
    print(t.getforlocal())
