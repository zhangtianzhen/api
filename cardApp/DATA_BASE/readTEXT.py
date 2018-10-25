#-*- coding:gbk -*-
import json
import re
import  os
"""
依赖或者不依赖都通过用例id取数据
"""
file_path = os.path.split(os.path.realpath(__file__))[0] #查看当前路径
class TextManage():

    def readText(self,*args):
        fb = open(file_path+"\\"+"personal", "r",encoding="UTF-8")
        for i in fb.readlines():
            res = eval(i)
            if res.get("test01"):
                return res["test01"]
        fb.close()

    def writeText(self,*args):

        #a = {'CarParkingSpaceInfo': [{'CarParkingSpaceInfoId': 1, 'CarParkingFloor': '1', 'SpaceNo': '1', 'CarParkingSpaceFloorPlan': 'http://altofile.test.cn-cic.com/HandoverFile/20180720/8ffcb87d-e8e2-43ad-ab0e-b84663780653.png'}], 'CICMemberQRCode': '4C81244D3EE9956D15CA36D740BC78C1D425D9BDE112C53ACBF0BC80C96A01C372F5B36A3E91E00BA41B438633A3679F91C20E575DE657E09DB119A49C2F5AFD7E191C142F42403F3AE0CCA9EA6C0B80E942E9098A94C9615C53DF78C72C9A725CBF928056C12CFB8E336E2CD1E4C2001B79B4D94E65C12D3741DCCE8F6E4A0D9A12E3044E133E87', 'QRCodeEffectiveDuration': 300, 'UserName': 'T2727', 'UserId': 21, 'UserToken': '123456789123456789', 'TagsList': 'UserDefault,B26F26U26,OwnerB26F26U26,all,GO_6DC6BDED0A91834E,6124F8B9618591FA', 'Alias': '6DC6BDED0A91834E', 'UserDisplayName': '测试1', 'UserChiDisplayName': '测试2', 'UserSimChiDisplayName': '测试3', 'UserEngDisplayName': '测试4', 'EmailAll': '446343417@qq.com', 'Email': '446343417@qq.com', 'Email2': '', 'HomePhone': '', 'MobilePhone': '13965440195', 'Avatar': 'http://altofile.test.cn-cic.com/Images/20180727/77844fd4-b14f-440d-9e4f-c8d841800a8e.jpg', 'IsOwner': True, 'Building': '26', 'Unit': '26', 'Floor': '26', 'FloorPlan': 'http://altofile.test.cn-cic.com/ManageImages/UnitFloorPlan/151c632a-6569-4180-9e36-46b747c0c666.jpg', 'Gender': '男', 'CanHandoverHouseBook': 2, 'HanoverHouseStartDate': '2018-06-04T00:00:00', 'ReportProjectStatus': 2, 'AddMatterStatus': 1, 'MatterStatus': 2, 'DaysRemaining': 0, 'CurrentSubmitKey': 3}
        a = args[0] #用例id

        fb = open(file_path+"\\"+"personal", "r+",encoding="utf-8")
        list1 = []
        ret = fb.readlines()#读取所有的数据
        if ret:
            for i in ret:
                res = eval(i) #转换成字典
                if res.get(a):
                    try:
                        if type(args[1]) != str:

                            if (res.get(a)["UserName"]) == args[1][a]["UserName"]: #判断用户姓名相同
                                    itm = args[1][a].items()#获取接口最新返回的数据
                                    for key,value in itm:
                                        res[a][key]=value #存在就修改 不存在就添加
                        else:
                            res[a]["HashedValue"] = args[1]  #添加加密的字符串
                    except Exception as e:
                        print("报错", e)
                        return None  # 这里进行报错处理 并且阻止下面的文件写入
                    else:
                        list1.append(res)
                else:
                    list1.append(res)

        else:
            list1.append(args[1])
        fb.close()

        fb = open(file_path+"\\"+"personal", "w+", encoding="utf-8") #重新打开 写入文件
        try:
            for i in list1:
                fb.write(str(i)+"\n")
        except Exception as e:
            print("写入文件错误")
        else:
            fb.close()
            return True


if __name__ == "__main__":
    t = TextManage()
    t.readText()

