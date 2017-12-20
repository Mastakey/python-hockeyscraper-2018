import pyodbc
import sqlite3

class WEBDB(object):
    def __init__(self, dbStr, config):
        #DRIVER={SQL Server};SERVER=SQLBRSDEV02;DATABASE=Serena;UID=SerenaAdm;PWD=$3r3n4Adm1
        if config['type'] == 'sqlite':
            self.dbcon = sqlite3.connect(dbStr)
        else:
            self.dbcon = pyodbc.connect(dbStr)
        self.cursor = self.dbcon.cursor()
        self.config = config

    def debugLog(self, string):
        if self.config['logging'] == "on":
            f = open("WEBDB.log", "a")
            f.write(string)
            f.write("\n")

    def executeQuery(self, query):
        cursor = self.dbcon.cursor()
        self.debugLog(query)
        values = cursor.execute(query)
        self.dbcon.commit()
        return values
        
    def insertQuery(self, query):
        cursor = self.dbcon.cursor()
        self.debugLog(query)
        values = cursor.execute(query)
        self.dbcon.commit()
        return cursor.lastrowid

    def updateQuery(self, query):
        cursor = self.dbcon.cursor()
        self.debugLog(query)
        values = cursor.execute(query)
        self.dbcon.commit()
        
    def insertQueryBlob(self, query, blob):
        cursor = self.dbcon.cursor()
        self.debugLog(query)
        values = cursor.execute(query, (blob,))
        self.dbcon.commit()
        return cursor.lastrowid
        
    def updateQueryBlob(self, query, blob):
        cursor = self.dbcon.cursor()
        self.debugLog(query)
        values = cursor.execute(query, (blob,))
        self.dbcon.commit()

    def executeQueryDictBlob(self, query):
        #self.dbcon.text_factory = lambda x: str(x, 'utf-8', 'ignore')
        cursor = self.dbcon.cursor()
        self.debugLog(query)
        results = cursor.execute(query)
        column_dict = {}
        result_list = []
        count = 0
        for columns in cursor.description:
            column_dict[columns[0]] = count
            count += 1
        result = results.fetchone()
        return result


    def executeQueryDict(self, query):
        #self.dbcon.text_factory = lambda x: str(x, 'utf-8', 'ignore')
        cursor = self.dbcon.cursor()
        self.debugLog(query)
        results = cursor.execute(query)
        column_dict = {}
        result_list = []
        count = 0
        for columns in cursor.description:
            column_dict[columns[0]] = count
            count += 1
        self.debugLog(str(results))
        for result in results:
            result_dict = {}
            for key in column_dict.keys():
                    result_dict[key] = result[column_dict[key]]
            result_list.append(result_dict)
        return result_list

def test_execBlob():
    myDB = WEBDB('../db/kb_1.db', {'logging':'on', 'type':'sqlite'})
    for i in range(1,200):
        query = "SELECT * FROM table_content where id="+str(i)
        print (query)
        data = myDB.executeQueryDictBlob(query)
        print (data)


#test_execBlob()
