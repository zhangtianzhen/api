import pymysql
"""
登陆,交楼与执漏的sql操作
2018/9/16
"""
class Sql(object):

    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1",port=3306,user="root",password="123456",database="api",charset="utf8")
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def select(self,name):
        try:
            if name:
                #查询出结果集
                self.cursor.execute( """
                select * from requestdata left  join dependdata on 
                requestdata.depid = dependdata.reqid where name = %s
                """,[name,])

        except Exception as e:
            return None
        else:

            return self.cursor.fetchone()

    def replyDataTotestId(self,test_id): #根据依赖id查找数据
        try:
            if test_id:
                self.cursor.execute(
                    """
                    select * from requestdata left  join  dependdata on requestdata.depid = dependdata.reqid 
                    where test_id = %s
                    """,[test_id]
                )
        except Exception as e:
            return None
        return self.cursor.fetchone()

    def updateToken(self,name,token,*args):#更新token值
        try:
            if name:
                self.cursor.execute("""
                    update requestdata LEFT JOIN 
                    dependdata on requestdata.depid = dependdata.reqid 
                    set usertoken=%s where name=%s
                """,[name,token])
        except Exception as e:
            return None
        else:
            self.conn.commit()
            return "ok"

    def updateHashedValue(self,name,HashedValue,*args): #更新盐值
        try:
            if name:
                self.cursor.execute("""
                    update requestdata LEFT JOIN 
                    dependdata on requestdata.depid = dependdata.reqid 
                    set HashedValue=%s where name=%s
                """,[name,HashedValue])

        except Exception as e:
            return None
        else:
            self.conn.commit()
            return "ok"
    def updatePassword(self,name,password,*args): #更新密码
        try:
            if name:
                self.cursor.execute("""
                update requestdata set password=%s  where name=%s
                """,[password,name])
        except Exception as e:
            return None
        else:
            self.conn.commit()
            return  "ok"
    def updatemobile(self,name,mobile,*args): #更新电话号码
        try:
            if name:
                self.cursor.execute("""
                update requestdata set mobile=%s where name =%s
                """,[mobile,name])
            else:
                return None
        except Exception as e:
            return None
        else:
            self.conn.commit()
            return "ok"
    def updateEmail(self,name,email,*args):#更新邮箱
        try:
            if name:
                self.cursor.execute("""
                update requestdata set eamil=%s where name=%s 
                """,[email,name])

        except Exception as e:
            return None
        else:
            self.conn.commit()
            return "ok"
    def updateTime(self,name,time,*args):#更新系统时间
        if name:
            try:
                self.cursor.execute(
                    """
                    update requestdata set CurrentServerTime = %s where name = %s
                   """,[name,time])
            except Exception as e:
                return None
            else:
                self.conn.commit()
                return "ok"
        return None

    def updateEncode(self,name,code,*args): #更新加密规则
        try:
            if name !=None and code !=None:
                self.cursor.execute(
                    """
                    update requestdata LEFT JOIN
                    dependdata ON requestdata.depid = dependdata.reqid  SET code = %s where name = %s
                    """,[code,name])
        except Exception as e:
            return None
        else:
            self.conn.commit()
            return "ok"

    def insertRequestData(self,*args): #新增requestdata表数据

        try:

            self.cursor.execute(
                """
                insert into requestdata(depid,name,account,password,mobile,email)
                """,[args[0],args[1],args[2],args[3],args[4]])


        except Exception as e:
            return None
        else:
            self.conn.commit()
            return "ok"


    def insertDependataMany(self,*args):#数据依赖表 插入多条数据

        try:
            self.cursor.execute(
                """
                insert into dependdata(reqid,HashedValue,usertoken,encode)
                """,[args[0],args[1],args[2],args[3]])
        except Exception as e:
            return e

        else:
            self.conn.commit()
            return "ok"

    def updateRequestMany(self,name,*args):#一次更新多条数据

        try:
            self.cursor.execute("""
            update requestdata SET account=%s,password=%s,mobile=%s,email=%s  where name=%s
            """
            ,[args[0],args[1],args[2],args[3],name])
        except Exception as e:
            return None
        else:
            self.conn.commit()
            return "ok"

    def updateDepdendDataMany(self,name,*args): #更新数据依赖表多个字段的值
        try:
            self.cursor.execute("""
            update requestdata left join dependdata on request.depid = dependdata.reqid 
            set HashedValue=%s,usertoken=%s,encode=%s where name = %s
            """,[args[0],args[1],args[2],name])
        except Exception as e:
            return None
        else:
            self.conn.commit()
            return "ok"

    def delete(self,*args):
        pass

    def __del__(self):
        self.cursor.close()
        self.conn.close()

t = Sql()
print(t.select("user1"))