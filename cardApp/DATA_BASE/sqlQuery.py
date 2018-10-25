import  pymysql
import json
class BaseQuery(object):

    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1",port=3306,user="root",password="123456",database="api",charset="utf8")
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def selectByid(self,testid): #通過用例id查找數據 有依賴的 case走這條
        self.cursor.execute("select value from request where testid =%s and username=%s",[testid])
        if self.cursor.fetchone():
            return json.loads(self.cursor.fetchone()["value"])
        else:
            return None



    def selectByUsername(self,username): #通過username查找該用戶所有數據 這是執行不依賴的case
        try:
            self.cursor.execute("select value from request where username=%s",[username])

            return json.loads(self.cursor.fetchone()["value"])
        except :
            return None


    def selectByid_username(self,testid,username):
        self.cursor.execute("select value from request where testid=%s and username=%s",[testid,username])
        return json.loads(self.cursor.fetchone()["value"])

    def updateByid(self,testid,data):
        self.cursor.execute("update request set value =%s where testid=%s",[data,testid])
        self.conn.commit() #提交執行

    def updateByUsername(self,username,data):
        self.cursor.execute("update request set VALUE=%s where username=%s ",[data,username])
        self.conn.commit()
    def insert(self,testid,username,value):
        self.cursor.execute("insert into request(testid,username,value) values(%s,%s,%s)",[testid,username,value])
        self.conn.commit()


    def __del__(self):
        self.cursor.close()
        self.conn.close()



if __name__ == "__main__":
    test = BaseQuery()
    result = (test.selectByid("test01"))
    print(result)