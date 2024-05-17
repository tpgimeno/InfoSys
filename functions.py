from os import system
import subprocess
from prueba import *

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

