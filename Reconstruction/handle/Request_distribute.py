"""
操作层 进行get,post处理
"""
import requests
import json
import hashlib
import xmltodict
import re
from jsonpath_rw import jsonpath,parse

class Distribution():#对请求进行分发处理

    def Post(self,url,body,header):

        try:

            result = requests.post(url,data=body.encode("utf-8"),headers=header)
            res = result.text

            r0 = json.loads(re.findall(r'(\{.*\})', res)[0])
            r1 = r0["StateList"][0]
            r2 = re.findall('xmlns="http://tempuri.org/"><(.*)Result>{', res)[0]
            if r1["StateCode"] == 1001 and r1["StateMsg"] == "成功":

                pass
                #print(r2+"请求接口正常>>>>>"+r1["StateMsg"])

            else:
                print(r2+"请求接口错误>>>>>>"+r1["StateMsg"])
        except Exception as e:

            print("请求模块报错",e)
        else:

            # return r0["ResultData"] 修改前
            # if r0["ResultData"] ==None:
            #     return {'StateCode': 1003, 'StateMsg': '参数错误'}
            # try:
            #
            #     if type(r0["ResultData"]) == list:
            #         print(r0["ResultData"]+r0["StateList"])
            #         return r0["ResultData"]+r0["StateList"]
            #
            #     r0["ResultData"].update(r1)
            #     return  r0["ResultData"] #修改后
            # except Exception as e:
            #     print("Post请求模块报错>>>>",e)
            return r0
    def Get(self):
        pass


#     pass
