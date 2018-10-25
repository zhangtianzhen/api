"""
操作层 进行get,post处理
"""
import requests
import json
import hashlib
import xmltodict
import re
from jsonpath_rw import jsonpath,parse
url = "http://hkustmobile.test.cn-cic.com/CardAppService.svc"
class Distribution():#对请求进行分发处理

    def Post(self,body,header):

        try:

            result = requests.post(url,data=body.encode("utf-8"),headers=header)
            res = result.text

            r0 = json.loads(re.findall(r'(\{.*\})', res)[0])
            r1 = r0["StateList"][0]
            r2 = re.findall('xmlns="http://tempuri.org/"><(.*)Result>{', res)[0]
            if r1["StateCode"] == 1001 and r1["StateMsg"] == "成功":

                pass


            else:
                print(r2+"请求接口错误>>>>>>"+r1["StateMsg"])
        except Exception as e:

            print("请求模块报错",e)
        else:

            return r0
    def Get(self):
        pass


#     pass
