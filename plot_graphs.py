import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time
import mysql.connector
import datetime
import csv

bd_cloud = mysql.connector.connect(user='root', password='q1w2e3rtghnjmk,.;!',host='35.198.12.124',database='gesep')
cursor = bd_cloud.cursor()

sensor = "piranometro"
dateBegin = ["'2018-11-28 00:00:00'","'2018-11-29 00:00:00'","'2018-11-30 00:00:00'","'2018-12-01 00:00:00'"]
dateEnd = ["'2018-11-28 23:59:59'","'2018-11-29 23:59:59'","'2018-11-30 23:59:59'","'2018-12-01 23:59:59'"]
date_arq = ["28-11","29-11","30-11","01-12"]

if(sensor=="ldr"):
    
    for i in range(0,len(date_arq)):
        res = "1k"
        ins = "SELECT leitura, data from "+ sensor +" where id='"+res+"' and data>="+dateBegin[i]+" and data<="+dateEnd[i]+" order by data"  
        cursor.execute(ins)
        with open("ldr_1k_"+date_arq[i]+".csv", "w") as csv_file:              # Python 2 version
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Leitura', 'Data']) # write headers
            csv_writer.writerows(cursor)
        res = "750"
        ins = "SELECT leitura, data from "+ sensor +" where id='"+res+"' and data>="+dateBegin[i]+" and data<="+dateEnd[i]+" order by data"  
        cursor.execute(ins)
        with open("ldr_470_"+date_arq[i]+".csv", "w") as csv_file:              # Python 2 version
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Leitura', 'Data']) # write headers
            csv_writer.writerows(cursor)
        res = "470"
        ins = "SELECT leitura, data from "+ sensor +" where id='"+res+"' and data>="+dateBegin[i]+" and data<="+dateEnd[i]+" order by data"  
        cursor.execute(ins)
        with open("ldr_750_"+date_arq[i]+".csv", "w") as csv_file:              # Python 2 version
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Leitura', 'Data']) # write headers
            csv_writer.writerows(cursor)
    
elif (sensor=="piranometro"):
    for i in range(0,len(date_arq)):
        ins = "SELECT tensao,leitura,data from "+ sensor +" where data>="+dateBegin[i]+" and data<="+dateEnd[i]+" order by data"
        cursor.execute(ins)
        with open("piranometro_"+date_arq[i]+".csv", "w") as csv_file:              # Python 2 version
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Tensão','Leitura', 'Data']) # write headers
            csv_writer.writerows(cursor)
elif (sensor=="dht"):
    for i in range(0,len(date_arq)):
        ins = "SELECT temp,umidade,data from "+ sensor +" where data>="+dateBegin[i]+" and data<="+dateEnd[i]+" order by data"
        cursor.execute(ins)
        with open("dht_"+date_arq[i]+".csv", "w") as csv_file:              # Python 2 version
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Temp','Umidade', 'Data']) # write headers
            csv_writer.writerows(cursor)
elif (sensor=="tenCorrente"):
    for i in range(0,len(date_arq)):
        ins = "SELECT tensaoPainel,tensaoSensor, correntePainel, correnteSensor,data from "+ sensor +" where data>="+dateBegin[i]+" and data<="+dateEnd[i]+" order by data"
        cursor.execute(ins)
        with open("tensao_corrente_"+date_arq[i]+".csv", "w") as csv_file:              # Python 2 version
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Tensao Painel','Tensao Sensor','Corrente Painel', 'Corrente Sensor', 'Data']) # write headers
            csv_writer.writerows(cursor)
else:
    ins = "SELECT tensao,leitura,data from "+ sensor +" where data>="+dateBegin+" and data<="+dateEnd+" order by data"
    cursor.execute(ins)
    
    with open("piranometro_27-11.csv", "w") as csv_file:              # Python 2 version
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Tensão','Leitura', 'Data']) # write headers
        csv_writer.writerows(cursor)
    dados = cursor.fetchall()
    
    plt.plot([data for leitura, data in dados], [leitura for leitura,data in dados])


