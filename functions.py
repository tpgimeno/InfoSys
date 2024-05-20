from os import system
import subprocess
import re
from intel import *
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
            print(lines[i])
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

def getCpuInfo():
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
    return result


def getMainBoardInfo():
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

def getMemoryInfo():
    result = subprocess.run(["wmic", "memorychip", "get", "/value"], capture_output=True, text=True)
    file = open("cpu.txt", "tw")
    file.write(result.stdout)
    file = open("memory.txt", "r")
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

def createTableCpuSpecsByMader(mader, cpu_info): 
    mader = mader.replace("\n", "")   
    tableName = mader + "Specs"
    sql = "CREATE TABLE if not exists `" + tableName + "` (id INT AUTO_INCREMENT PRIMARY KEY"
    for item in cpu_info.keys():
        item = item.replace("(", " ")
        item = item.replace(")", " ")
        item = item.replace(" ", "_")
        sql = sql + ", " + item + " VARCHAR(255)"
    sql = sql + ")" 

    bdagent.cursor.execute(sql)

def insertCpuSpecsData(mader, cpu_info):
    mader = mader.replace("\n", "")
    mader = mader.replace(" ", "_")
    mader = normalizeString(mader)
    tableName = mader.strip() + "Specs"
    sql = "INSERT INTO `" + tableName + "` ("
    keys = cpu_info.keys()
    for item in keys:
        item = item.replace("(", " ")
        item = item.replace(")", " ")
        item = item.replace(" ", "_")
        sql = sql + "`" + item + "` ,"

    sql = sql.rstrip(sql[-1])
    sql = sql + ") VALUES (" 
    for item in keys:
        sql = sql + "%s,"

    sql = sql.rstrip(sql[-1]) 
    sql = sql + ")"
    values = cpu_info.values()
    
    
    
    bdagent.cursor.execute(sql, values)