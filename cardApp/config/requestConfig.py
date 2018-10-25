"""
配置基本的请求头数据 可动态添加 方便进行配置
"""
import json
from DATA_BASE.readTEXT import TextManage
import hashlib
MasterSecret = "CTGi*7d54Fs*eruieud545Jgsdudb===Yhdt6"
AppEstateId =  "6124F8B9618591FA"
Version = "1.0.0"
DeviceInfo = "Redmi Note 4|7.0|WIFI网络|1.0.0|AArch64 Processor rev 4 (aarch64)"
ClientType = "2"
Language = 2
UserName = "T2626"
Location="N/A"
RegistrationID  = "170976fa8aa40eb997d"
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

    method = ""
    def __init__(self):
        pass

    def Header(self,*args): #此处必须传要调用的接口方法
        self.header = {
            "SOAPAction": "http://tempuri.org/ICardAppService/" + self.method,
            "Accept": "application/json,text/javascript,*/*",
            "Content-Type": "text/xml;charset=UTF-8"
        }
        return self.header
    def form1(self,*args):

        self.data1 = """
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <soap:Body>
        <""" + self.method + """ xmlns="http://tempuri.org/"><JsonData>"""
        return self.data1

    def form2(self,dict1=None):
        #print("dict1",dict1)
        self.data = {
            "MasterSecret":getMasterSecret(),"AppEstateId":getAppEstateId(),"Version":getVersion(),
            "DeviceInfo":getDeviceInfo(),"ClientType":getClientType(),"Language":getLanguage(),
            "Location":getLocation(),"RegistrationID":getRegistrationID()
        }
        if dict1:

            self.data.update(dict1)

            return json.dumps(self.data)

        else:
            print("test1")
            return json.dumps(self.data)

    def form3(self,*args):


        self.data2 = """
    </JsonData>
        </"""+self.method+""">
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

    def body(self,method=None):
        try:
            if method:
                return self.form1()+self.form2(method)+self.form3()
            else:
                return self.form1()+self.form2()+self.form3()
        except Exception as e:
            print("基本配置模块报错>>>>>",e)

if __name__ =="__main__":
    t = BaseConfig()
    t.method="LoginInfo"
    #print(t.body())
    # form1 = t.form1()
    # form2 = t.form2()
    # form3 = t.form3()
    # print(form1+form2+form3)

    print(t.form2({"UserName":"T2626"}))




















#
# method = "GetUserLoginInfo"
# data1 =  """
# <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
#   <soap:Body>
#     <"""+method+""" xmlns="http://tempuri.org/"><JsonData>"""
#
# data2 = {"MasterSecret":"CTGi*7d54Fs*eruieud545Jgsdudb===Yhdt6","AppEstateId":"6124F8B9618591FA",
#          "Version":"1.0.0","DeviceInfo":"Redmi Note 4|7.0|WIFI网络|1.0.0|AArch64 Processor rev 4 (aarch64)",
#          "ClientType":"2","Language":2,"UserName":"T2626"} #所需参数
#
# data3 = """
# </JsonData>
#  </"""+method+""">
#   </soap:Body>
# </soap:Envelope>
# """
#
# header ={
#     "SOAPAction":"http://tempuri.org/ICardAppService/GetUserLoginInfo",
#     "Accept":"application/json,text/javascript,*/*",
#     "Content-Type":"text/xml"
# }
