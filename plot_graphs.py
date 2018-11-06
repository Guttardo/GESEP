import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time
import mysql.connector
import datetime

bd_cloud = mysql.connector.connect(user='root', password='q1w2e3rtghnjmk,.;!',host='35.198.12.124',database='sensores')
cursor = bd_cloud.cursor()

sensor = "tsl2561"
dateBegin = "'2018-10-16 15:37:00'"
dateEnd = "'2018-10-16 18:00:00'"

if(sensor=="LDR"):
    ins = "SELECT leitura, data from "+ sensor +" where id=1 and data>="+dateBegin+" and data<="+dateEnd+" order by data"

    cursor.execute(ins)
    ldr2 = cursor.fetchall()
    ins = "SELECT leitura, data from "+ sensor +" where id=2 and data>="+dateBegin+" and data<="+dateEnd+" order by data"
    cursor.execute(ins)
    ldr1 = cursor.fetchall()
    ins = "SELECT leitura, data from "+ sensor +" where id=3 and data>="+dateBegin+" and data<="+dateEnd+" order by data"
    cursor.execute(ins)
    ldr3 = cursor.fetchall()
    plt.plot([data for leitura, data in ldr1], [leitura for leitura,data in ldr1],label='LDR 1', color='blue')
    plt.plot([data for leitura, data in ldr2], [leitura for leitura,data in ldr2],label='LDR 2', color='green')
    plt.plot([data for leitura, data in ldr3], [leitura for leitura,data in ldr3],label='LDR 3', color='red')
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
    ins = "SELECT leitura, data from "+ sensor +" where data>="+dateBegin+" and data<="+dateEnd+" order by data"
    cursor.execute(ins)
    dados = cursor.fetchall()
    plt.plot([data for leitura, data in dados], [leitura for leitura,data in dados])

plt.gcf().autofmt_xdate()
plt.xlabel('Hora')
plt.ylabel('Leitura')
plt.title(sensor)
plt.show()