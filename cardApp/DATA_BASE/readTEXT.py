#-*- coding:gbk -*-
import json
import re
import  os
"""
�������߲�������ͨ������idȡ����
"""
file_path = os.path.split(os.path.realpath(__file__))[0] #�鿴��ǰ·��
class TextManage():

    def readText(self,*args):
        fb = open(file_path+"\\"+"personal", "r",encoding="UTF-8")
        for i in fb.readlines():
            res = eval(i)
            if res.get("test01"):
                return res["test01"]
        fb.close()

    def writeText(self,*args):

        #a = {'CarParkingSpaceInfo': [{'CarParkingSpaceInfoId': 1, 'CarParkingFloor': '1', 'SpaceNo': '1', 'CarParkingSpaceFloorPlan': 'http://altofile.test.cn-cic.com/HandoverFile/20180720/8ffcb87d-e8e2-43ad-ab0e-b84663780653.png'}], 'CICMemberQRCode': '4C81244D3EE9956D15CA36D740BC78C1D425D9BDE112C53ACBF0BC80C96A01C372F5B36A3E91E00BA41B438633A3679F91C20E575DE657E09DB119A49C2F5AFD7E191C142F42403F3AE0CCA9EA6C0B80E942E9098A94C9615C53DF78C72C9A725CBF928056C12CFB8E336E2CD1E4C2001B79B4D94E65C12D3741DCCE8F6E4A0D9A12E3044E133E87', 'QRCodeEffectiveDuration': 300, 'UserName': 'T2727', 'UserId': 21, 'UserToken': '123456789123456789', 'TagsList': 'UserDefault,B26F26U26,OwnerB26F26U26,all,GO_6DC6BDED0A91834E,6124F8B9618591FA', 'Alias': '6DC6BDED0A91834E', 'UserDisplayName': '����1', 'UserChiDisplayName': '����2', 'UserSimChiDisplayName': '����3', 'UserEngDisplayName': '����4', 'EmailAll': '446343417@qq.com', 'Email': '446343417@qq.com', 'Email2': '', 'HomePhone': '', 'MobilePhone': '13965440195', 'Avatar': 'http://altofile.test.cn-cic.com/Images/20180727/77844fd4-b14f-440d-9e4f-c8d841800a8e.jpg', 'IsOwner': True, 'Building': '26', 'Unit': '26', 'Floor': '26', 'FloorPlan': 'http://altofile.test.cn-cic.com/ManageImages/UnitFloorPlan/151c632a-6569-4180-9e36-46b747c0c666.jpg', 'Gender': '��', 'CanHandoverHouseBook': 2, 'HanoverHouseStartDate': '2018-06-04T00:00:00', 'ReportProjectStatus': 2, 'AddMatterStatus': 1, 'MatterStatus': 2, 'DaysRemaining': 0, 'CurrentSubmitKey': 3}
        a = args[0] #����id

        fb = open(file_path+"\\"+"personal", "r+",encoding="utf-8")
        list1 = []
        ret = fb.readlines()#��ȡ���е�����
        if ret:
            for i in ret:
                res = eval(i) #ת�����ֵ�
                if res.get(a):
                    try:
                        if type(args[1]) != str:

                            if (res.get(a)["UserName"]) == args[1][a]["UserName"]: #�ж��û�������ͬ
                                    itm = args[1][a].items()#��ȡ�ӿ����·��ص�����
                                    for key,value in itm:
                                        res[a][key]=value #���ھ��޸� �����ھ����
                        else:
                            res[a]["HashedValue"] = args[1]  #��Ӽ��ܵ��ַ���
                    except Exception as e:
                        print("����", e)
                        return None  # ������б����� ������ֹ������ļ�д��
                    else:
                        list1.append(res)
                else:
                    list1.append(res)

        else:
            list1.append(args[1])
        fb.close()

        fb = open(file_path+"\\"+"personal", "w+", encoding="utf-8") #���´� д���ļ�
        try:
            for i in list1:
                fb.write(str(i)+"\n")
        except Exception as e:
            print("д���ļ�����")
        else:
            fb.close()
            return True


if __name__ == "__main__":
    t = TextManage()
    t.readText()

