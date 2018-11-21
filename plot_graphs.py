import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time
import mysql.connector
import datetime
import csv

bd_cloud = mysql.connector.connect(user='gesep', password='Q1w2e3rtghnjmk,.;!',host='127.0.0.1',database='gesep')
cursor = bd_cloud.cursor()

sensor = "tenCorrente"
dateBegin = "'2018-11-14 11:10:00'"
dateEnd = "'2018-11-14 23:59:00'"

if(sensor=="ldr"):
    res = "470"
    ins = "SELECT leitura, data from "+ sensor +" where id='"+res+"' and data>="+dateBegin+" and data<="+dateEnd+" order by data"
	
    cursor.execute(ins)
    with open("ldr1k.csv", "w") as csv_file:              # Python 2 version
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Leitura', 'Data']) # write headers
        csv_writer.writerows(cursor)
    ldr470 = cursor.fetchall()
    
    ins = "SELECT leitura from piranometro" +" where data>="+dateBegin+" and data<="+dateEnd+" order by leitura"
    cursor.execute(ins)
    piranometro = cursor.fetchall()
    plt.plot([leitura for leitura in ldr470], [leitura for leitura in piranometro],label='LDR 1 Kohm', color='blue')
    plt.legend()
elif (sensor=="tsl2561"):
    ins = "SELECT full, infra, lux, visivel, data from "+ sensor +" where data>="+dateBegin+" and data<="+dateEnd+" order by data"
    cursor.execute(ins)
    dados = cursor.fetchall()
    
    plt.plot([data for full,infra,lux,visivel,data in dados], [full for full,infra,lux,visivel,data in dados],label='FULL', color='black')
    plt.plot([data for full,infra,lux,visivel,data in dados], [visivel for full,infra,lux,visivel,data in dados],label='Visível', color='deepskyblue')
    plt.plot([data for full,infra,lux,visivel,data in dados], [infra for full,infra,lux,visivel,data in dados],label='Infra-Vermelho', color='red')
    plt.plot([data for full,infra,lux,visivel,data in dados], [lux for full,infra,lux,visivel,data in dados],label='Lux', color='green')
    plt.legend()
else:
    ins = "SELECT tensaoPainel,correntePainel,data from "+ sensor +" where data>="+dateBegin+" and data<="+dateEnd+" order by data"
    cursor.execute(ins)
    
    with open("out.csv", "w") as csv_file:              # Python 2 version
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Tensão','Corrente', 'Data']) # write headers
        csv_writer.writerows(cursor)
    dados = cursor.fetchall()
    
    plt.plot([data for leitura, data in dados], [leitura for leitura,data in dados])

plt.gcf().autofmt_xdate()
plt.xlabel('Tempo')
plt.ylabel('Irradiância Piranômetro (W/m2)')
plt.title('Irradiância')
plt.show()
