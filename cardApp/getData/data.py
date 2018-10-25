from DATA_BASE.readExcel import Excele
from config.execlconfig import *

"""
获取传过来的行 和 列
"""

class GetData(object):

    def __init__(self,sheet=0):#初始化操作excel的类
        self.excel = Excele(sheet)

    def get_Value(self,row,col):#公共的取excel值方法
        result = self.excel.getValue(row, col)
        if result:
            return result
        return None

    def allLines(self):#获取总行数 执行用例的次数
        return self.excel.allCase()

    def Get_Id(self,row): #获取每行的id
        col = getId() #获取列
        return self.get_Value(row,col)
        # result = self.excel.getValue(row,col)
        # if result:
        #     return result
        # return None


    def Get_Page(self,row): #获取每一行的页面
        col = getPage()
        return self.get_Value(row, col)

    def Get_Name(self,row): #获取每一行的名称
        col = getNmae()
        return self.get_Value(row, col)
    def Get_Client(self,row):
        col = getClien()
        return self.get_Value(row, col)
    def Get_Parameter(self,row):
        col = getParameter()
        return self.get_Value(row, col)

    def Get_Url(self,row):
        col = getUrl()
        return self.get_Value(row, col)


    def Get_getMethod(self,row):
        col = getMethod()
        return self.get_Value(row, col)
    def Get_getExecute(self,row):
        col = getExecute()
        return self.get_Value(row, col)
    def Get_getRequest_Method(self,row):
        col = getRequest_Method()
        return self.get_Value(row, col)

    def Get_Header(self,row):
        col = Header()
        return self.get_Value(row, col)

    def Get_RelyID(self,row):
        col = RelyID()
        return self.get_Value(row, col)

    def Get_RelyData1(self,row):
        col = RelyData1()
        return self.get_Value(row, col)


    def Get_RelyData2(self,row):
        col = RelyData2()
        return self.get_Value(row, col)
    def Get_RelyFied(self,row):
        col = RelyFied()
        return self.get_Value(row, col)

    def Get_RequestDate(self,row):
        col = RequestDate()
        return self.get_Value(row, col)

    def Get_ExpectedReuslt(self,row):
        col = ExpectedReuslt()
        return self.get_Value(row, col)


if __name__ == "__main__":
    test = GetData()
    a = (test.Get_RelyData1(2))
    print(a)