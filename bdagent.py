import mysql.connector
import pymysql
import time

conexion=mysql.connector.connect(host="localhost", user="root", passwd="")
cursor=conexion.cursor()
cursor.execute("CREATE DATABASE if not exists infosys")
conexion.close()   

#RECONECTAMOS CON LA BASE DE DATOS SELECCIONADA

conexion=mysql.connector.connect(host="localhost", user="root", passwd="",database="infosys", consume_results=True)
cursor=conexion.cursor()
dictcursor=conexion.cursor(pymysql.cursors.DictCursor)

#CREAMOS LAS TABLAS BASE

cursor.execute("CREATE TABLE if not exists cpu_manufacturers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), image VARCHAR(255))")
cursor.execute("CREATE TABLE if not exists mainboard_manufacturers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), image VARCHAR(255))")
cursor.execute("CREATE TABLE if not exists memory_manufacturers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), image VARCHAR(255), code INT(4))")


