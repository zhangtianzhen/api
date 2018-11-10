import base64
import re
import json
import os
import hashlib
from jsonpath_rw import jsonpath,parse
import  time
import copy
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
            if type(thisApi) == str:
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


    def joinTeamByhandle(self,method=None,need=None,thisApi=None,key=None,add1=None): #人工填写id方式邀请入队

        if type(thisApi) == str:
            thisApi = eval(thisApi)
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(ret[0],ret[1])

        return result




    def getTeamUplist1(self, method=None, need=None, thisApi=None, key=None, add1=None):  # 获取组队ID

        self.longin1(method="UserLogin", thisApi=key)

        if type(thisApi) == str:
            thisApi = eval(thisApi)
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(ret[0], ret[1])
        for i in result["ResultData"]["TeamUpListEntity"]:
            if i["TeamUpType"] == 3:  # 这里的FromUserId 不能写死
                return i["TeamUpItemEntity"][0]["TeamUpAgreeStateId"]

    def getTeamUplist2(self, method=None, need=None, thisApi=None, key=None, add1=None):  # 获取组队ID

        self.longin1(method="UserLogin", thisApi=key)

        if type(thisApi) == str:
            thisApi = eval(thisApi)
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(ret[0], ret[1])
        print(json.dumps(result,indent=2))
        return {"StateCode":1001,"StateMsg":"成功","ResultType":1}



    def confirmJoin(self,method=None, need=None, thisApi=None, key=None, add1=None): #接受组队邀请并入队
        TeamUpAgreeStateId = None
        if type(need) == str and need !=None:
            need = self.decompression(need)
            TeamUpAgreeStateId = self.getTeamUplist1(**need[0])
        elif type(need) == dict and need !=None:
            TeamUpAgreeStateId = self.getTeamUplist1(need)
        if type(thisApi) == str:
            thisApi = eval(thisApi)
        if TeamUpAgreeStateId !=None:
            thisApi.update({"TeamUpAgreeStateId":TeamUpAgreeStateId})

        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(ret[0],ret[1])

        return result


    def GetMyTeamInfo(self,method=None, need=None, thisApi=None, key=None, add1=None):
        """退出隊伍第一步"""
        self.longin1(method="UserLogin", thisApi=key)
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(ret[0],ret[1])
        return result["ResultData"]["TeamId"]

    def teamRetreat(self,method=None, need=None, thisApi=None, key=None, add1=None): #退出队伍第二步
        need = self.decompression(need)
        TeamId=self.GetMyTeamInfo(**need[0])
        ret = self.body_headers(method,{"TeamId":TeamId})
        result = self.sendRequest.Post(ret[0],ret[1])
        return result



    def ConfirmJoinForManay(self, method=None,need=None, thisApi=None, key=None, add1=None):

        info = {"TeamName":"接口发出的组队邀请","ToUserMessage":"APItest","ToUserId":""}
        GetTeamUpList = {"page": 1, "CurrentServerTime": "2015-08-01T00:00:00"}
        agree = {"AgreeState":1}
        ToUserId,UserNames  = eval(key)["ToUserId"],eval(key)["UserName"]
        list1 = []
        for i in UserNames:
            a = copy.deepcopy(info)
            list1.append(a)

        for i in range(len(list1)):
            list1[i]["ToUserId"]=ToUserId[i]
        flag = 1
        tokens = []
        js = 0
        start = 0
        finall = None
        while start <= len(UserNames)-1:

            newStart = start
            end = 0
            while end<10:
                self.longin1(method="UserLogin", thisApi=thisApi)
                ret = self.joinTeamByhandle(method="TeamInvite", thisApi=list1[newStart])["ResultData"]["ResultType"]  # 發送组队申请
                if flag == 1: #当邀请人是单身时
                    if ret == 1: #成功接收到组队邀请，进入被邀请人同意并加入队伍阶段
                        ret = self.getTeamUplist1(method="GetTeamUpList",thisApi=GetTeamUpList,key={"UserName":UserNames[js],"password":"a123456"}) #获取组队id
                        agree.update({"TeamUpAgreeStateId":ret})
                        compleJoin = self.confirmJoin(method="TeamUpStateOperation",thisApi=agree) #加入队伍
                        if compleJoin['ResultData'].get("ResultType") == 1:  # 如果加入了队伍
                            t = copy.deepcopy(self.info)
                            tokens.append(t)  # 添加一个用户信息 用于邀请用户加入队伍时候使用
                            flag += 1
                            newStart += 1  # 邀请下一个人

                elif flag != 1: #当邀请人非单身时 须进过家属同意才能发出邀请
                        init = 0
                        for i in tokens:
                            i.update({"page": 1, "CurrentServerTime": "2015-08-01T00:00:00"})
                            bodys = super(API, self).body("GetTeamUpList", i)
                            headers = super(API, self).headers("GetTeamUpList")
                            result = self.sendRequest.Post(bodys, headers)
                            r1 = result["ResultData"]["TeamUpListEntity"][0]
                            for m in r1["TeamUpItemEntity"]:
                                if m["ToUserId"] == i["UserId"]:
                                    TeamUpAgreeStateId=m["TeamUpAgreeStateId"]
                                    agreed = {"AgreeState":1}
                                    agreed.update({"TeamUpAgreeStateId":TeamUpAgreeStateId}) #将邀请id加入到本次接口请求中
                                    agreed.update(i)
                                    body = super(API, self).body("TeamUpStateOperation", agreed)
                                    headers = super(API, self).headers("TeamUpStateOperation")
                                    compleJoin = self.sendRequest.Post(body, headers)
                                    #compleJoin = self.confirmJoin(method="TeamUpStateOperation", thisApi=agree)  # 加入队伍
                                    if compleJoin["ResultData"]["ResultType"] == 1:
                                        print("同意队友的邀请入队申请")
                            init += 1
                        if init == len(tokens):
                            break #结束本次循环
                end += 1

            #进入被邀请人业务流程

            ret1 = self.longin1(method="UserLogin", thisApi={"UserName":UserNames[newStart],"password":"a123456"})
            UserToken1,UserId1 = ret1["ResultData"]["UserToken"],ret1["ResultData"]["UserId"]
            info1 = {"UserToken":UserToken1,"UserId":UserId1}

            info1.update({"page": 1, "CurrentServerTime": "2015-08-01T00:00:00"})

            body = super(API, self).body("GetTeamUpList", info1)
            headers = super(API, self).headers("GetTeamUpList")
            result = self.sendRequest.Post(body, headers)
            for i in result["ResultData"]["TeamUpListEntity"]:
                for j in i["TeamUpItemEntity"]:
                    if j["ToUserId"] == UserId1:
                        TeamUpAgreeStateId = j["TeamUpAgreeStateId"]
                        info1.update({"AgreeState":1})
                        info1.update({"TeamUpAgreeStateId":TeamUpAgreeStateId})
                        compleJoin = self.confirmJoin(method="TeamUpStateOperation", thisApi=info1)
                        if compleJoin["ResultData"]["ResultType"] == 1:
                            tokens.append({"UserToken":UserToken1,"UserId":UserId1})
                            finall = compleJoin

            start+=1

        return finall

    def TeamApply(self, method=None, need=None, thisApi=None, key=None, add1=None):  # 申请入队 (1)
        ret = self.body_headers("TeamApply", thisApi=thisApi)
        result = self.sendRequest.Post(ret[0], ret[1])  # 发送申请入队
        if result["ResultData"]["ResultType"] == 1:
            return "ok"
        return None

    def TeamUpStateOperation(self, method=None, need=None, thisApi=None, key=None, add1=None):  # 获取申请入队的用户id(2)
        num, toUserId = len(key), add1
        parameter = {"page": 1, "CurrentServerTime": "2015-08-01T00:00:00"}
        parameter.update(self.info)  # 加入用户token,userid
        body = super(API, self).body(method="GetTeamUpList", dict1=parameter)
        header = super(API, self).headers(method="GetTeamUpList")
        result = self.sendRequest.Post(body, header)  # 获取申请入队信息
        get = result["ResultData"]["TeamUpListEntity"]
        statusId = []
        for i in get:
            listNum = len(i["TeamUpItemEntity"])  # 获取当前队员数量
            for jc in i["TeamUpItemEntity"]:
                if (jc["AgreeState"] == 0):
                    pass
                elif (jc["AgreeState"] in [1, 2]):  # 如果该入队申请请求有被操作
                    listNum -= 1  # 则减少
            if listNum == len(i["TeamUpItemEntity"]):  # 如果该申请入队请求状态为0 且没减少
                for jc in range(0, len(i["TeamUpItemEntity"])):
                    if (i["TeamUpItemEntity"][jc]["AgreeState"] == 0) and (
                    i["TeamUpItemEntity"][jc]["ToUserId"]) == add1:  # 申请记录未操作且发送给的申请人是当前toUserid
                        #print(i["TeamUpItemEntity"][jc]["TeamUpAgreeStateId"])
                        statusId.append(i["TeamUpItemEntity"][jc]["TeamUpAgreeStateId"])
        return statusId
    def applyTeam(self, method=None, need=None, thisApi=None, key=None, add1=None):  # 多人加入队伍(3)
        teamName, toUserId = ["c1@3202.com", "c2@3202.com"], [43, 44]
        key = eval(key)
        UserName, UserId = key["UserName"], key['UserId']
        count = 0  # 用于统计发送申请入队成功的人数
        for i in UserName:
            self.longin1(method="UserLogin", thisApi={"UserName": i, "password": "a123456"})  # 登录 获取到用户token,userid
            Parameter = {"ToUserId": toUserId[0], "ToUserMessage": str(i) + "发送的入队申请"}  # 添加接口需要的参数
            self.info.update(Parameter)  # 将参数放入这次请求中
            result = self.TeamApply(thisApi=self.info)  # 发送的组队申请的相应接口不为None 则申请成功
            if result != None:
                count += 1
        TeamUpAgreeStateId =[]
        for i in range(len(toUserId)):
            self.longin1(method="UserLogin",thisApi={"UserName": teamName[i], "password": "a123456"})  # 登录 获取到用户token,userid
            result = self.TeamUpStateOperation(key=UserId[:count], add1=toUserId[i])  # 调用该方法 获取申请入队信息
            TeamUpAgreeStateId.append(result)

        for i in range(len(toUserId)):
            self.longin1(method="UserLogin", thisApi={"UserName": teamName[i], "password": "a123456"})
            for id in TeamUpAgreeStateId[i]:
                ret = self.body_headers(method=method,thisApi={"TeamUpAgreeStateId":id,"AgreeState":1})
                result = self.sendRequest.Post(ret[0],ret[1])

        return result