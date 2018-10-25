import  re
import json
import requests
import xmltodict
import re
import hashlib
from DATA_BASE.readTEXT  import TextManage
from config.requestConfig import BaseConfig
from jsonpath_rw import parse,jsonpath
url= "http://altomobile.test.cn-cic.com/CardAppService.svc"
txt = TextManage()


rs = BaseConfig("GetUserLoginInfo")
body = rs.body()

header = rs.Header("GetUserLoginInfo")

res = requests.post(url,data=body.encode('utf-8'),headers=header)
r = re.search(r"\{.*\}", res.text)

ret = (json.loads(r.group()))#将str类型转换成字典类型

apiMessage = {"test01":"{xxxxx}"} #以{用例Id:接口返回信息方法组成文本内容} 先写死 用于调试 后期用变量替代
resultCode = ret["StateList"][0]["StateCode"]
resultStr = ret["StateList"][0]["StateMsg"]
apiMessage["test01"] = ret["ResultData"]
if resultCode == 1001 and resultStr=="成功":

        sava = txt.writeText("test01",apiMessage)
        username = txt.readText()["UserName"]
        salt = txt.readText()["Salt"] #读取文本里面的数据
        password = "a123456"
        hansleValue = rs.md5Function(salt,username,password)

        txt.writeText("test01",hansleValue)

method = "UserLogin"
rs = BaseConfig(method)
bodys = rs.body("HashedValue")
head = rs.Header("UserLogin")

res = requests.post(url,data=bodys.encode("utf-8"),headers=head)
r = re.search(r"\{.*\}", res.text)
ret = (json.loads(r.group()))#将str类型转换成字典类型
apiMessage["test01"] = ret["ResultData"]
txt.writeText("test01",apiMessage)
jsonpath_expr = parse("$..UserToken")
res  =[match.value for match in jsonpath_expr.find(ret)][0]
txt.writeText("test01",res)

r1 = BaseConfig("GetMalfunctionClass")
body1 = r1.body("UserToken,UserId")
head1 = r1.Header("GetMalfunctionClass")
ret1 = requests.post(url,data=body1.encode("utf-8"),headers=head1)
ret1 = re.search(r"\{.*\}", ret1.text)
ret1 = ret1.group()
#print(json.dumps(json.loads(ret1),indent=2,ensure_ascii=False))
jsonpath_expr = parse("$..MalfunctionClassId")
classid  =[match.value for match in jsonpath_expr.find(json.loads(ret1))][0]
MalfunctionClassId = classid
jsonpath_expr = parse("$..IssueMalfunctionClassId")
id  =[match.value for match in jsonpath_expr.find(json.loads(ret1))][0]
IssueMalfunctionClassId = id

#{"MalfunctionClassId":"45","RequestMatterList":[{"WorkTrayMalfunctionClassId":"102","IssueMalfunctionClassIdList":"173","Type":2,"ImageUrl":null,"ContentStr":""}]}


r2 = BaseConfig("SubmitMatter")
body2 = r2.body("UserToken,UserId")
head2 = r2.Header("SubmitMatter")
data1 = """
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <SubmitMatter xmlns="http://tempuri.org/">
      <JsonData>{"Version":"1.0.1","MasterSecret":"CTGi*7d54Fs*eruieud545Jgsdudb===Yhdt6","AppEstateId":"6124F8B9618591FA","DeviceInfo":"ONEPLUS A6000|9|WIFI网络|1.0.0|AArch64 Processor rev 13 (aarch64) ","ClientType":2,"Language":3,"UserToken":%s,"UserId":"21","MalfunctionClassId":"45","RequestMatterList":[{"WorkTrayMalfunctionClassId":"102","IssueMalfunctionClassIdList":"173","Type":2,"ImageUrl":null,"ContentStr":""}]}
</JsonData>
    </SubmitMatter>
  </soap:Body>
</soap:Envelope>
"""%json.dumps(res)
ret2 = requests.post(url,data=data1.encode("utf-8"),headers=head2)
ret2 = re.search(r"\{.*\}", ret2.text)
ret2 = json.loads(ret2.group())
MalfunctionId = (ret2["ResultData"]["MalfunctionId"])
header3 = {
            "SOAPAction": "http://tempuri.org/ICardAppService/SubmitMalfunction",
            "Accept": "application/json,text/javascript,*/*",
            "Content-Type": "text/xml"
        }
data2 = """
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <SubmitMalfunction xmlns="http://tempuri.org/">
      <JsonData>{"MasterSecret":"CTGi*7d54Fs*eruieud545Jgsdudb===Yhdt6","AppEstateId":"6124F8B9618591FA","Version":"1.0.0","DeviceInfo":"Redmi Note 4|7.0|1.0.0|AArch64 Processor rev 4 (aarch64)","ClientType":"2","Language":2,"UserName":"T2626","Location":"N/A","RegistrationID":"170976fa8aa40eb997d","UserToken":%s,"UserId":"21","MalfunctionId":%s,"SubmitKey":2}</JsonData>
    </SubmitMalfunction>
  </soap:Body>
</soap:Envelope>
        """%(json.dumps(res),json.dumps(MalfunctionId)) #注意点 用xml发送body请求时候 加入加密后的字符串 需要先json.dumps 来解决json解析的错误 因为这是要JSONDATA的格式要求
ret3 = requests.post(url,data=data2.encode("utf-8"),headers=header3)
print(ret3)
ret3 = re.search(r"\{.*\}", ret3.text)
ret3 = json.loads(ret3.group())