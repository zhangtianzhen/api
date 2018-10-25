import requests
import json
import hashlib
import xmltodict
import re
import sys
# print(sys.getdefaultencoding())
url= "http://altomobile.test.cn-cic.com/CardAppService.svc"


data1 = """
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <GetUserLoginInfo xmlns="http://tempuri.org/">
      <JsonData>{"MasterSecret":"CTGi*7d54Fs*eruieud545Jgsdudb===Yhdt6","AppEstateId":"6124F8B9618591FA","Version":"1.0.0","DeviceInfo":"Redmi Note 4|7.0|1.0.0|AArch64 Processor rev 4 (aarch64)","ClientType":"2","Language":2,"UserName":"T2626"}</JsonData>
    </GetUserLoginInfo>
  </soap:Body>
</soap:Envelope>
"""
header ={
    "SOAPAction":"http://tempuri.org/ICardAppService/GetUserLoginInfo",
    "Accept":"application/json,text/javascript,*/*",
    "Content-Type":"text/xml"
}


res = requests.post(url,data=data1.encode('utf-8'),headers=header)
res = res.text
r0 = json.loads(re.findall(r'(\{.*\})', res)[0])
r = r0["ResultData"]
# r1 = eval(re.findall('"StateList":\[(.*)\]',res)[0])
r1 = r0["StateList"][0]
print(r)
print(r1["StateMsg"])

#res = json.loads(r.group())#先转换成字典 方便操作
#print(res)

convertedDict = xmltodict.parse(res) #转换成字典

res = json.dumps(convertedDict,indent=3,sort_keys=True)#转换成json

res =convertedDict["s:Envelope"]["s:Body"]["GetUserLoginInfoResponse"]["GetUserLoginInfoResult"] #取到最后一个为字符串 要转换成字典
ret = (json.loads(res))


#print(json.dumps(ret["ResultData"]))

resultCode = ret["StateList"][0]["StateCode"]
resultStr = ret["StateList"][0]["StateMsg"]
if resultCode == 1001 and resultStr=="成功":
    str3 = res
    resutl =re.findall(r'"ResultData":(\{(.+)\})',str3) #正则匹配ResultData
    if resutl:

        res = json.loads(resutl[0][0][:-1]) #将内容转换成字典类型
       # print(res["Salt"]) #取的盐
        salt = res["Salt"] #取得盐
        username = res["UserName"]
        password = "a123456"
        #MD5 加密规则:salt:username:password
        ecode = salt+":"+username+":"+password
       # print("加密前的规则:\t",ecode)
        md5 = hashlib.md5()
        md5.update(ecode.encode(encoding='utf-8')) #加密的后的密码 需要大写
        code = md5.hexdigest()
        code = code.upper() #转换成大写的
        print(code)
        data2 = """
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <UserLogin xmlns="http://tempuri.org/">
      <JsonData>{"MasterSecret":"CTGi*7d54Fs*eruieud545Jgsdudb===Yhdt6","AppEstateId":"6124F8B9618591FA","Version":"1.0.0","DeviceInfo":"Redmi Note 4|7.0|1.0.0|AArch64 Processor rev 4 (aarch64)","ClientType":"2","Language":2,"UserName":"T2626","Location":"N/A","RegistrationID":"170976fa8aa40eb997d","HashedValue":%s}</JsonData>
    </UserLogin>
  </soap:Body>
</soap:Envelope>
        """%json.dumps(code) #注意点 用xml发送body请求时候 加入加密后的字符串 需要先json.dumps 来解决json解析的错误 因为这是要JSONDATA的格式要求

        header = {
            "SOAPAction": "http://tempuri.org/ICardAppService/UserLogin",
            "Accept": "application/json,text/javascript,*/*",
            "Content-Type": "text/xml"
        }
        ree = requests.post(url,data=data2, headers=header)
        r = re.search(r"\{.*\}", ree.text)
        print(r.group())
        res = json.loads(r.group()) #先转换成字典 放到文本里面不易出错 例如将null 转换成python的none true 转换成 True 因为服务端返回的是字符串

        userId= res["ResultData"]["UserId"]
        userToken = res["ResultData"]["UserToken"]
        print('获取到用户id:\t',userId)
        print("获取用户token:\t",userToken)

