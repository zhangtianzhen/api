import xlrd
import os,os.path,sys

path = (sys.path[1]+"\\"+"config"+"\\"+"ust.xlsx") #动态获取文件地址 方便任意电脑运行


class Excel(object):

    def __init__(self,num=0):

        data = xlrd.open_workbook(path)
        self.sheet = data.sheets()[num]

    def allCase(self):#获取当前excel表的测试用例总数
        return self.sheet.nrows

    def getValue(self,row=1,col=1): #获取指定的单元内容
        if isinstance(row, int) == True and isinstance(col, int) == True:
            x, y = row, col
        else:
            if isinstance(row, int) != True and isinstance(col, int) != True:
                x, y = 0, 0
            elif isinstance(row, int) == True and isinstance(col, int) != True:

                y = 0
            elif isinstance(row, int) != True and isinstance(col, int) == True:
                x = 0
        return self.sheet.cell_value(row,col)



    def get_rows_data(self,case_id):#根据对应的case _id 找到对应的内容
        row_num = self.get_row_num(case_id)
        rows_data = self.get_raw_values(row_num)
        return rows_data

    def get_row_num(self,case_id): #根据对应的case_id 找到对应的行号
        num = 0
        clols_data = self.get_cols_data()
        for col_data in clols_data:
            if case_id in col_data:
                return num
            num += 1
        return num
    def get_raw_values(self,row): #根据行号 找到该行的内容
        tables = self.sheet #拿到全部的sheet内容
        row_data = tables.row_values(row) #row_values获取行内容
        return row_data

    def get_cols_data(self,col_id=0): #获取列内容
        if col_id :
            cols =self.sheet.col_values(col_id)
        else:
            cols = self.sheet.col_values(col_id)
        return cols

if __name__ == "__main__":
    t = Excel()
    # print(file_path)
    print(t.getValue(2,7))

