import base64
import re
import json
import os
import hashlib
from jsonpath_rw import jsonpath,parse
import  time
MasterSecret = "CTGi*7d54Fs*eruieud545Jgsdudb===Yhdt6"
AppEstateId =  "A53F512B2108EAD5"
Version = "1.0.0"
DeviceInfo = "Redmi Note 4|7.0|WIFI网络|1.0.0|AArch64 Processor rev 4 (aarch64)"
ClientType = "2"
Language = 2
UserName = "T2626"
Location="N/A"
RegistrationID  = "120c83f76071ca71611"
from handle.Request_distribute import  Distribution

def getRegistrationID():
    return RegistrationID
def getLocation():
    return Location

def getMasterSecret(m=MasterSecret):
    return m
def getAppEstateId(a=AppEstateId):
    return a

def getVersion(v=Version):
    return v

def getDeviceInfo(d=DeviceInfo):
    return d

def getClientType(c=ClientType):
    return c

def getLanguage(l=Language):
    return l

class BaseConfig(object):


    def __init__(self):
        self.sendRequest = Distribution()



    def headers(self,method=None): #此处必须传要调用的接口方法
        self.header = {
            "SOAPAction": "http://tempuri.org/ICardAppService/" + method,
            "Accept": "application/json,text/javascript,*/*",
            "Content-Type": "text/xml;charset=UTF-8"
        }
        return self.header
    def form1(self,method=None):

        self.data1 = """
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <soap:Body>
        <""" + method + """ xmlns="http://tempuri.org/"><JsonData>"""
        return self.data1

    def form2(self,dict1=None):
        """
              :param dict1: 请求体body
              :return:
              """
        self.data = {
            "MasterSecret":getMasterSecret(),"AppEstateId":getAppEstateId(),"Version":getVersion(),
            "DeviceInfo":getDeviceInfo(),"ClientType":getClientType(),"Language":getLanguage(),
            "Location":getLocation(),"RegistrationID":getRegistrationID()
        }
        if dict1:
            if type(dict1) == str:
                dict1 = eval(dict1) #将excel读取到的字符串转换成字典
            self.data.update(dict1)
            return json.dumps(self.data)
        else:

            return json.dumps(self.data)

    def form3(self,method=None):


        self.data2 = """
    </JsonData>
        </"""+method+""">
        </soap:Body>
        </soap:Envelope>
            """

        return self.data2

    def md5Function(self,salt, username, password): #md5計算方法
        ecode = salt + ":" + username + ":" + password
        md5 = hashlib.md5()
        md5.update(ecode.encode(encoding='utf-8'))  # 加密的后的密码 需要大写
        code = md5.hexdigest()
        code = code.upper()  # 转换成大写的
        return code

    def body(self,method=None,dict1=None):
        """

        :param dict1: 请求体body
        :return:
        """
        try:
            if dict1:
                return self.form1(method)+self.form2(dict1)+self.form3(method)
            else:
                return self.form1(method)+self.form2()+self.form3(method)
        except Exception as e:
            print("API基本配置模块报错>>>>>\t",e)


class API(BaseConfig):
    HashedValue = ""  # 存放 哈希值
    md5 = {}  # 存放Salt,用户账号
    info = {}  # 存放账号的usertokn,userid,username等必须的参数


    def GetUserLoginInfo(self,dict1=None):
        if dict1 !=None: #这是执行用例时候使用
            pass
        else:
            dict1={"UserName":"T2626","password":"a123456"} #不执行用例时候 使用
        url = 'http://altomobile.test.cn-cic.com/CardAppService.svc'
        method = "GetUserLoginInfo"
        username = {"UserName":dict1["UserName"]} #传字典进入请求内容里面
        password = dict1["password"]

        header = super(API,self).headers(method)
        body = super(API,self).body(method,username)
        result = self.sendRequest.Post(body,header)["ResultData"]
        for i in ["UserName","Salt"]:
            self.md5[i] =result[i]
        self.HashedValue = self.md5Function(self.md5["Salt"],self.md5["UserName"], password)
        #print(self.md5)

    def longin1(self,method=None,need=None,thisApi=None,key=None,add1=None):
        try:
            thisApi = eval(thisApi)
            self.GetUserLoginInfo(thisApi)  # 生成哈希值
            UserName = {"Username":self.md5.get("UserName")}
            HashedValue = {"HashedValue":self.HashedValue}
            thisApi.update(UserName)
            thisApi.update(HashedValue)

            header = super(API,self).headers(method)
            body = super(API,self).body(method,thisApi)
            result = self.sendRequest.Post(body,header)

            for i in ["UserToken","UserId"]:
                self.info[i] = result["ResultData"][i]
            return result
        except Exception as e:
            print(e)
        #return result["StateList"]
    def token_userid(self):  # 封装 公共的提取 usertoken的方法
        try:
            dict1 = {}
            for i in ["UserToken","UserId"]:
                dict1[i] = self.info[i] #结合用例时 需要切换到self.info
            return dict1
        except Exception as e:
            print("token报错",e)
    def body_headers(self,method=None,thisApi=None,key=None,add1=None): #封装 公共的 获取请求头 与 请求体的方法
        try:
            if thisApi == None or thisApi == "":
                body = super(API,self).body(method,self.token_userid()) #当本次接口不需要额外参数时获取基类的基本请求参数  self.token_userid(args) 的作用是获取token userid 并加入到本次请求中
            else:
                if type(thisApi) != dict: #不是字典时候 用eval转换成字典
                    thisApi = eval(thisApi) #当本次接口需要额外的参数时 以字典形式与本次 token一起加入到 请求参数中 转换成字典 例如:eamil:1234@qq.com或mobile：123456之类的
                thisApi.update(self.token_userid())
                body = super(API, self).body(method,thisApi)
            headers = super(API,self).headers(method)
            return [body,headers]
        except Exception as e:
            print(e)


    def jsonpase(self,getparse,result):
        ret = None

        if type(getparse) == str:

            jsonparse = parse("$..%s"%getparse)
            ret = [match.value for match in jsonparse.find(result)]

        elif type(getparse) == list:

            for i in getparse:
                jsonparse = parse("$..%s"%i)
                ret= [match.value for match in jsonparse.find(result)]

        return ret

    def decompression(self,need):
        try:
            need = eval(need)
            functionName = []
            for i in need.keys():  # 先将所有参数的关键字加入到列表中
                functionName.append(i)

            at = []
            for v in functionName:  # 循环当前列表
                args = {"method": None, "thisApi": None, "need": None, "key": None, "add1": None}
                for i in need[v].keys():  # 根据关键字查找当 提取出关键字
                    for j in args.keys():  # 提取当前的方法需要的关键
                        if j == i:  # 传入进来的关键字在当前方法里面
                            args[j] = need[v][j]  # 加入到当前方法里面去
                at.append(args)  # 添加上个接口需要的的参数
            return at
        except Exception as e:
            print("解压>>>:",e)

    def getOwnerInfo(self,method=None,need=None,thisApi=None,key=None,add1=None):
        thisApi =  eval(thisApi)
        ret= self.body_headers(method,thisApi)
        result = self.sendRequest.Post(ret[0],ret[1])
        return result

    def getUserInfo(self, method=None, need=None, thisApi=None, key=None, add1=None):  # 获取组队广场的信息

        thisApi = eval(thisApi)
        ret = self.body_headers(method, thisApi)
        result = self.sendRequest.Post(ret[0], ret[1])
        return result

    def getUserInfo1(self,method=None,need=None,thisApi=None,key=None,add1=None): #获取组队广场的信息
        """邀请组队第一步获取未组队人的id"""""
        currTime = time.strftime("%Y-%m-%dT%H:%M:%S")
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(ret[0],ret[1])
        page = 2
        while True:
            for i in result["ResultData"].get("TeamMemberList"):
                if i["TeamStatus"] == 1: #如果找到了 则停止查找
                    return i["UserId"]  # 返回给方法

            if len(result["ResultData"]["TeamMemberList"]) == 0:
                break #当查询所有结果为空时 返回None
            thisApi["page"] = page
            thisApi["CurrentServerTime"] = currTime+".9349649+08:00"
            ret = self.body_headers(method, thisApi)
            result = self.sendRequest.Post(ret[0], ret[1])
            page += 1

    def joinTeam(self,method=None,need=None,thisApi=None,key=None,add1=None): #邀请组队
        """邀请组队第二步获取发送邀请"""""
        need = self.decompression(need)
        UserId = self.getUserInfo1(**need[0])
        thisApi = eval(thisApi)
        thisApi.update({"ToUserId":UserId})
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(ret[0],ret[1])
        return result
        #return  {"StateCode": 1001, "StateMsg": "成功", "ResultType": 1}


    def getTeamUplist(self,method=None,need=None,thisApi=None,key=None,add1=None): #获取组队ID
        thisApi = eval(thisApi)
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(ret[0],ret[1])
        return result

    def getTeamUplist1(self, method=None, need=None, thisApi=None, key=None, add1=None):  # 获取组队ID
        thisApi = eval(thisApi)
        ret = self.body_headers(method, thisApi)
        result = self.sendRequest.Post(ret[0], ret[1])
        for i in result["ResultData"]["TeamUpListEntity"]:
            if i["TeamUpType"] == 3 and i["FromUserId"] == 61:  # 这里的FromUserId 不能写死
                return i["TeamUpId"]


