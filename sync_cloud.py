import mysql.connector
import datetime

bd_local = mysql.connector.connect(user='root', password='raspberry',host='192.168.0.140',database='sensores')
cursor = bd_local.cursor()

bd_cloud = mysql.connector.connect(user='root', password='q1w2e3rtghnjmk,.;!',host='35.198.12.124',database='sensores')
cursor2 = bd_cloud.cursor()


query = ("SELECT COD, leitura, data FROM bh1750 ")
cursor.execute(query)
registros = cursor.fetchall()
for (COD, leitura, data) in registros:
    ins = "INSERT INTO bh1750 (COD,leitura, data, sync) VALUES ('"+COD+"',"+str(leitura)+",'"+data.strftime("%Y-%m-%d %H:%M:%S")+"', 1)"
    cursor2.execute(ins)
    bd_cloud.commit()
    delet = "DELETE FROM bh1750 WHERE `COD` = '"+COD+"' "
    cursor.execute(delet)
    bd_local.commit()


query = ("SELECT COD, leitura, data FROM bmp180 ")
cursor.execute(query)
registros = cursor.fetchall()
for (COD, leitura, data) in registros:
    ins = "INSERT INTO bmp180 (COD,leitura, data, sync) VALUES ('"+COD+"',"+str(leitura)+",'"+data.strftime("%Y-%m-%d %H:%M:%S")+"', 1)"
    cursor2.execute(ins)
    bd_cloud.commit()
    delet = "DELETE FROM bmp180 WHERE `COD` = '"+COD+"' "
    cursor.execute(delet)
    bd_local.commit()


query = ("SELECT COD, id, leitura, data FROM LDR ")
cursor.execute(query)
registros = cursor.fetchall()
for (COD, id, leitura, data) in registros:
    ins = "INSERT INTO LDR (COD, id, leitura, data, sync) VALUES ('"+COD+"',"+str(id)+","+str(leitura)+",'"+data.strftime("%Y-%m-%d %H:%M:%S")+"', 1)"
    cursor2.execute(ins)
    bd_cloud.commit()
    delet = "DELETE FROM LDR WHERE `COD` = '"+COD+"' "
    cursor.execute(delet)
    bd_local.commit()


query = ("SELECT COD, leitura, data FROM temt6000 ")
cursor.execute(query)
registros = cursor.fetchall()
for (COD, leitura, data) in registros:
    ins = "INSERT INTO temt6000 (COD, leitura, data, sync) VALUES ('"+COD+"',"+str(leitura)+",'"+data.strftime("%Y-%m-%d %H:%M:%S")+"', 1)"
    cursor2.execute(ins)
    bd_cloud.commit()
    delet = "DELETE FROM temt6000 WHERE `COD` = '"+COD+"' "
    cursor.execute(delet)
    bd_local.commit()


query = ("SELECT COD, full, infra, lux, visivel, data FROM tsl2561 ")
cursor.execute(query)
registros = cursor.fetchall()
for (COD, full, infra, lux, visivel, data) in registros:
    ins = "INSERT INTO tsl2561 (COD, full, infra, lux, visivel, data, sync) VALUES ('"+COD+"',"+str(full)+","+str(infra)+","+str(lux)+","+str(visivel)+",'"+data.strftime("%Y-%m-%d %H:%M:%S")+"', 1)"
    cursor2.execute(ins)
    bd_cloud.commit()
    delet = "DELETE FROM tsl2561 WHERE `COD` = '"+COD+"' "
    cursor.execute(delet)
    bd_local.commit()

cursor.close()
cursor2.close()
bd_local.close()
bd_cloud.close()