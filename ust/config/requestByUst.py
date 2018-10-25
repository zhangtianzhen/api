import base64
import re
import json
import os
import hashlib
import time
from jsonpath_rw import jsonpath,parse
import datetime
MasterSecret = "CTGi*7d54Fs*eruieud545Jgsdudb===Yhdt6"
AppEstateId =  "D4305C7C4CC3597C"
Version = "1.0.0"
DeviceInfo = "Redmi Note 4|7.0|WIFI网络|1.0.0|AArch64 Processor rev 4 (aarch64)"
ClientType = "2"
Language = 2
UserName = "T2626"
Location="N/A"
RegistrationID  = "1a0018970af37efb44f"

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
        dict1 = {}
        for i in ["UserToken","UserId"]:
            dict1[i] = self.info[i] #结合用例时 需要切换到self.info
        return dict1

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

    def register(self,method=None,thisApi=None,need = None,key=None,add1=None):
        """"
        新用户注册
        """""
        thisApi = eval(thisApi)

        ret = self.body(method,thisApi)

        headers = self.headers(method)
        result = self.sendRequest.Post(ret,headers)
        return  {"StateCode":1001,"StateMsg":"成功"}


    def getCurretn(self,method=None,thisApi=None,need = None,key=None,add1=None): #获取当前信息 独立用例
        ret = self.body_headers(method)
        result = self.sendRequest.Post(ret[0],ret[1])
        return result

    def activateEmail(self,method=None,thisApi=None,need = None,key=None,add1=None): #激活邮箱
        thisApi = eval(thisApi)

        ret = self.body_headers(method,thisApi)

        result =self.sendRequest.Post(ret[0],ret[1])
        return result

    def editPassword(self,method=None,thisApi=None,need = None,key=None,add1=None): #修改密码 独立用例
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(ret[0],ret[1])
        return result

    def GetVerificationCode(self,method=None,thisApi=None,need = None,key=None,add1=None): #获取验证码
        thisApi = eval(thisApi)
        body = super(API, self).body(method, thisApi)
        header = self.headers(method)
        result = self.sendRequest.Post(body, header)
        return result

    def useVerificationCode(self,method=None,thisApi=None,need = None,key=None,add1=None):#使用验证码
        thisApi = eval(thisApi)
        body = super(API,self).body(method,thisApi)
        header = self.headers(method)
        result = self.sendRequest.Post(body,header)
        return result

    def forgetThePassword(self,method=None,thisApi=None,need = None,key=None,add1=None): #重置密码
        thisApi = eval(thisApi)
        body = super(API, self).body(method, thisApi)
        header = self.headers(method)
        result = self.sendRequest.Post(body, header)
        return result

    def UploadPictures1(self,method=None,thisApi=None,need = None,key=None,add1=None):
        """"
        上传图片 返回地址 与self.updateInfo 耦合
        """""
        file1 = "H:\\ust\\config\\text.jpg"
        need = eval(need)
        header = self.headers(need["UploadPictures1"]["method"])
        form1 = """
               <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
               <soap:Body>
               <%s xmlns="http://tempuri.org/">
                   """%need["UploadPictures1"]["method"]

        form2 = """
                   <JsonData>{"MasterSecret": "CTGi*7d54Fs*eruieud545Jgsdudb===Yhdt6", "AppEstateId": "D4305C7C4CC3597C", "Version": "1.0.0", 
                   "DeviceInfo": "Redmi Note 4|7.0|WIFI|1.0.0|AArch64 Processor rev 4 (aarch64)", "ClientType": "2", "Language": 2, 
                   "Location": "N/A", "RegistrationID": "1a0018970af37efb44f", "HandoverHouseRecordId": 0, 
                   "UserToken": %s, 
                   "UserId": %s,"Type":2,"CurrentFileName":"test.jpg"}</JsonData>""" % (
        json.dumps(self.info["UserToken"]), json.dumps(self.info["UserId"]))

        form3 = """
                            </%s>
                   </soap:Body>
                   </soap:Envelope>
                   """%need["UploadPictures1"]["method"]

        img = "<currentFileBytes>" + base64.b64encode(open(file1, 'rb').read()).decode() + "</currentFileBytes>"

        body = form1 + form2 + img + form3

        result = self.sendRequest.Post(body, header)
        return result["ResultData"]["FileUrl"] #返回地址
    def updateInfo(self,method=None,thisApi=None,need = None,key=None,add1=None): #修改个人信息

        UsersAvatar = self.UploadPictures1(need=need)
        thisApi = eval(thisApi)
        fileUrl = {"UsersAvatar":UsersAvatar}
        thisApi.update(fileUrl) #放入图片地址
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(ret[0],ret[1])
        return result

    def getCheckList(self,method=None,thisApi=None,need = None,key=None,add1=None): #查看当前时间列表

        try:
            localTime = time.strftime('%Y-%m-%d 00:00:00') #获取当前时间
            thisApi = eval(thisApi)
            SearchDate = thisApi["SearchDate"] #处理输入的时间
            if localTime == SearchDate: #这个方法功能主要实现的是查看当前时间 如果需要查看之前的时间 需要重新写一个方法
                pass
            else:
                thisApi["SearchDate"] = localTime
            ret = self.body_headers(method,thisApi)
            result = self.sendRequest.Post(ret[0],ret[1])
            print(result)
            return result
        except Exception as e:
            print('getCheckList',e)

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
    def getCheckList1(self, method=None, thisApi=None, need=None, key=None, add1=None):  # 查看当前时间列表
        """
        查找未被done的活动
        """""

        try:
            localTime = time.strftime('%Y-%m-%d 00:00:00')  # 获取当前时间
            if type(thisApi) == dict or type(thisApi) == list : #判断输入的参数类型
                pass
            else:
                thisApi = eval(thisApi)
            if type(key) == dict or type(key) == list :
                pass
            else:
                key = eval(key)
            SearchDate = thisApi["SearchDate"]  # 接口客户端发来的时间
            if localTime == SearchDate:  # 这个方法功能主要实现的是查看当前时间 如果需要查看之前的时间 需要重新写一个方法
                pass
            else:
                thisApi["SearchDate"] = localTime
            ret = self.body_headers(method, thisApi)
            result = self.sendRequest.Post(ret[0], ret[1])
            num = []
            for i in result["ResultData"]:
                if i["RegistrationCheck"][0]["Done"] == False:
                    num.append(i["RegistrationCheck"][0]["RegistrationCheckId"])
            if len(num) != 0:
                return {"RegistrationCheckId":num[0]}
            else:
                return None
        except Exception as e:
            print('getCheckList', e)

    def getCheckList2(self, method=None, thisApi=None, need=None, key=None, add1=None):  # 查看当前时间列表
        """
        查找已被done的活动
        """""

        try:
            localTime = time.strftime('%Y-%m-%d 00:00:00')  # 获取当前时间
            if type(thisApi) == dict or type(thisApi) == list:  # 判断输入的参数类型
                pass
            else:
                thisApi = eval(thisApi)
            if type(key) == dict or type(key) == list:
                pass
            else:
                key = eval(key)
            SearchDate = thisApi["SearchDate"]  # 接口客户端发来的时间
            if localTime == SearchDate:  # 这个方法功能主要实现的是查看当前时间 如果需要查看之前的时间 需要重新写一个方法
                pass
            else:
                thisApi["SearchDate"] = localTime
            ret = self.body_headers(method, thisApi)
            result = self.sendRequest.Post(ret[0], ret[1])
            num = []
            for i in result["ResultData"]:
                if i["RegistrationCheck"][0]["Done"] == True:
                    num.append(i["RegistrationCheck"][0]["RegistrationCheckId"])
            if len(num) != 0:
                return {"RegistrationCheckId": num[0]}
            else:
                return None
        except Exception as e:
            print('getCheckList', e)

    def getCheckDetails(self,method=None,thisApi=None,need = None,key=None,add1=None):

        at = self.decompression(need) #
        get = self.getCheckList1(**at[0])
        ret = self.body_headers(method,get)
        result = self.sendRequest.Post(ret[0],ret[1])

        return result


    def completeDone(self,method=None,thisApi=None,need = None,key=None,add1=None): #注册列表 完成

        """to do /done 按钮变成 done"""""
        try:
            at = self.decompression(need)  #
            get = self.getCheckList1(**at[0])
            ret = self.body_headers(method, get)
            result = self.sendRequest.Post(ret[0], ret[1])
            return result
        except Exception as e:
            print(e)


    def completeCacncel(self,method=None,thisApi=None,need = None,key=None,add1=None):
        """to do /done 按钮变成 to do"""""
        try:
            at = self.decompression(need)  #
            get = self.getCheckList2(**at[0])
            ret = self.body_headers(method, get)
            result = self.sendRequest.Post(ret[0], ret[1])
            return result
        except Exception as e:
            return e
    def getActivityList(self,method=None,thisApi=None,need = None,key=None,add1=None):
        """获取活动列表"""""
        try:
            thisApi = eval(thisApi)
            ret = self.body_headers(method,thisApi)
            print(ret)
            result = self.sendRequest.Post(ret[0],ret[1])
            return result

        except Exception as e:
            return e

    def getActivityListByTheme(self,method=None,thisApi=None,need = None,key=None,add1=None):
        """获取活动列表 按照Theme返回"""""
        try:
            thisApi = eval(thisApi)
            ret = self.body_headers(method,thisApi)
            result = self.sendRequest.Post(ret[0],ret[1])
            for i in result["ResultData"]:
                if i != thisApi["Theme"]:
                    return {"StateCode":1003,"StateMsg":"参数取值错误返回的数据包含Them%d以外的数据"%thisApi["Theme"]}
            return result

        except Exception as e:
            return e

    def getActivityList1(self, method=None, thisApi=None, need=None, key=None, add1=None):
        """查看详情"""""
        try:

            ret = self.body_headers(method, thisApi)
            result = self.sendRequest.Post(ret[0], ret[1])
            id1,id2=[],[]
            for i in result["ResultData"]:
                if i["CanRegWaitingListQuota"] >0 :
                    for j in i["ActivityTimeslot"]: #查看排队报名的名额
                        if  j["Quota"] >0 and j ["WaitingListQuota"]>0:
                            id1.append(i["ActivityManagementId"])
                            id2.append(j["ActivityTimeslotId"])

            if len(id1) != 0:
                return {'ActivityManagementId':id1[0],"ActivityTimeslotId":id2[0]}
            else:
                return {"StateCode":1111,"StateMsg":"查找失败"}
        except Exception as e:
            return e




    def getActivityDetails(self, method=None, thisApi=None, need=None, key=None, add1=None):
        """"获取活动详情"""""
        try:
            at = self.decompression(need)
            get = self.getActivityList1(**at[0])
            ret =self.body_headers(method,get)
            result = self.sendRequest.Post(ret[0],ret[1])
            return result
        except Exception as e:
            return e

    def getActivityList2(self, method=None, thisApi=None, need=None, key=None, add1=None):
        """查看详情"""""
        try:

            ret = self.body_headers(method, thisApi)
            result = self.sendRequest.Post(ret[0], ret[1])
            id1,id2=[],[]
            for i in result["ResultData"]:
                if i["CanRegWaitingListQuota"] >0 :
                    for j in i["ActivityTimeslot"]: #查看排队报名的名额
                        if  j["Quota"] >0 and j ["WaitingListQuota"]>0:
                            id1.append(i["ActivityManagementId"])
                            id2.append(j["ActivityTimeslotId"])

            if len(id1) != 0:
                return {'ActivityManagementId':id1[0],"ActivityTimeslotId":id2[0]}
            else:
                return {"StateCode":1111,"StateMsg":"查找失败"}
        except Exception as e:
            return e

    def CheckActivityTimeslot(self,method=None, thisApi=None, need=None, key=None, add1=None):
        """"注册报名第一步之检测时段状况"""""

        method1,thisApi1 = need[0]["method"],need[0]["thisApi"]
        method2, thisApi2 = need[1]["method"],need[1]["thisApi"]

        ret = self.body_headers(method1, thisApi1)
        result = self.sendRequest.Post(ret[0], ret[1])

        dict1,list1 = {},[]
        for i in result["ResultData"]:
            if i["CanRegWaitingListQuota"] > 0:
                for j in i["ActivityTimeslot"]:  # 查看排队报名的名额
                    if j["Quota"] > 0 and j["WaitingListQuota"] > 0:
                        dict1 = {'ActivityManagementId': i["ActivityManagementId"],
                                 "ActivityTimeslotId": j["ActivityTimeslotId"]}
                        list1.append(dict1)

        a = datetime.date.today()
        a1 = str(a).replace("-", "/") + " 00:00:00"
        thisApi2["BookDate"] = a1

        ji = 0

        while True:
            flag = ji
            while ji <= len(list1) :
                thisApi2.update(list1[flag])   #先查找第一个id在所有时间时间段内可报名日期
                ret = self.body_headers(method2,thisApi2)
                result = self.sendRequest.Post(ret[0],ret[1])
                if result["ResultData"]["ResultType"]  == 1: #如果第一个id 在日期范围内未报名的 则 找到 并退出
                    return [thisApi2]
                else:
                    ji += 1
                    d = a + datetime.timedelta(days=ji) #如果当前时间不满足报名条件 则查找明天的
                    thisApi2["BookDate"] = str(d).replace("-", "/") + " 00:00:00"
            ji = 0
    def getRegActivity(self, method=None, thisApi=None, need=None, key=None, add1=None):

        """"注册报名第二步"""""
        at = self.decompression(need)
        get=self.CheckActivityTimeslot(need=at)

        ret = self.body_headers(method,get[0])
        result = self.sendRequest.Post(ret[0],ret[1])
        return  result

    def getRegActivityList(self, method=None, thisApi=None, need=None, key=None, add1=None):  # 获取活动报名列表
        thisApi = eval(thisApi)
        ret = self.body_headers(method, thisApi)
        result = self.sendRequest.Post(ret[0], ret[1])
        return result

    def getRegActivityList1(self, method=None, thisApi=None, need=None, key=None, add1=None):#获取活动报名列表
        """"取消活动报名第一步 获取可取消的id"""""

        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(ret[0],ret[1])
        localTime = time.strftime('%Y-%m-%dT%H:00:00')  # 获取当前时间
        localTime = localTime.split("T")
        for i in result["ResultData"]:
            if i["Status"] == 1:
                st = i["StartTime"].split("T")
                if st[0] >= localTime[0]: #如果当前天数大于等于 则说明有效
                    if localTime[1] <= st[0]: #如果本地实际未超过 预约的开始时间 说明可以取消
                        return {"ActivityManagementRegId":i["ActivityManagementRegId"]} #默认获取第一个


    def cancelRegActivity(self, method=None, thisApi=None, need=None, key=None, add1=None):#取消活动报名第二步

        need = self.decompression(need)
        ActivityManagementRegId = self.getRegActivityList1(**need[0])
        ret = self.body_headers(method,ActivityManagementRegId)
        result = self.sendRequest.Post(ret[0],ret[1])
        return result

    def getGitList(self, method=None, thisApi=None, need=None, key=None, add1=None):#获取礼物列表
        thisApi = eval(thisApi)
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(ret[0],ret[1])
        return result

    def getGitList1(self):
        method = "GetRedemptionList"
        thisApi = {"page":1,"CurrentServerTime":"2015-08-01T00:00:00"}
        ret = self.body_headers(method, thisApi)
        result = self.sendRequest.Post(ret[0], ret[1])
        for i in result["ResultData"]:
            return {"RedemptionId":i["RedemptionId"]}



    def getGitDetails(self, method=None, thisApi=None, need=None, key=None, add1=None): #获取礼物详情
        RedemptionId = self.getGitList1()
        ret = self.body_headers(method,RedemptionId)
        result = self.sendRequest.Post(ret[0],ret[1])
        return result


    def beforeGetCheckList(self, method=None, thisApi=None, need=None, key=None, add1=None): #获取过去时间的活动列表
        thisApi = eval(thisApi)
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(ret[0],ret[1])
        print(result)
        return result


    def CheckActivityTimeslot1(self, method=None, thisApi=None, need=None, key=None, add1=None): #同一天注册两场活动

        method1,thisApi1 = need[0]["method"],need[0]["thisApi"]
        method2, thisApi2 = need[1]["method"],need[1]["thisApi"]
        ret = self.body_headers(method1,thisApi1)
        result = self.sendRequest.Post(ret[0],ret[1])
        dict1, list1 = {}, []
        list2 = [] #存放同一时段
        for i in result["ResultData"]:
            if i["CanRegWaitingListQuota"] > 0:
                if len(i["ActivityTimeslot"])>1: #当天可报名的时段 大于1
                    jc = 0
                    for j in i["ActivityTimeslot"]:  # 查看排队报名的名额
                        if j["Quota"] > 0 and j["WaitingListQuota"] > 0: #统计时段可预约名额
                                jc += 1
                    if jc > 1: #如果选择的时段 有两个及以上 有名额的时段 则加入列表
                        for j in i["ActivityTimeslot"]:
                            dict1 = {'ActivityManagementId': i["ActivityManagementId"],
                                     "ActivityTimeslotId": j["ActivityTimeslotId"]}
                            list2.append(dict1)
                        list1.append(list2)
        localTime = time.strftime("%Y/%m/%d 00:00:00")
        inputTime = thisApi2["BookDate"].split("00:00:00")[0] #获取输入的时间 判断输入的天数是不是过往时间
        if inputTime > localTime.split("00:00:00")[0]:
            pass
        else: #如果是过往时间 则 修改为当天
            thisApi2["BookDate"] = localTime

        a = datetime.date.today()
        a1 = str(a).replace("-", "/") + " 00:00:00"
        thisApi2["BookDate"] = a1

        ji = 0
        flash = None
        while True:
            flag,ag= ji,None
            c = 0
            conti = None
            for i in list1: #查找列表里面的报名时段
                ag = i
                while ji <= len(i):
                    c += 1
                    thisApi2.update(i[ji])  # 先顺序查找id在所有时间时间段内可报名日期
                    ret = self.body_headers(method2, thisApi2)
                    result = self.sendRequest.Post(ret[0], ret[1])
                    if result["ResultData"]["ResultType"] == 1:  # 如果未报名 则 找到 并退出
                        method = "RegActivity"
                        ret = self.body_headers(method,thisApi2)
                        self.sendRequest.Post(ret[0],ret[1])
                        flash= i[flag + 1]
                        # if ji  == 0 : #第一个时段刚刚被预约，那么 预约下一个时段早已被预约或未被预约
                        #     flash= i[flag + 1]#获取到当前时段的下一个时段
                        # else: #说明 刚刚预约之前的时段 早已被预约 那么返回早已被预约的时段 (这段逻辑 暂且无用)
                        #     flash= i[flag - 1] #获取当前时间的上一个时段
                        for i in flash: #将参数内容进行修改 修改为当天另一个时段的
                            thisApi2[i] =flash[i]
                        break
                        # ret = self.body_headers(method2, thisApi2)
                        # result = self.sendRequest.Post(ret[0], ret[1])
                        # if result["ResultData"]["ResultType"] !=1: #如果当天其他时段 调用接口返回的不是1 那么 说明当天已有时段被预约
                        #     break
                        # else:
                        #     conti=True
                        #     break
                    else:
                        ji += 1
                        d = a + datetime.timedelta(days=ji)  # 如果当前时间不满足报名条件 则查找明天的 以此类推
                        thisApi2["BookDate"] = str(d).replace("-", "/") + " 00:00:00"
                # if conti: #如果临近时段也是
                #     continue

                ji = 0
            if flash or c >= len(list1[ag]) :
                break
        return thisApi2
    def doubleRegActivity(self, method=None, thisApi=None, need=None, key=None, add1=None):
        need = self.decompression(need)
        dict1 = self.CheckActivityTimeslot1(need=need)
        ret = self.body_headers(method,dict1)
        result = self.sendRequest.Post(ret[0],ret[1])
        return result

    def CheckActivityTimeslot2(self, method=None, thisApi=None, need=None, key=None, add1=None): #
        method1, thisApi1 = need[0]["method"], need[0]["thisApi"]
        method2, thisApi2 = need[1]["method"], need[1]["thisApi"]
        ret = self.body_headers(method1, thisApi1)
        result = self.sendRequest.Post(ret[0], ret[1])
        dict1, list1 = {}, []

        for i in result["ResultData"]:
            if i["CanRegWaitingListQuota"] > 0:
                for j in i["ActivityTimeslot"]:  # 查看排队报名的名额
                    if j["Quota"] > 0 and j["WaitingListQuota"] > 0:
                        dict1 = {'ActivityManagementId': i["ActivityManagementId"],
                                 "ActivityTimeslotId": j["ActivityTimeslotId"],"StartTime":j["StartTime"],"EndTime":j["EndTime"]}
                        list1.append(dict1)
        localTime = time.strftime("%Y/%m/%d 00:00:00")
        inputTime = thisApi2["BookDate"].split("00:00:00")[0]  # 获取输入的时间 判断输入的天数是不是过往时间
        if inputTime > localTime.split("00:00:00")[0]:
            pass
        else:  # 如果是过往时间 则 修改为当天
            thisApi2["BookDate"] = localTime
        ji = 0
        a = datetime.date.today()
        a1 = str(a).replace("-", "/") + " 00:00:00"
        thisApi2["BookDate"] = a1
        flash = None
        while True:
            flag = ji
            while ji <= len(list1):
                thisApi2.update(list1[ji])  # 先查找第一个id在所有时间时间段内可报名日期
                ret = self.body_headers(method2, thisApi2)
                result = self.sendRequest.Post(ret[0], ret[1])
                if result["ResultData"]["ResultType"] == 1:  # 如果第一个id 在日期范围内未报名的 则 找到 并退出
                    method = "RegActivity"
                    ret = self.body_headers(method, thisApi2)
                    result = self.sendRequest.Post(ret[0], ret[1])
                    flash = True
                    break
                else:
                    ji += 1
                    d = a + datetime.timedelta(days=ji)  # 如果当前时间不满足报名条件 则查找明天的
                    thisApi2["BookDate"] = str(d).replace("-", "/") + " 00:00:00"
            if flash:
                break
            ji = 0

        ActivityManagementId=thisApi2["ActivityManagementId"] #通过ActivityManagementId 筛选不是本活动的 其实 CheckActivityTimeslot1也可以通过id进行做判断
        startTime,endTime = thisApi2["StartTime"],thisApi2["EndTime"]
        startTime,endTime = startTime.split("T")[1],endTime.split("T")[1]
        times = None
        for i in list1:
            if i["ActivityManagementId"] != ActivityManagementId:
                sTime,eTime=i["StartTime"].split("T")[1],i["EndTime"].split("T")[1]
                if sTime == startTime and endTime == eTime :
                    times = i
                    break
                elif sTime < startTime and eTime < endTime:
                    times = i
                    break
                elif sTime > startTime and sTime< endTime and eTime < endTime:
                    times = i
                    break
                elif sTime > startTime and sTime< endTime and eTime > endTime:
                    times = i
                    break
                elif sTime < startTime and eTime > endTime:
                    times = i
                    break
        for j in times:
            thisApi2[j] = times[j]
        return thisApi2
    def sameRegActivity(self, method=None, thisApi=None, need=None, key=None, add1=None): #报名与之冲突的时段
        need = self.decompression(need)
        dict1 = self.CheckActivityTimeslot2(need=need)
        ret = self.body_headers(method,dict1)
        result = self.sendRequest.Post(ret[0],ret[1])
        return  result
        #return {"StateCode":1001,"StateMsg":"成功","ResultType":4}



    def CheckActivityTimeslot3(self, method=None, thisApi=None, need=None, key=None, add1=None):
        method1, thisApi1 = need[0]["method"], need[0]["thisApi"]
        method2, thisApi2 = need[1]["method"], need[1]["thisApi"]
        ret = self.body_headers(method1, thisApi1)
        result = self.sendRequest.Post(ret[0], ret[1])
        dict1, list1 = {}, []

        for i in result["ResultData"]:
            if i["CanRegWaitingListQuota"] > 0:
                for j in i["ActivityTimeslot"]:  # 查看排队报名的名额
                    if j["Quota"] > 0 and j["WaitingListQuota"] > 0:
                        dict1 = {'ActivityManagementId': i["ActivityManagementId"],
                                 "ActivityTimeslotId": j["ActivityTimeslotId"], "StartTime": j["StartTime"],
                                 "EndTime": j["EndTime"]}
                        list1.append(dict1)
        info = list1[0]
        info.update(thisApi2)
        return info
    def beforeGetCheckList1(self, method=None, thisApi=None, need=None, key=None, add1=None): #报名过去的时段
        need = self.decompression(need)
        dict1 = self.CheckActivityTimeslot3(need=need)
        ret = self.body_headers(method,dict1)
        result = self.sendRequest.Post(ret[0],ret[1])
        return  result
        #return {"StateCode":1001,"StateMsg":"成功","ResultType":3}

    def CheckActivityTimeslot4(self, method=None, thisApi=None, need=None, key=None, add1=None):
        method1, thisApi1 = need[0]["method"], need[0]["thisApi"]
        method2, thisApi2 = need[1]["method"], need[1]["thisApi"]
        ret = self.body_headers(method1, thisApi1)
        result = self.sendRequest.Post(ret[0], ret[1])
        dict1, list1 = {}, []
        for i in result["ResultData"]:
            for j in i["ActivityTimeslot"]:  # 查看排队报名的名额
                    dict1 = {'ActivityManagementId': i["ActivityManagementId"],
                             "ActivityTimeslotId": j["ActivityTimeslotId"], "StartTime": j["StartTime"],
                             "EndTime": j["EndTime"]}
                    list1.append(dict1)
        ji = 0
        a = datetime.date.today()
        a1 = str(a).replace("-", "/") + " 00:00:00"
        thisApi2["BookDate"] = a1
        flash,thisApi3 = None,None
        while True:
            while ji < len(list1):
                thisApi2.update(list1[ji])  # 先查找第一个id在所有时间时间段内可报名日期
                ret = self.body_headers(method2, thisApi2)
                result = self.sendRequest.Post(ret[0], ret[1])

                if result["ResultData"]["CanRegQuota"] == 0 or result["ResultData"]["CanRegQuota"] < 0:  # 如果第一个id 在日期范围内未报名的 则 找到 并退出
                    return thisApi2
                    flash =True
                    break
                else:
                    ji += 1
                    d = a + datetime.timedelta(days=ji)  # 如果当前时间不满足报名条件 则查找明天的
                    thisApi2["BookDate"] = str(d).replace("-", "/") + " 00:00:00"
            if flash:
                break
            ji = 0

    def fullRegActivity(self, method=None, thisApi=None, need=None, key=None, add1=None): #报名 名额不足的活动
        need = self.decompression(need)
        dict1 = self.CheckActivityTimeslot4(need = need)
        ret = self.body_headers(method,dict1)
        result = self.sendRequest.Post(ret[0],ret[1])
        return result
        #return {"StateCode":1001,"StateMsg":"成功","ResultType":4}

    def register1(self, method=None, thisApi=None, need=None, key=None, add1=None): #多用户注册
        thisApi = eval(thisApi)

        for i in range(102,151):
            EmailAccount={"EmailAccount":"hk%d"%i+"@3202.com"}
            thisApi.update(EmailAccount)
            ret = self.body_headers(method,thisApi)
            print("正在注册%s" % EmailAccount["EmailAccount"])
            self.sendRequest.Post(ret[0],ret[1])
        return {"StateCode":1001,"StateMsg":"成功"}
