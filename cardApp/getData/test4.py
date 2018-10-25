# dict2 = {"Version":"1.0.0","MasterSecret":"CTGi*7d54Fs*eruieud545Jgsdudb===Yhdt6","AppEstateId":"6124F8B9618591FA","DeviceInfo":"ONEPLUS A6000|9|WIFI网络|1.0.0|AArch64 Processor rev 12 (aarch64) ","ClientType":2,"Language":3,"UserToken":"CF4A3990CAB183E318705B5BA5E75441C4DA85CF2CDA98C59984CE532212E151047107DA809FA1C222188A31B9E3DA0A4771BFEBD834B44F","UserId":"21","MalfunctionId":"97","SubmitKey":2}
# dict3 = {"MalfunctionClassId":"45","RequestMatterList":[{"WorkTrayMalfunctionClassId":"102","IssueMalfunctionClassIdList":"173","Type":2,"ImageUrl":None,"ContentStr":""}]}
# dict2.update(dict3)
# from jsonpath_rw import jsonpath,parse
# a={'ResultType': 1, 'HandoverHouseList': [{'HandoverFeederVehicle': [{'HandoverFeederVehicleId': 2, 'Add': '將軍澳地鐵站', 'FeederVehicleMins': 5, 'WaitingTime': 5, 'LimitQuantity': 5}], 'HandoverHouseId': 147}]}
# jsonparse = parse("$..HandoverHouseId")
# res = [match.value for match in jsonparse.find(a)][0]
# print(res)
import requests
import base64
import json
url = "http://altomobile.test.cn-cic.com/CardAppService.svc"
body = """

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <EditUserAvatar xmlns="http://tempuri.org/">
      <JsonData>{"MasterSecret":"CTGi*7d54Fs*eruieud545Jgsdudb===Yhdt6","AppEstateId":"6124F8B9618591FA",
      "Version":"1.0.0","DeviceInfo":"Redmi Note 4|7.0|WIFI网络|1.0.0|AArch64 Processor rev 4 (aarch64)",
      "ClientType":"2","Language":2,"UserName":"T2626","Location":"N/A","RegistrationID":"170976fa8aa40eb997d","UserId": 21,"CurrentFileName":"T26261538061595439.jpg",
      "UserToken":"CF4A3990CAB183E3AB7863B22D33DAE428C38D93CA3C3E8EC79194502AC5EBA32ACD18468AB170C5CA83ED17BC6D7949CBA61F93895A52D8"}</JsonData>
    </EditUserAvatar>
  </soap:Body>
</soap:Envelope>

"""
header = {
            "SOAPAction": "http://tempuri.org/ICardAppService/EditUserAvatar",
            "Accept": "application/json,text/javascript,*/*",
            "Content-Type": "text/xml;charset=UTF-8"
        }


file = {"img":('H:/cardApp/config/text.jpg',base64.b64encode(open("H:/cardApp/config/text.jpg",'rb').read()).decode(),'img/png',{})}
imagefile = 'H:\cardApp\config\\text.jpg'

files = {"currentFileBytes [ i:type=c:base64 ]":base64.b64encode(open(imagefile,'rb').read()).decode()}
files = {"img":(imagefile,open(imagefile,"rb"),"img/png",{})}
r = requests.post(url,data=body.encode("utf-8"),headers=header,files=files)
print(r.text)