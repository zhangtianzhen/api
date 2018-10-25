"""
配置基本的请求头数据 可动态添加 方便进行配置
"""
import base64
import re
import json

import hashlib
from jsonpath_rw import jsonpath,parse
MasterSecret = "CTGi*7d54Fs*eruieud545Jgsdudb===Yhdt6"
AppEstateId =  "6124F8B9618591FA"
Version = "1.0.0"
DeviceInfo = "Redmi Note 4|7.0|WIFI网络|1.0.0|AArch64 Processor rev 4 (aarch64)"
ClientType = "2"
Language = 2
UserName = "T2626"
Location="N/A"
RegistrationID  = "170976fa8aa40eb997d"
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

def getUserName(u=UserName):
    return u
def getmethod(function=None):
    return function

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
    HashedValue = {}  # 存放 哈希值
    md5 = {}  # 存放Salt,用户账号
    info = []  # 存放账号的usertokn,userid,username等必须的参数

    def GetUserLoginInfo(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #登录第一步

        """

        :param method: 请求的接口地址
        :param args:  请求体放置的参数
        :return:
        """

        try:

            password = re.findall(r'"password":"(.*)?"', args)[0]

            assert password !=""
        except Exception as e:
            print("登录第一步接口报错信息>>>密码没有提取到:\t",e)
            return None
        else:
            headers = super(API, self).headers(method) #获取请求头
            body = super(API, self).body(method,args)
            """
            发送post请求
            """
            result = self.sendRequest.Post(url,body,headers)
            UserName = result["UserName"]
            for i in ["Salt","UserName"]:
                self.md5[i] = result[i]
            if len(self.HashedValue ) == 0:
                self.HashedValue[UserName] = self.md5Function(self.md5["Salt"],self.md5["UserName"], password)
            else:
                for i in self.HashedValue:
                    if i == UserName:
                        self.HashedValue[UserName] = (self.md5Function(self.md5["Salt"],self.md5["UserName"], password))
            return result

    def UserLogin(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):#登录第二步

        #self.GetUserLoginInfo("http://altomobile.test.cn-cic.com/CardAppService.svc","GetUserLoginInfo",'{"UserName":"T2626","password":"a123456"}') #调用登陆第一步 生产 加密字符串

        try:
            HashedValue = None
            for i in self.HashedValue:
                if i == args or i == args.lower():
                    HashedValue = self.HashedValue[args]

            body = super(API, self).body(method,{"HashedValue":HashedValue,"UserName":self.md5["UserName"]})

            headers = super(API,self).headers(method)

            result = self.sendRequest.Post(url,body,headers)
            dict1 = {"UserName":result["UserName"],"UserId":result["UserId"],"UserToken":result["UserToken"]}
            UserName = result["UserName"]
        except Exception as e:
            print("方法:UserLogin",e)

        else:
            if len(self.info) == 0:
                self.info.append(dict1)
            else:
                for i in self.info: #存在 则修改
                    if i["UserName"] ==UserName:
                        i["UserToken"] = dict1["UserToken"]
                        break
                    else: #不存在 则新增用户信息
                        self.info.append(dict1)
                        break
           # print(self.info)
            return result

    def LostLoginPassword(self,url,method=None,thisApi=None,args= None,extract=None,lastApi=None):

        """""
        定制化请求方式 这里不适用公共方法
        """""
        body = super(API,self).body(method,thisApi)
        headers = super(API,self).headers(method)
        result = self.sendRequest.Post(url,body,headers)
        return result
    def token_userid(self,args): #封装 公共的提取 usertoken的方法

        try:
            index = 0
            for i in self.info: #查找当前账号所在位置的下标

                if i["UserName"] == args or i["UserName"] == args.lower() :
                    index = 0
                    break
                else:
                    index += 1

            return {"UserToken":self.info[index]["UserToken"],"UserId":self.info[index]["UserId"]} #根据下标获取对应的账号与密码
        except Exception as e:

            print("方法:token_userid 账号或者密码错误",e)

    def body_headers(self,method=None,thisApi=None,args=None,extract=None,lastApi=None): #封装 公共的 获取请求头 与 请求体的方法
        try:
            if thisApi == None or thisApi == "":
                body = super(API,self).body(method,self.token_userid(args)) #当本次接口不需要额外参数时获取基类的基本请求参数  self.token_userid(args) 的作用是获取token userid 并加入到本次请求中
            else:
                if type(thisApi) != dict: #不是字典时候 用eval转换成字典
                    thisApi = eval(thisApi) #当本次接口需要额外的参数时 以字典形式与本次 token一起加入到 请求参数中 转换成字典 例如:eamil:1234@qq.com或mobile：123456之类的
                thisApi.update(self.token_userid(args))
                body = super(API, self).body(method,thisApi)
            headers = super(API,self).headers(method)
            return [body,headers]
        except Exception as e:
            print(e)

    def GetCurrentUserInfo(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):

        body = super(API,self).body(method,self.token_userid(args))
        headers = super(API,self).headers(method)
        result = self.sendRequest.Post(url,body,headers)
        return result

    def EditPassword(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):

        """"
        
        :param url:  网址
        :param method:  接口方法
        :param thisApi:  本次接口需要的参数
        :param args:  账号或密码
        :return: 
        """""

        try:
            result = self.sendRequest.Post(url,self.body_headers(method,thisApi,args)[0], self.body_headers(method,thisApi,args)[1])
        except Exception as  e:
            print(e)
        else:
            return result


    def EditUserInfo(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #修改个人信息
        result = self.sendRequest.Post(url,self.body_headers(method,thisApi,args)[0],self.body_headers(method,thisApi,args)[1])
        return result
    def UserLogout(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #用户登出

        body = super(API,self).body(method,self.token_userid(args))
        headers = super(API,self).headers(method)
        result = self.sendRequest.Post(url, body, headers)
        return result
    def index(self,args): #封装查找下标的方法
        """"
        
        :param args:  要传入用户名 根据用户查找数据
        :return: 
        """""
        index = 0
        for i in self.info:  # 查找当前账号所在位置的下标

            if i["UserName"] == args or i["UserName"] == args.lower():
                index = 0
                break
            else:
                index += 1
        return index

    def jsonparse(self,args=None,extract=None,result=None): #封装保存接口响应的方法

        index = self.index(args)  # 查找到当前用户所在的下标
        try:
            for i in eval(extract):
                jsonParse = parse("$..%s" % i)
                find = [match.value for match in jsonParse.find(result)][0]
                self.info[index][i] = find
            print(self.info)
        except Exception as e:
            print("未匹配到",e)

    def GetHandoverHouseDateList(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #可預約日期列表 目的 获取HandoverHouseDate 获取交楼日期 根据日期交楼
        """
        
        :param url:  地址
        :param method: 接口
        :param thisApi: 邮箱 账号密码之类的
        :param args:  查找当前账号的token的账号
        :param extract: 提取接口请求返回来的参数 用于下一次接口请求的使用
        :return: 
        """""


        result = self.sendRequest.Post(url, self.body_headers(method,thisApi,args)[0],self.body_headers(method,thisApi,args)[1])
        self.jsonparse(args,extract,result)

        return result



    def GetHandoverHouseList(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):
        """"
        #根據日期獲取可预约列表 目的:获取HandoverHouseId  根据这个日期提交预约
        :param url: 
        :param method: 
        :param thisApi: 
        :param args: 
        :param extract: 
        :param lastApi: 获取上个接口的参数 用于本次接口请求 
        :return: 
        """""

        index = self.index(args) #查找到当前用户所在的下标
        dict1 = {}
        try:
            for i in eval(lastApi): #转换成列表 找到了 放入到本次请求中
                dict1[i] = self.info[index].get(i)
            result = self.sendRequest.Post(url, self.body_headers(method, dict1, args)[0],
                                           self.body_headers(method, dict1, args)[1])
            self.jsonparse(args, extract, result)  # 调用 这个方法 用于存储本次接口返回的数据

            return result
        except Exception as e:
            print(e)




    def BookHandoverHouse(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):
        """"
        提交預約
        """""
        try:
            index = self.index(args)
            dict1 = {}
            for i in eval(lastApi):  # 转换成列表 找到了 放入到本次请求中
                dict1[i] = self.info[index].get(i)
            thisApi= eval(thisApi)
            thisApi.update(dict1)
            result = self.sendRequest.Post(url,self.body_headers(method,thisApi,args)[0],self.body_headers(method,thisApi,args)[1])
            return result
        except Exception as e:
            print(e)


    def GetHandoverHouseSetting(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):
        """"
        獲取預約相關信息  目的获取HandoverHouseRecordId 用于取消预约
        """""
        index = self.index(args)
        dict1 = {}
        for i in eval(lastApi):  # 转换成列表 找到了 放入到本次请求中
            dict1[i] = self.info[index].get(i)
        thisApi=dict1
        result = self.sendRequest.Post(url,self.body_headers(method,thisApi,args)[0],self.body_headers(method,thisApi,args)[1])
        self.jsonparse(args,extract,result)

        return result
    def CancelBookHandoverHouse(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):
        index = self.index(args)
        dict1 = {}
        for i in eval(lastApi):
            dict1[i] = self.info[index].get(i)
        result = self.sendRequest.Post(url,self.body_headers(method,dict1,args)[0],self.body_headers(method,dict1,args)[1])
        return result
    # "RequestMatterList":[{"WorkTrayMalfunctionClassId":"102","IssueMalfunctionClassIdList":"156","Type":2,"ImageUrl":null,"ContentStr":""}]
    RequestMatterList = [{"WorkTrayMalfunctionClassId":"","IssueMalfunctionClassIdList":"","Type":2,"ImageUrl":None,"ContentStr":""}]

    def GetMalfunctionClass(self, url, method=None, thisApi=None, args=None, extract=None, lastApi=None):
        types = {"Type1": 2, "Type2": 1}
        for i in types:
            if types[i] == 2:
                thisApi = {"Type": 2}
                r = self.body_headers(method, thisApi, args)
                result = self.sendRequest.Post(url, r[0], r[1])
                extract = str(["MalfunctionClassId"])
                self.jsonparse(args, extract, result) #这里属于特殊处理方式   自己自定义存储的数据
            elif types[i] == 1:
                thisApi = {"Type": 1}
                r = self.body_headers(method, thisApi, args)
                result = self.sendRequest.Post(url, r[0], r[1])
                extract = ["MalfunctionClassId", "IssueMalfunctionClassId"]
                for i in extract:
                    jsonparse = parse("$..%s"%i)
                    get = 1
                    if i == "IssueMalfunctionClassId":
                        get = 3
                    par = [match.value for match in jsonparse.find(result)][:get]
                    if i == "MalfunctionClassId":  # str(par)[1:-1]的作用是 [156, 159, 161] 将变成 156, 159, 161 去掉括号
                        self.RequestMatterList[0]["WorkTrayMalfunctionClassId"] = str(par)[1:-1] #存储位置
                    if i == "IssueMalfunctionClassId":  # 如果 查询的是issue 则走这里
                        self.RequestMatterList[0]["IssueMalfunctionClassIdList"] = str(par)[1:-1]#存储issue

        return result

    def GetMalfunctionClass1(self, url, method=None, thisApi=None, args=None, extract=None, lastApi=None): #异常用例 输入type=3

        ret = self.body_headers(method[:-1],thisApi,args)
        result= self.sendRequest.Post(url,ret[0],ret[1])
        return result
    def SubmitMatter(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):
        try:
            index = self.index(args)
            dict1 = {}
            for i in eval(lastApi):
                dict1[i] = self.info[index].get(i) #取得位置id MalfunctionClassId
            dict1.update({"RequestMatterList":self.RequestMatterList}) #将事项类别与issue加入到字典中
            dict1.update(eval(thisApi)) #将本次接口需要的参数加入到字典中

            result = self.sendRequest.Post(url,self.body_headers(method,dict1,args)[0],self.body_headers(method,dict1,args)[1])
            self.jsonparse(args,extract,result) #提取本次相应的结果值

            return result
        except Exception as e:
            print(e)
    def SubmitMalfunction(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):
        index = self.index(args)
        dict1 = {}
        for i in eval(lastApi):
            dict1[i] = self.info[index].get(i)
        thisApi= eval(thisApi)
        thisApi.update(dict1)

        result = self.sendRequest.Post(url,self.body_headers(method,thisApi,args)[0],self.body_headers(method,thisApi,args)[1])
        return  result


    def GetMalfunctionBookDateList(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):
        try:

            result = self.sendRequest.Post(url,self.body_headers(method,thisApi,args)[0],self.body_headers(method,thisApi,args)[1])
            self.jsonparse(args=args,extract=extract,result=result)
            return result
        except Exception as e:
            print(e)
    def GetMalfunctionBookList(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):#预约跟进--根據日期獲取可预约列表
        try:
            index= self.index(args)
            dict1 = {}
            for i in eval(lastApi):
                dict1[i] = self.info[index].get(i)
            ret = self.body_headers(method,dict1,args)
            result = self.sendRequest.Post(url,ret[0],ret[1])
            self.jsonparse(args=args,extract=extract,result=result)
            return result
        except Exception as e:
            print(e)
    def GetMalfunctionList(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):
        ret = self.body_headers(method,thisApi,args)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        self.jsonparse(args,extract,result)
        return  result


    def SubmitMalfunctionBook(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):
        index = self.index(args)
        dict1 = {}
        for i in eval(lastApi):
            dict1[i] = self.info[index].get(i)
        dict1.update(eval(thisApi))
        ret = self.body_headers(method,dict1,args)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return result


    def GetMalfunctionBookSetting(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #MalfunctionBookId：bigint 唯一I 作用是获取预约唯一id 用于取消
        print("extract",extract)
        index = self.index(args)
        dict1 = {}
        for i in eval(lastApi):
            dict1[i] = self.info[index].get(i)

        ret = self.body_headers(method,dict1,args)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        self.jsonparse(args,extract,result)
        return result
    def CancelMalfunctionBook(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):
        index = self.index(args)
        dict1 = {}

        for i in eval(lastApi):
            dict1[i]= self.info[index].get(i)
        ret = self.body_headers(method,dict1,args)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return result


    def GetMalfunctionDetails(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):
        index = self.index(args)
        dict1 = {}
        for i in eval(lastApi):
            dict1[i] = self.info[index].get(i)

        ret =  self.body_headers(method,dict1,args)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return result


    def GetNoticeClassList(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #獲取通告分類
        try:
            ret = self.body_headers(method, thisApi, args)
            result = self.sendRequest.Post(url,ret[0],ret[1])
            self.jsonparse(args,extract,result)
            return  result
        except Exception as e:
            print(e)

    def GetNoticeListByClassId(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): # 獲取通告列表
        index = self.index(args)
        dict1 = {}
        try:
            for i in eval(lastApi):
                dict1[i] = self.info[index].get(i)
            thisApi = eval(thisApi)
            thisApi.update(dict1)
            ret = self.body_headers(method, thisApi, args)
            result = self.sendRequest.Post(url, ret[0], ret[1])
            self.jsonparse(args, extract, result)  # 只使用单条数据响应
            return result
        except Exception as e:
            print(e)



    def evalLastApi(self,args=None,lastApi=None): #写一个公共处理方法 用于处理获取到上一个接口提取下来的数据
        index = self.index(args)
        dict1 = {}
        try:
            for i in eval(lastApi):
                dict1[i] = self.info[index].get(i)

            return dict1
        except Exception as e:
            print(e)

    def GetNoticeContent(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #獲取通告內容

        dict1 = self.evalLastApi(args,lastApi)
        ret = self.body_headers(method,dict1,args)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return result

    def LikeNotice(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):
        dict1 = self.evalLastApi(args,lastApi)
        ret = self.body_headers(method,dict1,args)
        result = self.sendRequest.Post(url, ret[0], ret[1])
        return result

    def GetContactInfoList(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): # 獲取設置信息
        headers = super(API,self).headers(method)
        body = super(API,self).body(method)
        result = self.sendRequest.Post(url,body,headers)
        return result


    def GetSettingInfo(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #获取联络我们
        headers = super(API,self).headers(method)
        body = super(API,self).body(method)
        result = self.sendRequest.Post(url,body,headers)
        return  result

    def SendMail(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):#发送邮件
        headers = super(API,self).headers(method)
        body = super(API,self).body(method,thisApi)
        result = self.sendRequest.Post(url, body, headers)
        return result

    def GetOtherInfo(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #获取相关信息
        headers = super(API,self).headers(method)
        body = super(API,self).body(method,thisApi)
        result = self.sendRequest.Post(url, body, headers)
        return result


    def GetInboxMsgList(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #获取消息中心的数据
        ret = self.body_headers(method,thisApi,args)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        self.jsonparse(args,extract,result)
        return  result
    def OperateInboxMsg(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #删除消息中心的头一条数据

        dict1 = self.evalLastApi(args,lastApi)
        thisApi = eval(thisApi)
        dict2 = {"InboxMsgIdList":dict1["InboxMsgId"]}
        thisApi.update(dict2)
        ret = self.body_headers(method,thisApi,args)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return result

    def GetWebUrl(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #获取业主委员会网址
        ret = self.body_headers(method,thisApi,args)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return result

    def SendEmailForNotice(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #通告发送电邮
        try:
            dict1 = self.evalLastApi(args,lastApi)
            thisApi = eval(thisApi)
            thisApi.update(dict1)
            ret = self.body_headers(method,thisApi,args)
            result = self.sendRequest.Post(url,ret[0],ret[1])
            return result
        except Exception as e:
            print(e)
    def GetFacilityNameList(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #获取会所列表 注意这里只获取可预订的id 不可预约的过滤掉
        ret = self.body_headers(method,thisApi,args)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        jsonparse = parse("$..NeedBook")
        NeedBookStatus = [match.value for match in jsonparse.find(result)] #获取所有的可预订状态
        getIndex = NeedBookStatus.index(True) #只取NeedBook == True的会所  默认取第一条 可自由配置
        jsonparse = parse("$..%s"%extract) #再次匹配响应的结果 这次根据获取的下标 取会所id 因为一个id对应一个下标
        FacilityId = [match.value for match in jsonparse.find(result)][getIndex]

        index = self.index(args) #获取当前用户的下标
        self.info[index]["FacilityId"] = FacilityId
        print(self.info)
        return  result

    def GetFacilityDetails(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #获取某个设施的详情
        dict1 = self.evalLastApi(args,lastApi)
        ret = self.body_headers(method,dict1,args)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return result

    def GetAvaliableSessionsByDate(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #获取预约时间段
        dict1 = self.evalLastApi(args,lastApi)
        thisApi = eval(thisApi)
        thisApi.update(dict1)
        ret = self.body_headers(method,thisApi,args)
        result =self.sendRequest.Post(url,ret[0],ret[1])
        jsonparse = parse("$..BookType")
        ret = [match.value for match in jsonparse.find(result)] #获取所有可预订 不可预订的时段
        BookType = 0 #0表示可预订 其余状态表示不可预订
        position = []
        for i in range(0,len(ret)):
            if ret[i] == BookType: #判断当前状态是否等于 0
                position.append(i) #获取到可预订时段的下标
        jsonparse = parse("$..%s"%extract)
        list1 = [match.value for match in jsonparse.find(result)] #默认获取所有的已预约 不可预约的时段
        BookCodeList = [] #设定一个可预约时段的空列表
        j = 0
        for i in list1:
            BookCodeList.append(list1[position[j]]) #通过位置下标 将 可预约时段筛选出来 上面的列表存储的都是可预约的时段下标
            j += 1
            if j >= len(position):
                break

        str1 = "" #定义一个空字符串 用于拼接
        BookCodeList =(BookCodeList[:2]) #：BookCodeList=2018/10/5 7:30:00|2018/10/5 8:30:00|3|0,2018/10/5 8:30:00|2018/10/5 9:30:00|3|1 按照这种格式拼接

        for i in BookCodeList: #这里要拼接 不能用切割的方法 用切割产生的效果是字符串嵌套字符串
            str1 += i +","
        index = self.index(args)
        self.info[index]["BookCodeList"] = str1[:-1] #存放在本地
        print("BookCodeList",BookCodeList)
        return result
    def BookFacility(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #会所预定 作用提交预定
        dict1 = self.evalLastApi(args,lastApi)
        thisApi =eval(thisApi)
        thisApi.update(dict1)
        ret = self.body_headers(method,thisApi,args)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return result

    def GetBookStatusList(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None): #调用会所预定记录的接口 作用:获取已预订的设施ID 预定的单号BookId
        ret = self.body_headers(method,thisApi,args)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        Status = 1
        jsonparse = parse("$..Status")
        ret = [match.value for match in jsonparse.find(result)]
        position = [] #存放可取消预定的记录 下标
        for i in range(0,len(ret)):
            if ret[i] == Status:
                position.append(i)
        index = self.index(args)
        try:
            for i in eval(extract):
                jsonparse = parse("$..%s"%i)
                ret = [match.value for match in jsonparse.find(result)][position[0]] #默认第一个
                self.info[index][i]=ret #写入对应的账号字典里面
        except Exception as e:
            print(e)
      #  return self.info
        return result
    def CancelBooking(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):
        dict1 = self.evalLastApi(args,lastApi)
        ret= self.body_headers(method,dict1,args)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return  result

    def EditUserAvatar(self,url,method=None,thisApi=None,args=None,extract=None,lastApi=None):
        file1 = "H:\cardApp\config\\745.jpg"

        header = self.headers(method)
        form1 =  """
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <soap:Body>
    <EditUserAvatar xmlns="http://tempuri.org/">
        """
        index = self.index(args)
        form2 = """
        <JsonData>{"MasterSecret": "CTGi*7d54Fs*eruieud545Jgsdudb===Yhdt6", "AppEstateId": "6124F8B9618591FA", "Version": "1.0.0", 
        "DeviceInfo": "Redmi Note 4|7.0|WIFI|1.0.0|AArch64 Processor rev 4 (aarch64)", "ClientType": "2", "Language": 2, 
        "Location": "N/A", "RegistrationID": "170976fa8aa40eb997d", "HandoverHouseRecordId": 0, 
        "UserToken": %s, 
        "UserId": 21,"Type":2,"CurrentFileName":"test.jpg"}</JsonData>"""%json.dumps(self.info[index]["UserToken"])

        form3 = """
                 </EditUserAvatar>
        </soap:Body>
        </soap:Envelope>
        """

        img = "<currentFileBytes>"+base64.b64encode(open(file1,'rb').read()).decode()+"</currentFileBytes>"

        body = form1+form2+img+form3

        result = self.sendRequest.Post(url,body,header)
        return result
if __name__ =="__main__":
    t = API()



    #print(t.GetUserLoginInfo('{"UserName":"T2525"}'))
    #
    # t.method = "UserLogin"
    # print(t.UserLogin())
    #t.LostLoginPassword()








