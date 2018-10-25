from DATA_BASE.readExcel import Excel
from config.execlconfig import *
from config.requestConfigtest import API
class RePlay(object):

    def __init__(self,replayid):
        self.replayid = replayid
        self.excel = Excel()
        self.req = API()

    def getReplayMethod(self):

        allmethod = []
        allid = []

        id = self.replayid #当前依赖的名称 例如test01
        allid.append(id)
        while True:

            num = self.excel.get_row_num(id) #根据当前依赖id找到编号
            id = self.excel.getValue(num, getRelyID()) # 找到所在接口 查看所依赖的名称  用于下一次循环使用
            if id == "": #添加最后一个依赖的方法 这里是循环到了 最后一个依赖id  这是添加最后一个依赖id的方法 如果这个接口 依赖的用例编号为空 则在列表加入当前的方法名
                allmethod.append(self.excel.getValue(num, getMethod()))

                break #结束循环
            else: #如果当前不为空  则加入当前的 接口 的名称 继续循环查找是否还有依赖的接口
                allid.append(id)
                allmethod.append(self.excel.getValue(num, getMethod()))

        allmethod.reverse() #翻转列表内容  按顺序发送接口请求
        #print("所有的依赖方法",allmethod)
        #print("所有的依赖id",allid)
        return [allmethod,allid]


    def runTest(self):
        allMethod ,allid = self.getReplayMethod()[0] ,self.getReplayMethod()[1]#取得当前接口所有依赖的方法
        for j in range(1,self.excel.allCase()):  #查询当前exce的用例数量
            for i in allMethod:
                if self.excel.getValue(j,getMethod()) == i :

                    testid = self.excel.getValue(j,getId())
                    url = self.excel.getValue(j,getUrl()) #获取url
                    method =self.excel.getValue(j,getMethod()) #获取方法
                    args = self.excel.getValue(j,getRequestDate()) #获取账号
                    keyvalue = self.excel.getValue(j,getRelyData2()) #提取当前接口的响应数据并保存
                    forApidata = self.excel.getValue(j,getRelyFied()) #放入本次接口的数据
                    value = self.excel.getValue(j, getInputKey())  # 提取本次接口需要的数据用以发送给后台
                    if testid in allid: #进一步判断 当前方法是否属于这个用例id
                        result = getattr(self.req, i)(url, method=method, thisApi=forApidata, args=args, extract=keyvalue,lastApi=value)
                       # print("依赖接口", i,testid)
                    #print(result)