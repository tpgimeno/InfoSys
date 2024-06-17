from os import system
import subprocess
import re
from intel import *
from mainboard import *
import bdagent

def getSystemInfo():    
    result = subprocess.run("systeminfo", capture_output=True, text=True)  
    file = open("info.txt", "+tw")
    file.write(result.stdout)
    file = open("info.txt", "+tr")
    lines = file.readlines()
    data = {}
    for i in range(1, len(lines)):
        if lines[i] == "":            
            del lines[i]
        else:            
            key = lines[i].split(":")[0].strip()           
            if len(lines[i].split(":")) > 2:
                value = lines[i].split(":")[2].strip()
                data[key] = value
            elif len(lines[i].split(":")) > 1:
                value = lines[i].split(":")[1].strip()
                data[key] = value
    return data

def getCpuWmicInfo():
    result = subprocess.run(["wmic", "cpu", "get", "/value"], capture_output=True, text=True)
    file = open("cpu.txt", "tw")
    file.write(result.stdout)
    file = open("cpu.txt", "r")
    lines = file.readlines()
    data = {}
    for line in lines:
        if line == "":
            del(line)
        key = line.split("=")[0]
        value = ""
        if len(line.split("=")) > 1:
            value = line.split("=")[1]
        data[key] = value
    return data

def normalizeString(string):
    cleanString = re.sub(r'[^a-zA-Z0-9()\s]', '', string)
    return cleanString

def depurateCpuName(name):
    data = name.split()
    result = []
    for item in data:
        if(item.find("(") > -1):            
            del(item)
        elif(item.find("@") > -1):
            del(item)
        elif(item.find("GHz") > -1):
            del(item)
        elif(item.find("CPU") > -1):
            del(item)
        else:
            result.append(item)
    return " ".join(result)

def depurateMainBoardManufacturer(name):    
    if(name.find("ASUSTeK") > -1):
        return("Asus")
    else:
        return(name)



def getMainBoardWmicInfo():
    result = subprocess.run(["wmic", "baseboard", "get", "/value"], capture_output=True, text=True)
    file = open("mainboard.txt", "tw")
    file.write(result.stdout)
    file = open("mainboard.txt", "r")
    lines = file.readlines()
    data = {}
    for line in lines:
        if line == "":
            del(line)
        key = line.split("=")[0]
        value = ""
        if len(line.split("=")) > 1:
            value = line.split("=")[1]
        data[key] = value
    return data

def filterManufacturers(manufacturer):    
    if(manufacturer.find("Genuine") != -1):
        manufacturer = manufacturer.replace("Genuine", "")        
    return manufacturer

def getMemoryWmicInfo():
    result = subprocess.run(["wmic", "memorychip", "get", "/value"], capture_output=True, text=True)
    file = open("memory.txt", "tw")
    file.write(result.stdout)
    file = open("memory.txt", "r")
    lines = file.readlines()
    data = {}
    for line in lines:        
        if len(line) < 2 or line=="\n":
            del(line)
            continue
        key = line.split("=")[0]
        value = ""
        
        if len(line.split("=")) > 1:
            value = line.split("=")[1]
        data[key] = value
    return data



def createTableCpuSpecsByMader(mader, cpu_info): 
    mader = mader.replace("\n", "")   
    tableName = "Cpu" + mader + "Specs"
    sql = "CREATE TABLE if not exists `" + tableName.lower() + "` (id INT AUTO_INCREMENT PRIMARY KEY"
    sql = sql + ", name VARCHAR(255) UNIQUE KEY"
    for item in cpu_info.keys():
        item = item.replace("(", " ")
        item = item.replace(")", " ")
        item = item.replace(" ", "_")
        sql = sql + ", " + item + " VARCHAR(255)"
    sql = sql + ")" 

    bdagent.cursor.execute(sql)

def verifyTableExists(tableName):
    bdagent.cursor.execute("show tables")
    for table in bdagent.cursor:
        if(tableName.lower() == table[0]):            
            return True            
    return False


def verifyCpuDataInDb(name, mader):    
    tableName = "cpu" + mader.strip() + "specs"    
    if(verifyTableExists(tableName.lower())):
        sql = "SELECT * FROM `" + tableName.lower() + "` WHERE `name` = '" + name + "'"        
        bdagent.cursor.execute(sql)
        result = bdagent.cursor.fetchall()
        if(result):
            return True
        else:
            return False
    else:
        return False
    
def verifyMainboardDataInDb(product, mader):    
    tableName = "mainboard" + mader.strip() + "specs"    
    if(verifyTableExists(tableName.lower())):
        sql = "SELECT * FROM `" + tableName.lower() + "` WHERE `Model` = '" + product.strip() + "'"        
        bdagent.cursor.execute(sql)
        result = bdagent.cursor.fetchall()
        if(result):
            return True
        else:
            return False
    else:
        return False



def insertCpuSpecsData(mader, cpu_info, cpu_name):
    mader = mader.replace("\n", "")    
    tableName = "Cpu" + mader.strip() + "Specs"
    if(verifyCpuDataInDb(cpu_name, mader) == True):
        sql = "UPDATE SET `" + tableName.lower() + "` "
        sql = sql + "name = %s , "
        keys = cpu_info.keys()
        for item in keys:
            item = item.replace("(", " ")
            item = item.replace(")", " ")
            item = item.replace(" ", "_")        
            sql = sql + "`" + item + "` =%s ,"    
        sql = sql.rstrip(sql[-1]) 
        sql = sql + " WHERE `name` = `" + cpu_name + "`"
    else:
        sql = "INSERT INTO `" + tableName.lower() + "` ("
        sql = sql + "name, "
        keys = cpu_info.keys()
        for item in keys:
            item = item.replace("(", " ")
            item = item.replace(")", " ")
            item = item.replace(" ", "_")        
            sql = sql + "`" + item + "` ,"

        sql = sql.rstrip(sql[-1])
        sql = sql + ") VALUES (" 
        sql = sql + "%s,"
        for item in keys:
            sql = sql + "%s,"

        sql = sql.rstrip(sql[-1]) 
        sql = sql + ")"
    values = []    
    values.append(cpu_name[0])
    for key in keys:
        values.append(cpu_info[key])
    val = tuple(values)
        
    bdagent.cursor.execute(sql, val)
    bdagent.conexion.commit()

def getCpuDbData(name, mader):
    tableName = "Cpu" + mader.strip() + "Specs"    
    sql = "SELECT * FROM `" + tableName.lower() + "` WHERE name = '" + name + "'"
    bdagent.cursor.execute(sql)
    content = bdagent.cursor.fetchall()
    keys = bdagent.cursor.column_names
    result = {}
    for i in range(0, len(keys)-1):
        result[keys[i]] = content[0][i]

    return result



def getMainboardDataDb(mader, name):
    tableName = "MainBoard" + mader.strip() + "Specs"    
    sql = "SELECT * FROM `" + tableName.lower() + "` WHERE `Model` = '" + name.strip() + "'"
    bdagent.cursor.execute(sql)
    content = bdagent.cursor.fetchall()
    keys = bdagent.cursor.column_names
    result = {}
    for i in range(0, len(keys)-1):
        result[keys[i]] = content[0][i]

    return result

    
def createMainboardSpecsTable(mader, mainboard_info):
    bdagent.cursor.reset()
    tableName = "MainBoard" + mader.strip() + "Specs"
    sql = "CREATE TABLE if not exists `" + tableName.lower() + "`(id INT AUTO_INCREMENT PRIMARY KEY"
    for item in mainboard_info.keys():        
            item = item.replace("(", " ")
            item = item.replace(")", " ")
            item = item.replace("/", "_")
            item = item.replace(" ", "_")
            item = item.replace("&", "")
            item = item.replace("-", "")               
            sql = sql + ", " + item + " TEXT"       
    sql = sql + ")"
    bdagent.cursor.execute(sql)

def insertMainboardSpecsData(mader, mainboard_info, product):
    tableName = "MainBoard" + mader.strip() + "Specs"
    if(verifyMainboardDataInDb(product, mader) == False):
        sql = "INSERT INTO `" + tableName.lower() + "` ("
        keys = mainboard_info.keys()
        for item in keys:
            item = item.replace("(", " ")
            item = item.replace(")", " ")
            item = item.replace("/", "_")
            item = item.replace(" ", "_")
            item = item.replace("&", "")
            item = item.replace("-", "")        
            sql = sql + "`" + item + "` ,"

        sql = sql.rstrip(sql[-1])
        sql = sql + ") VALUES ("     
        for item in keys:
            sql = sql + "%s,"

        sql = sql.rstrip(sql[-1]) 
        sql = sql + ")"
    else:
        sql = "UPDATE `" + tableName.lower() + "` SET "
        keys = mainboard_info.keys()
        for item in keys:
            item = item.replace("(", " ")
            item = item.replace(")", " ")
            item = item.replace("/", "_")
            item = item.replace(" ", "_")
            item = item.replace("&", "")
            item = item.replace("-", "")                 
            sql = sql + "`" + item + "` =%s ,"

        sql = sql.rstrip(sql[-1])
        sql = sql + " WHERE `Model` = '" + mainboard_info["Model"] + "'"        
    values = []
    
    for key in keys:    
        if(type(mainboard_info[key]) is list) :              
            line = " - ".join(mainboard_info[key])        
            line = line.replace(mainboard_info[key][0] + " - ", "")            
            values.append(line)
        else:
            values.append(mainboard_info[key])
    val = tuple(values)
        
    bdagent.cursor.execute(sql, val)
    bdagent.conexion.commit()
