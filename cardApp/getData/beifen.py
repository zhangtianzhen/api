import  re
import json
import requests
import xmltodict
import re
import hashlib
from DATA_BASE.readTEXT  import TextManage
from config.requestConfig import BaseConfig
url= "http://altomobile.test.cn-cic.com/CardAppService.svc"
txt = TextManage()
method = "GetUserLoginInfo"
data1 =  """
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <"""+method+""" xmlns="http://tempuri.org/"><JsonData>"""

data2 = {"MasterSecret":"CTGi*7d54Fs*eruieud545Jgsdudb===Yhdt6","AppEstateId":"6124F8B9618591FA",
         "Version":"1.0.0","DeviceInfo":"Redmi Note 4|7.0|WIFI网络|1.0.0|AArch64 Processor rev 4 (aarch64)",
         "ClientType":"2","Language":2,"UserName":"T2626"} #所需参数

data3 = """
</JsonData>
 </"""+method+""">
  </soap:Body>
</soap:Envelope>
"""
data2 = json.dumps(data2,ensure_ascii=False) #将字典转换成字符串

data = data1+data2+data3
header ={
    "SOAPAction":"http://tempuri.org/ICardAppService/GetUserLoginInfo",
    "Accept":"application/json,text/javascript,*/*",
    "Content-Type":"text/xml"
}

rs = BaseConfig(method)
body = rs.body()
header = rs.Header("GetUserLoginInfo")

res = requests.post(url,data=body.encode('utf-8'),headers=header)
r = re.search(r"\{.*\}", res.text)
print(r.group())
hansleValue = ""
ret = (json.loads(r.group()))#将str类型转换成字典类型
apiMessage = {"test01":"{xxxxx}"} #以{用例Id:接口返回信息方法组成文本内容} 先写死 用于调试 后期用变量替代
resultCode = ret["StateList"][0]["StateCode"]
resultStr = ret["StateList"][0]["StateMsg"]
if resultCode == 1001 and resultStr=="成功":
        apiMessage["test01"] = ret["ResultData"]
        sava = txt.writeText("test01",apiMessage)
        # print(sava)
        #username  = ret["ResultData"]["UserName"]
        username = txt.readText()["UserName"]
        #salt = ret["ResultData"]["Salt"]
        salt = txt.readText()["Salt"] #读取文本里面的数据
        password = "a123456"
        #MD5 加密规则:salt:username:password
        ecode = salt+":"+username+":"+password
       # print("加密前的规则:\t",ecode)
        md5 = hashlib.md5()
        md5.update(ecode.encode(encoding='utf-8')) #加密的后的密码 需要大写
        code = md5.hexdigest()
        code = code.upper() #转换成大写的
        hansleValue = code
        print(hansleValue)
        txt.writeText("test01",hansleValue)

method = "UserLogin"
rs = BaseConfig(method)
bodys = rs.body("HashedValue")
head = rs.Header("UserLogin")

res = requests.post(url,data=bodys.encode("utf-8"),headers=head)
print(res.text)
