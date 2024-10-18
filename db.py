import mysql.connector
import os 
from dotenv import load_dotenv
load_dotenv()

class Failed(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class EMS:
    def __init__(self):
        self.ems = mysql.connector.connect(
            host= os.getenv('MYSQL_HOST'),
            port="3306",
            user= os.getenv('MYSQL_USER'),
            password= os.getenv('MYSQL_PWD'),
            database="EMS"
        )

        self.emsCursor = self.ems.cursor(buffered=True)
    
    
    def checkConnection(self):
        if not self.ems.is_connected():
            self.ems.reconnect()
        
    def login(self, username , password):
        self.checkConnection()
        try:
            query = 'SELECT id from Management where username = (%s) AND password = (%s)'
            params  = (username, password)
            self.emsCursor.execute(query,params)

            return [i for i in self.emsCursor], True 

        except Exception as e:
            return e, False
    
    def view(self,empid):
        self.checkConnection()
        try:
            if 'TEMP' in empid:
                query = 'SELECT * from Testing where id = (%s)'
                params  = (empid,)
                self.emsCursor.execute(query,params)

                return [i for i in self.emsCursor], True 
            
            elif 'DEMP' in empid:
                query = 'SELECT * from Development where id = (%s)'
                params  = (empid,)
                self.emsCursor.execute(query,params)

                return [i for i in self.emsCursor], True 
            
            else:
                return [], True

        except Exception as e:
            return e, False
        
    def add(self,empid,name,salary,state,education,pid):
        self.checkConnection()
        try:
            if 'TEMP' in empid:
                query = 'insert into Testing(id,name,salary,state,education,pid) values(%s,%s, %s, %s ,%s , %s);'
                params  = (empid,name,salary,state,education,pid)
                self.emsCursor.execute(query,params)
                self.ems.commit()
                return True, True 
            
            elif 'DEMP' in empid:
                query = 'insert into Development(id,name,salary,state,education,pid) values(%s,%s, %s, %s ,%s , %s);'
                params  = (empid,name,salary,state,education,pid)
                self.emsCursor.execute(query,params)
                self.ems.commit()
                return True, True 
            
            else:
                return False, True

        except Exception as e:
            return e, False
    
    def update(self,empid, keys:list , values:list):
        self.checkConnection()
        try:
            if 'TEMP' in empid:
                for key in keys:
                    query = f"UPDATE Testing SET {key} = %s WHERE id = %s"
                    params = (values[keys.index(key)],empid)
                    self.emsCursor.execute(query,params)
                    self.ems.commit()
                return True , True
            
            elif 'DEMP' in empid:
                for key in keys:
                    query = f"UPDATE Development SET {key} = %s WHERE id = %s"
                    params = (values[keys.index(key)],empid)
                    self.emsCursor.execute(query,params)
                    self.ems.commit()
                return True , True 
            
            else:
                return False, True

        except Exception as e:
            return e, False
        
    def delete(self,empid):
        self.checkConnection()
        try:
            if 'TEMP' in empid:
                query = 'select name from Testing where id=(%s)'
                params  = (empid,)
                self.emsCursor.execute(query,params)
                if [i for i in self.emsCursor] == []:
                    raise Failed('Not Found') 

                query = 'delete from Testing where id=(%s)'
                params  = (empid,)
                self.emsCursor.execute(query,params)
                self.ems.commit()
                return True, True 
            
            elif 'DEMP' in empid:
                query = 'select name from Development where id=(%s)'
                params  = (empid,)
                self.emsCursor.execute(query,params)
                if [i for i in self.emsCursor] == []:
                    raise Failed('Not Found') 
                
                query = 'delete from Development where id=(%s)'
                params  = (empid,)
                self.emsCursor.execute(query,params)
                self.ems.commit()
                return True, True 
            
            else:
                return False, True

        except Exception as e:
            return e, False
    
    def top(self):
        self.checkConnection()
        try:
            query = 'SELECT * FROM ( select name,state,education,salary from Testing union select name,state,education,salary from Development ) as Combined_employees WHERE salary >= (SELECT AVG(salary) AS average_salary FROM ( SELECT salary FROM Testing UNION ALL SELECT salary FROM Development ) AS combined_salaries);'
            self.emsCursor.execute(query)
            return [i for i in self.emsCursor] , True 

        except Exception as e:
            return e, False
    
    def all(self):
        self.checkConnection()
        try:
            query = 'SELECT * FROM ( select name,state,education,"Testing",pid from Testing union select name,state,education,"Development",pid from Development ) as Combined_employees INNER JOIN Projects ON Combined_employees.pid = Projects.pid;'
            self.emsCursor.execute(query)
            return [i for i in self.emsCursor] , True 

        except Exception as e:
            return e, False
        
    def dis(self):
        self.checkConnection()
        try:
            query = 'SELECT state,COUNT(*) FROM ( select state from Testing union select state from Development ) as Combined_employees GROUP BY state;'
            self.emsCursor.execute(query)
            return [i for i in self.emsCursor] , True 

        except Exception as e:
            return e, False