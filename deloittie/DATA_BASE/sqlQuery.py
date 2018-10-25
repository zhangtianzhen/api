import  pymysql
import json
class BaseQuery(object):

    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1",port=3306,user="root",password="123456",database="apiresult",charset="utf8")
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
    def selecet(self,testid):
        self.cursor.execute("select testid from delotitle where testid = %s",[testid])
        result = self.cursor.fetchone()
        return result

    def insert(self,testid,expect,result,apireturn,times):
        self.cursor.execute("insert into delotitle(testid,expect,result,apireturn,times) values(%s,%s,%s,%s,%s)",[testid,expect,result,apireturn,times])
        self.conn.commit()

    def update(self,testid,expect,result,apireturn,times):
        self.cursor.execute("update delotitle set expect=%s,result=%s,apireturn=%s,times=%s where testid=%s",[expect,result,apireturn,times,testid])
        self.conn.commit()
    def allCase(self):
        self.cursor.execute("select count(testid) from delotitle")
        return  self.cursor.fetchone()

    def selectByid(self, id):
        self.cursor.execute("select apireturn from request where id = %s", [id])
        return self.cursor.fetchone()

    def __del__(self):
        self.cursor.close()
        self.conn.close()



if __name__ == "__main__":
    test = BaseQuery()
    result = (test.selecet("test07"))
    print(result)