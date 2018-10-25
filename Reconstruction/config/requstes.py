import base64
import re
import json
import os
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
        result = self.sendRequest.Post(url,body,header)["ResultData"]
        for i in ["UserName","Salt"]:
            self.md5[i] =result[i]
        self.HashedValue = self.md5Function(self.md5["Salt"],self.md5["UserName"], password)
        #print(self.md5)

    def longin1(self,url=None,method=None,thisApi=None,add1=None,add2=None):
        thisApi = eval(thisApi)
        self.GetUserLoginInfo(thisApi)  # 生成哈希值
        UserName = {"Username":self.md5.get("UserName")}
        HashedValue = {"HashedValue":self.HashedValue}
        thisApi.update(UserName)
        thisApi.update(HashedValue)

        header = super(API,self).headers(method)
        body = super(API,self).body(method,thisApi)
        result = self.sendRequest.Post(url,body,header)

        for i in ["UserToken","UserId"]:
            self.info[i] = result["ResultData"][i]
        return result
        #return result["StateList"]
    def token_userid(self):  # 封装 公共的提取 usertoken的方法
        dict1 = {}
        for i in ["UserToken","UserId"]:
            dict1[i] = self.info[i] #结合用例时 需要切换到self.info
        return dict1

    def body_headers(self,method=None,thisApi=None,add1=None,add2=None): #封装 公共的 获取请求头 与 请求体的方法
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

    def getCurretn(self,url=None,method=None,thisApi=None,add1=None,add2=None): #获取当前信息 独立用例
        ret = self.body_headers(method)

        result = self.sendRequest.Post(url,ret[0],ret[1])

        #return result["StateList"]
        return result

    def editPassword(self,url=None,method=None,thisApi=None,add1=None,add2=None): #修改密码 独立用例
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        #return result["StateList"]
        return result
    def editUserinfo(self,url=None,method=None,thisApi=None,add1=None,add2=None):#修改个人信息 独立用例
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        #return result["ResultData"]["ResultType"]
        return result
    def findPassword(self,url=None,method=None,thisApi=None,add1=None,add2=None):#忘记密码 #独立用例
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        #return result["ResultData"]["ResultType"]
        return result
    def editPhoto(self, url=None,method=None,thisApi=None,add1=None,add2=None): #独立用例
        file1 = "E:\\api5\Reconstruction\config\\text.jpg"

        header = self.headers(method)
        form1 = """
       <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
       <soap:Body>
       <EditUserAvatar xmlns="http://tempuri.org/">
           """

        form2 = """
           <JsonData>{"MasterSecret": "CTGi*7d54Fs*eruieud545Jgsdudb===Yhdt6", "AppEstateId": "6124F8B9618591FA", "Version": "1.0.0", 
           "DeviceInfo": "Redmi Note 4|7.0|WIFI|1.0.0|AArch64 Processor rev 4 (aarch64)", "ClientType": "2", "Language": 2, 
           "Location": "N/A", "RegistrationID": "170976fa8aa40eb997d", "HandoverHouseRecordId": 0, 
           "UserToken": %s, 
           "UserId": %s,"Type":2,"CurrentFileName":"test.jpg"}</JsonData>"""%(json.dumps(self.info["UserToken"]),json.dumps(self.info["UserId"]))

        form3 = """
                    </EditUserAvatar>
           </soap:Body>
           </soap:Envelope>
           """

        img = "<currentFileBytes>" + base64.b64encode(open(file1, 'rb').read()).decode() + "</currentFileBytes>"

        body = form1 + form2 + img + form3

        result = self.sendRequest.Post(url, body, header)
        #return result["ResultData"]["ResultType"]
        return result
    def getTimeList(self, url=None,method=None,thisApi=None,add1=None,add2=None): #获取交楼预约列表 独立用例
        ret = self.body_headers(method)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return result
        #return result["ResultData"]["ResultType"]



    def getHouseList(self, url=None, method=None, thisApi=None, add1=None, add2=None): # 根据日期获取可预约信息 独立用例
        dict1 = self.getTimeList1() #先获取 时间列表
        ret = self.body_headers(method,dict1)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return result
        #return result["ResultData"]["ResultType"]


    def getTimeList1(self, url=None, method=None, thisApi=None, add1=None, add2=None):  # 获取交楼预约列表 有名额的日期 独立用例
        """
        取消三步骤之一
        :param url: 
        :param method: 
        :param thisApi: 
        :param add1: 
        :param add2: 
        :return: 
        """""

        method = "GetHandoverHouseDateList"
        url = "http://altomobile.test.cn-cic.com/CardAppService.svc"
        ret = self.body_headers(method)
        result = self.sendRequest.Post(url, ret[0], ret[1])["ResultData"]["HandoverHouseDateList"]
        dict1 = {"HandoverHouseDate": ""}
        for i in result:
            if i["CanBookQuantity"]:
                dict1["HandoverHouseDate"] = i["HandoverHouseDate"]  # 默认获取最近的
                break
        return dict1



    def getHouseList1(self, url=None, method=None, thisApi=None, add1=None, add2=None): # 获取提交预约时需要的HandoverHouseId
        method = "GetHandoverHouseList"
        url = "http://altomobile.test.cn-cic.com/CardAppService.svc"
        dict1 = self.getTimeList1() #先获取 时间列表
        ret = self.body_headers(method,dict1)
        result = self.sendRequest.Post(url,ret[0],ret[1])["ResultData"]
        return  {"HandoverHouseId":result["HandoverHouseList"][0]["HandoverHouseId"]} #返回id



    def getHouse(self,url=None, method=None, thisApi=None, add1=None, add2=None):#提交预约
        dict1 = self.getHouseList1()
        thisApi = eval(thisApi)
        thisApi.update(dict1)
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        #return result["ResultData"]["ResultType"]
        return result
    def HouseSetting(self,url=None, method=None, thisApi=None, add1=None, add2=None): #独立用例 获取当前用户有没有交楼

        dict1 = self.getTimeList1()
        dict1.update({"Version":"1.0.1"})
        ret = self.body_headers(method,dict1)
        result =self.sendRequest.Post(url,ret[0],ret[1])
        if result["ResultData"]["IsBooked"] == False:
            print("这个单位还未预约")
        else:
            print("该单位已预约")

        #return result["StateList"]
        return result
    def HouseSetting1(self,url=None, method=None, thisApi=None, add1=None, add2=None): #获取到已预约后的 用于取消预约的 获取id：HandoverHouseRecordId 取消三步骤之二
        """"
        取消三步骤之二
        """""
        method = "GetHandoverHouseSetting"
        url = "http://altomobile.test.cn-cic.com/CardAppService.svc"
        dict1 = self.getTimeList1()
        dict1.update({"Version":"1.0.1"})
        ret = self.body_headers(method,dict1)
        result =self.sendRequest.Post(url,ret[0],ret[1])


        result = self.jsonpase("HandoverHouseRecordId",result)
        return {"HandoverHouseRecordId":result[0]} #返回已获取的id 用于取消

    def cancelHouse(self,url=None, method=None, thisApi=None, add1=None, add2=None):#取消交楼预约  取消三步骤之三
        dict1 = self.HouseSetting1() #获取到已经交楼的HandoverHouseRecordId
        ret = self.body_headers(method,dict1)
        result = self.sendRequest.Post(url,ret[0],ret[1])

        #return result["ResultData"]["ResultType"]
        return result
    def getClass(self,url=None, method=None, thisApi=None, add1=None, add2=None): #获取事项类别独立用例
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return result
        #return result["StateList"]
    def getPosition(self,url=None, method=None, thisApi=None, add1=None, add2=None): #获取事项位置 独立用例
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(url, ret[0], ret[1])
        #return result["StateList"]
        return result
    def List_of_events(self,url=None, method=None, thisApi=None, add1=None, add2=None): #获取事项列表 独立用例

        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        #return result["StateList"]

        return result

    def submitMatter(self, url=None, method=None, thisApi=None, add1=None, add2=None):  # 保存事项 独立用例
        dict1 = self.getClassAndPostion()
        thisApi = eval(thisApi)
        add1 = eval(add1)
        add2 = eval(add2)
        add1["MalfunctionClassId"] = dict1[0]["MalfunctionClassId"]
        thisApi[0]["WorkTrayMalfunctionClassId"] = dict1[1]["WorkTrayMalfunctionClassId"]
        thisApi[0]["IssueMalfunctionClassIdList"] = dict1[2]["IssueMalfunctionClassId"]
        RequestMatterList = {"RequestMatterList": thisApi}
        list1 = [add1, add2]
        for i in list1:
            RequestMatterList.update(i)
        ret = self.body_headers(method, RequestMatterList)
        result = self.sendRequest.Post(url, ret[0], ret[1])
        #return result["ResultData"]["ResultType"]
        return result
    def getClassAndPostion(self,url=None, method=None, thisApi=None, add1=None, add2=None): #给保存事项用例保存好事项
        url="http://altomobile.test.cn-cic.com/CardAppService.svc"
        method = "GetMalfunctionClass"
        WorkTrayMalfunctionClassId={} #事项类别
        IssueMalfunctionClassIdList = {} #issue列表
        MalfunctionClassId = {} #事项位置
        for i in range(1,3):
            ret = self.body_headers(method,{"Type":i})
            result = self.sendRequest.Post(url,ret[0],ret[1])
            if i == 1:  # 先获取事项类别与issue
                for j in ["MalfunctionClassId", "IssueMalfunctionClassId"]:
                    if j == "MalfunctionClassId":

                        WorkTrayMalfunctionClassId["WorkTrayMalfunctionClassId"] = self.jsonpase(j, result["ResultData"])[0]
                    elif j == "IssueMalfunctionClassId":
                        IssueMalfunctionClassIdList["IssueMalfunctionClassId"] = str(self.jsonpase(j,result)[:5])[1:-1]
            if i == 2: #获取位置
                MalfunctionClassId["MalfunctionClassId"] = self.jsonpase("MalfunctionClassId",result)[0]

        return [MalfunctionClassId,WorkTrayMalfunctionClassId,IssueMalfunctionClassIdList]

    #RequestMatterList = [{"WorkTrayMalfunctionClassId":"","IssueMalfunctionClassIdList":"","Type":2,"ImageUrl":None,"ContentStr":""}]

    def submitMatter1(self,url=None, method=None, thisApi=None, add1=None, add2=None): #保存事项 提供给提交事项
        dict1 = self.getClassAndPostion()
        thisApi = [{"WorkTrayMalfunctionClassId":"","IssueMalfunctionClassIdList":"","Type":2,"ImageUrl":None,"ContentStr":"接口一条龙之提交文本内容"}]
        add1 = {"MalfunctionClassId":""}
        add2 = {"Version":"1.0.1"}
        add1["MalfunctionClassId"] = dict1[0]["MalfunctionClassId"]
        thisApi[0]["WorkTrayMalfunctionClassId"] =dict1[1]["WorkTrayMalfunctionClassId"]
        thisApi[0]["IssueMalfunctionClassIdList"] = dict1[2]["IssueMalfunctionClassId"]
        RequestMatterList = {"RequestMatterList":thisApi}
        method,url = "SubmitMatter","http://altomobile.test.cn-cic.com/CardAppService.svc"
        list1 = [add1,add2]
        for i in list1:
            RequestMatterList.update(i)
        ret = self.body_headers(method,RequestMatterList)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return result["ResultData"]["ResultType"]


    def List_of_events1(self,url=None, method=None, thisApi=None, add1=None, add2=None): #获取事项列表未提交的事项的id 用于提交事项单
        self.submitMatter1()
        method = "GetMalfunctionList"
        url = "http://altomobile.test.cn-cic.com/CardAppService.svc"
        dict1 = {"CurrentServerTime": "2015-08-01T00:00:00", "page": 1}
        ret = self.body_headers(method, dict1)
        result = self.sendRequest.Post(url, ret[0], ret[1])
        for i in range(0,len(result["ResultData"])):

            if result["ResultData"][i].get("Status") == 0: #当订单状态为0时候 表示未提交
                dict1 = {}
                if result["ResultData"][i].get("MalfunctionId"):
                    dict1["MalfunctionId"] = result["ResultData"][i].get("MalfunctionId")
                    break #默认获取一条就停止查找
        return dict1 #给完成交楼的方法 返回待提交的id

    def completeHandle(self,url=None, method=None, thisApi=None, add1=None, add2=None): #完成交楼
        thisApi = eval(thisApi)

        if thisApi["SubmitKey"] == 1: #这里执行提交钥匙的方法
            MalfunctionId = self.List_of_events1()
            thisApi.update(MalfunctionId)

        elif thisApi["SubmitKey"] == 2: #进行预约日期进行交楼的时候
            MalfunctionId = self.List_of_events2()
            thisApi.update(MalfunctionId)
            # ret = self.body_headers(method, thisApi)
            # result = self.sendRequest.Post(url, ret[0], ret[1])
            # return result["ResultData"]["ResultType"]
        ret = self.body_headers(method, thisApi)
        result = self.sendRequest.Post(url, ret[0], ret[1])
        #return result["ResultData"]["ResultType"]
        return result
    def getlistOftime(self,url=None, method=None, thisApi=None, add1=None, add2=None):#获取执漏预约时间列表 独立用例
        ret = self.body_headers(method)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        #return result["StateList"]
        return result
    def getlistOfBook(self, url=None, method=None, thisApi=None, add1=None, add2=None):  # 根据具体日期获取到可预约列表信息 独立用例
        dict1 = self.getlistOftime1()
        ret = self.body_headers(method, dict1)
        result = self.sendRequest.Post(url, ret[0], ret[1])

        #return result["StateList"]
        return result
    def getlistOftime1(self,url=None, method=None, thisApi=None, add1=None, add2=None):#获取执漏预约时间列表 预约日期用例组成部分第一步
        method,url = "GetMalfunctionBookDateList","http://altomobile.test.cn-cic.com/CardAppService.svc"
        ret = self.body_headers(method)
        result = self.sendRequest.Post(url,ret[0],ret[1])["ResultData"]
        dict1 = {}

        for i in range(0,len(result["MalfunctionBookDateList"])):

            if result["MalfunctionBookDateList"][i]["CanBookQuantity"]:#如果可预约人数大于0 则默认选第一个
                dict1["BookDate"] = result["MalfunctionBookDateList"][i]["BookDate"]
                return dict1

    def getlistOfBook1(self,url=None, method=None, thisApi=None, add1=None, add2=None):#获取执漏预约时间列表 预约日期用例组成部分第二步
        """"
        获取:MalfunctionBookDateId
        """""
        method, url = "GetMalfunctionBookList", "http://altomobile.test.cn-cic.com/CardAppService.svc"
        dict1 = self.getlistOftime1()
        ret = self.body_headers(method, dict1)
        result = self.sendRequest.Post(url, ret[0], ret[1])
        dict1 ={}

        for i in result["ResultData"]["MalfunctionBookDateList"]:
            if i["CanBookQuantity"]:#查找还有预约名额的进行报名
                dict1["MalfunctionBookDateId"] = i["MalfunctionBookDateId"]
                return dict1

    def submitFordate(self,url=None, method=None, thisApi=None, add1=None, add2=None):#获取执漏预约时间列表 预约日期用例组成部分第三步
        #  根据日期提交预约
        MalfunctionId = self.List_of_events1()
        MalfunctionBookDateId = self.getlistOfBook1()
        thisApi = eval(thisApi)
        for i in [MalfunctionId,MalfunctionBookDateId]:
            thisApi.update(i)
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(url,ret[0],ret[1])

        #return  result["ResultData"]["ResultType"]
        return result

    def getBookSetting(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """"
        获取预约执漏单详情
        """""
        dict1 = self.List_of_events2()
        ret = self.body_headers(method, dict1)
        result = self.sendRequest.Post(url, ret[0], ret[1])

        return result



    def submitFordate1(self,url=None, method=None, thisApi=None, add1=None, add2=None):#获取执漏预约时间列表 预约日期用例组成部分第三步
        #  根据日期提交预约
        MalfunctionId = self.List_of_events1()
        MalfunctionBookDateId = self.getlistOfBook2()
        thisApi = eval(thisApi)
        for i in [MalfunctionId,MalfunctionBookDateId]:
            thisApi.update(i)
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(url,ret[0],ret[1])

        #return  result["ResultData"]["ResultType"]
        return result

    def getlistOfBook2(self,url=None, method=None, thisApi=None, add1=None, add2=None):#获取执漏预约时间列表 预约日期用例组成部分第二步
        """"
        获取:MalfunctionBookDateId
        """""
        method, url = "GetMalfunctionBookList", "http://altomobile.test.cn-cic.com/CardAppService.svc"
        dict1 = self.getlistOftime1()
        ret = self.body_headers(method, dict1)
        result = self.sendRequest.Post(url, ret[0], ret[1])
        dict1 ={}

        for i in result["ResultData"]["MalfunctionBookDateList"]:
            if i["CanBookQuantity"]:#查找还有预约名额的进行报名
                dict1["MalfunctionBookDateId"] = i["MalfunctionBookDateId"]
                return dict1

    def getlistOftime2(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """"
        该方法功能 用于实现 查找到不可取消的天数
        """""
        method, url = "GetMalfunctionBookDateList", "http://altomobile.test.cn-cic.com/CardAppService.svc"
        ret = self.body_headers(method)
        result = self.sendRequest.Post(url, ret[0], ret[1])["ResultData"]
        dict1 = {}
        flag = 0
        for i in range(0, len(result["MalfunctionBookDateList"])):
            if flag == self.getBookSetting1(): #add1 这里代指不在取消范围内的天数
                break
            if result["MalfunctionBookDateList"][i]["CanBookQuantity"]:  # 如果可预约人数大于0 则默认选第一个
                dict1["BookDate"] = result["MalfunctionBookDateList"][i]["BookDate"]
                flag += 1

        return dict1



    def getBookSetting1(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """"
        获取预约执漏单详情
        """""
        method,url = "GetMalfunctionBookSetting","http://altomobile.test.cn-cic.com/CardAppService.svc"
        dict1 = self.List_of_events2()
        ret = self.body_headers(method, dict1)
        result = self.sendRequest.Post(url, ret[0], ret[1])

        return result["ResultData"]["CancelBook"] #返回取消日期
    def List_of_events2(self,url=None, method=None, thisApi=None, add1=None, add2=None): #获取事项列表未提交的事项的id 用于提交事项单
        """"
              获取 MalfunctionId
               取消三部曲之一
        """""
        method = "GetMalfunctionList"
        url = "http://altomobile.test.cn-cic.com/CardAppService.svc"
        dict1 = {"CurrentServerTime": "2015-08-01T00:00:00", "page": 1}
        ret = self.body_headers(method, dict1)
        result = self.sendRequest.Post(url, ret[0], ret[1])
        for i in range(0,len(result["ResultData"])):

            if result["ResultData"][i].get("Status") == 0: #当订单状态为0时候 表示未提交
                dict1 = {}
                if result["ResultData"][i].get("MalfunctionId"):
                    dict1["MalfunctionId"] = result["ResultData"][i].get("MalfunctionId")
                    break #默认获取一条就停止查找
        return dict1 #给完成交楼的方法 返回待提交的id


    def getDeatilsofTime(self,url=None, method=None, thisApi=None, add1=None, add2=None):
        """"
        获取MalfunctionBookId 用于取消 获取预约相关信息
        取消三步骤之二
        """""
        method,url = "GetMalfunctionBookSetting","http://altomobile.test.cn-cic.com/CardAppService.svc"
        dict1 = self.List_of_events2()
        ret = self.body_headers(method,dict1)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        if result["ResultData"]["MalfunctionBook"]["Status"] == 2: #只查找预约成功的
            dict1 = self.jsonpase("MalfunctionBookId",result)
            dict1={"MalfunctionBookId":dict1[0]}
            return dict1
        else:
            return None


    def cancelByDate(self,url=None, method=None, thisApi=None, add1=None, add2=None):
        """"
               获取MalfunctionBookId 取消已预约的执漏单
               取消三步骤之三
               """""

        dict1 = self.getDeatilsofTime()
        if dict1 ==None:
            return 4
        ret = self.body_headers(method,dict1)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        #return result["ResultData"]["ResultType"]
        return result



    def GetMalfunctionDetails(self,url=None, method=None, thisApi=None, add1=None, add2=None):
        """""
        获取执漏单详情 删除第二步
        """""
        method,url = "GetMalfunctionDetails","http://altomobile.test.cn-cic.com/CardAppService.svc"
        dict1 = self.List_of_events2()
        ret = self.body_headers(method,dict1)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        result = self.jsonpase("MatterId",result)
        length = len(result)
        get = 0
        if length > 3:
            get= length//2
            return {"MatterIdList":str(result[:get])[1:-1]}
        elif length == 1:
            #print(str(result[get])[1:-1])
            return {"MatterIdList":str(result[get])[1:-1]}
        elif length == 0:
            return 0
    def delet(self,url=None, method=None, thisApi=None, add1=None, add2=None):
        """""
               获取执漏单详情 删除第三步
               """""

        dict1 = self.GetMalfunctionDetails()
        if dict1 == None:
            return None
        ret = self.body_headers(method,dict1)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        #return result["ResultData"]["ResultType"]
        return result
    """
    获取会所设施 独立用例
    """
    def clubList(self,url=None, method=None, thisApi=None, add1=None, add2=None):
        ret = self.body_headers(method)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        #print(result)
        return result
    """
        获取会所设施 获取会所设施详细 第一步
        """

    def clubList1(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """"
        正向用例:获取需要预约的设施进行且不需要清洁时间的会所预约设施
        """""
        method,url = "GetFacilityNameList","http://altomobile.test.cn-cic.com/CardAppService.svc"
        ret = self.body_headers(method)
        result = self.sendRequest.Post(url, ret[0], ret[1])

        for i in result["ResultData"]:
            if i["NeedBook"] == True:
                if i["MaxUnitPerDay"] >0 :
                    if i["IsNeedClean"] == False:
                        dict1={}
                        dict1["FacilityId"] = i["FacilityId"] # 默认返回第一个 可以预约的
                        return dict1

    def clubDetails(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """"
                        获取会所详细设施情况
                                """""
        FacilityId =  self.clubList1()
        ret = self.body_headers(method,FacilityId)
        resullt = self.sendRequest.Post(url,ret[0],ret[1])
        print(resullt)
        return resullt


    def clubByDate(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """""
        获取根据日期获取预约时段的接口 且不需要清洁时间的   独立用例
        """""
        FacilityId =  self.clubList1()
        thisApi = eval(thisApi)
        thisApi.update(FacilityId)
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return result

    def clubDetails1(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """"
                        获取会所详细设施情况
                                """""
        FacilityId =  self.clubList1()
        ret = self.body_headers("GetFacilityDetails",FacilityId)
        resullt = self.sendRequest.Post(url,ret[0],ret[1])

        return resullt["ResultData"]["MaxUnitPerDay"] #返回每天最多预约次数


    def clubByDate1(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """""GetFacilityDetails
        获取根据日期获取预约时段的接口 且不需要清洁时间的 预约第一步
        """""

        add1 = eval(add1)
        method = add1["method"]
        thisApi = {"DateToSearch":add1["DateToSearch"]}
        FacilityId =  self.clubList1()
        maxGet = self.clubDetails1(url)#查看预约上限人数
        thisApi.update(FacilityId)
        ret = self.body_headers(method,thisApi)
        BookCode = []
        result = self.sendRequest.Post(url,ret[0],ret[1])
        try:
            if len(result["ResultData"]) > 0 and maxGet > 0: #获取预约天数不为大于0
                for i in result["ResultData"]:
                    if i["IsBooked"] == False and i["BookType"] == 0: #可预订 且未被预约

                        if i["IsSpecial"] == False:#不需要连续预定两节
                            if i["BookCode"] == 0 or i["BookCode"] == None or i ["BookCode"] == "":
                                return None
                            BookCode.append(i["BookCode"])
            else:
                print("预约名额或日期为空")
                return None
        except:
            return None
        BookCodeList = {}
        str1 = ""
        if len(BookCode) > 2:#如果可预约时间长度大于二 那么则连续预约两个时段\
            for i in range(0,maxGet):
                str1 += BookCode[i]+","
            BookCodeList["BookCodeList"] = str1[:-1]
        else:
            str1 = BookCode[0]
            BookCodeList["BookCodeList"]= str1

        return BookCodeList

    def getClub(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        print(add1)
        """"
        会所预定 第二步
        # """""
        # BookCodeList = self.clubByDate1(url,add1=add1)
        # FacilityId = self.clubList1()
        try:
            thisApi = eval(thisApi)
            for i in [self.clubByDate1(url,add1=add1),self.clubList1()]:
                thisApi.update(i)
            ret= self.body_headers(method,thisApi)
            result = self.sendRequest.Post(url,ret[0],ret[1])
            return result
        except:
            return None
    def clubrecord(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """"
        获取会所预定记录 用户取消预约 独立用例
        """""
        thisApi = eval(thisApi)
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return  result

    def clubrecord1(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """"
        获取会所预定记录 用户取消预约 第一步
        """""

        ret = self.body_headers("GetBookStatusList", {"CurrentServerTime": "2015-08-01T00:00:00", "page": 1})
        result = self.sendRequest.Post(url, ret[0], ret[1])
        dict1 = {"FacilityId": "", "BookId": ""}
        for i in result["ResultData"]:
            if i["Status"] == 1 and i["IsPaid"] == False:  # 未付款的记录
                for j in dict1:
                    dict1[j] = i[j]  # 默认获取最后一个

        return  dict1


    def cancelClub(self,url=None, method=None, thisApi=None, add1=None, add2=None):
        dict1 = self.clubrecord1(url=url)
        ret = self.body_headers(method,dict1)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return  result
    def getNoticeList(self,url=None, method=None, thisApi=None, add1=None, add2=None): #独立用例
        ret = self.body_headers(method)
        result= self.sendRequest.Post(url,ret[0],ret[1])

        return result
    def getNoticeById(self,url=None, method=None, thisApi=None, add1=None, add2=None):
        thisApi = eval(thisApi)
        dict1 = self.getNoticeList1(url=url)
        dict1.update(thisApi)
        ret = self.body_headers(method,dict1)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        return result

    def getNoticeList1(self,url=None, method=None, thisApi=None, add1=None, add2=None): #
        ret = self.body_headers("GetNoticeClassList")
        result= self.sendRequest.Post(url,ret[0],ret[1])
        for i in result["ResultData"]:
            if i["NoticeCounts"] != 0 :
                dict1 = {"NoticeClassId":i["NoticeClassId"]}
                return dict1

    def getNoticeById1(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """"
        获取通过内容 第二步
        """""
        thisApi = {"page":1,"CurrentServerTime":"2015-08-01T00:00:00"}
        dict1 = self.getNoticeList1(url=url)
        dict1.update(thisApi)
        ret = self.body_headers("GetNoticeListByClassId", dict1)
        result = self.sendRequest.Post(url, ret[0], ret[1])
        return {"NoticeId":result["ResultData"][0]["NoticeId"]}

    def getContent(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """"
        获取通告内容第三步
        """""
        dict1 = self.getNoticeById1(url=url)
        ret = self.body_headers(method,dict1)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        print(result)
        return result
    def likeNotice(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """""
        通过点赞
        """""
        dict1 = self.getNoticeById1(url=url)
        ret = self.body_headers(method,dict1)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        print(result)
        return result
    def aboatUs(self,url=None, method=None, thisApi=None, add1=None, add2=None):
        ret = self.body_headers(method)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        print(result)
        return result
    def getSetting(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        ret = self.body_headers(method)
        result = self.sendRequest.Post(url, ret[0], ret[1])
        print(result)
        return result
    def sendEmail(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        thisApi = eval(thisApi)
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        print(result)
        return result
    def getInboxList(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        thisApi = eval(thisApi)
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        print(result)
        return result

    def getInboxList1(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """"
        删除未读消息第一步 获取未读消息的id
        """""
        thisApi = {"AppType":1,"CurrentServerTime":"2015-08-01T00:00:00","page":1}
        method = "GetInboxMsgList"
        ret = self.body_headers(method,thisApi)
        result = self.sendRequest.Post(url,ret[0],ret[1])
        for i in result["ResultData"]:
            if i["IsRead"] == False:
                dict1 = {"InboxMsgIdList":i["InboxMsgId"]} #默认返回第一未读消息的 InboxMsgId
                return dict1

    def getInboxList2(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """"
        删除未读消息第一步 获取未读消息的id
        """""
        thisApi = {"AppType": 1, "CurrentServerTime": "2015-08-01T00:00:00", "page": 1}
        method = "GetInboxMsgList"
        ret = self.body_headers(method, thisApi)
        result = self.sendRequest.Post(url, ret[0], ret[1])
        for i in result["ResultData"]:
            if i["IsRead"] == True:
                dict1 = {"InboxMsgIdList": i["InboxMsgId"]}  # 默认返回第一未读消息的 InboxMsgId
                return dict1

    def deleteInBox(self, url=None, method=None, thisApi=None, add1=None, add2=None):
        """"
        删除未读消息 第二步
        """""
        try:
            dict1 = self.getInboxList2(url)

            thisApi = eval(thisApi)
            thisApi.update(dict1)

            ret = self.body_headers(method,thisApi)
            result = self.sendRequest.Post(url,ret[0],ret[1])
            print(result)
            return result
        except Exception as e:
            print("没有可删除的消息了",e)
    def readInBox(self, url=None, method=None, thisApi=None, add1=None, add2=None): #将未读消息变为已读消息
        try:
            dict1 = self.getInboxList1(url)
            thisApi = eval(thisApi)
            thisApi.update(dict1)

            ret = self.body_headers(method, thisApi)
            result = self.sendRequest.Post(url, ret[0], ret[1])
            print(result)
            return result
        except Exception as e:
            print("没有可删除的消息了", e)



if __name__ == "__main___":
    test = API()
    print(test.longin1())