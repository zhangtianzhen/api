import  pymysql
import json
class BaseQuery(object):

    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1",port=3306,user="root",password="123456",database="api",charset="utf8")
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
    def selecet(self,testid):
        self.cursor.execute("select expect from request where testid = %s",[testid])
        result = self.cursor.fetchone()
        return result

    def insert(self,testid,expect):
        self.cursor.execute("insert into request(testid,expect) values(%s,%s)",[testid,expect])
        self.conn.commit()
    def update(self,testid,expect):
        self.cursor.execute("update request set testid = %s,expect=%s",[testid,expect])
        self.conn.commit()

    def selectByid(self,testid):
        self.cursor.execute("select testid from request where testid = %s",[testid])
        return self.cursor.fetchone()
    def __del__(self):
        self.cursor.close()
        self.conn.close()



if __name__ == "__main__":
    test = BaseQuery()
    result = (test.selectByid("test07"))
    print(result)