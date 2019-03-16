import mysql.connector
import datetime

print('Conectando ao banco local')
bd_local = mysql.connector.connect(user='gesep', password='Q1w2e3rtghnjmk,.;!',host='127.0.0.1',database='gesep')
cursor = bd_local.cursor()
print('Conectado!')
print('Conectando ao banco na nuvem')
bd_cloud = mysql.connector.connect(user='root', password='q1w2e3rtghnjmk,.;!',host='35.198.12.124',database='gesep')
cursor2 = bd_cloud.cursor()
print('Conectado!')

print('Iniciando sincronizacao:')
print('Sincronizando DHT...')
query = ("SELECT COD, temp, umidade, data FROM dht ")
cursor.execute(query)
registros = cursor.fetchall()
values = ",".join(map(str, [("'"+COD+"'") for (COD, temp, umidade, data) in registros]))
delet = "DELETE FROM dht WHERE `COD` IN ({})".format(values)
cursor.execute(delet)
bd_local.commit()
    
values = ', '.join(map(str, [(COD, str(temp), str(umidade), data.strftime("%Y-%m-%d %H:%M:%S")) for (COD, temp, umidade, data) in registros]))
ins = "INSERT INTO dht (COD, temp, umidade, data) VALUES {}".format(values)
cursor2.execute(ins)
bd_cloud.commit()

print('Concluido')
print('Sincronizando piranometro...')
query = ("SELECT COD, leitura, tensao, data FROM piranometro")
cursor.execute(query)
registros = cursor.fetchall()
values = ', '.join(map(str, [("'"+COD+"'") for (COD, leitura, tensao, data) in registros]))
delet = "DELETE FROM piranometro WHERE `COD` IN ( {} )".format(values)
cursor.execute(delet)
bd_local.commit()
    
values = ', '.join(map(str, [(COD, str(leitura), str(tensao), data.strftime("%Y-%m-%d %H:%M:%S")) for (COD, leitura, tensao, data) in registros]))
ins = "INSERT INTO piranometro (COD,leitura, tensao, data) VALUES {}".format(values)
cursor2.execute(ins)
bd_cloud.commit()
print('Concluido')    
print('Sincronizando LDRs...')

query = ("SELECT COD, id, leitura, data FROM ldr ")
cursor.execute(query)
registros = cursor.fetchall()
values = ', '.join(map(str, [("'"+COD+"'") for (COD, id, leitura, data) in registros]))
delet = "DELETE FROM ldr WHERE `COD` IN ( {} )".format(values)
cursor.execute(delet)
bd_local.commit()
    
values = ', '.join(map(str, [(COD, id, str(leitura), data.strftime("%Y-%m-%d %H:%M:%S")) for (COD, id, leitura, data) in registros]))
ins = "INSERT INTO ldr (COD, id, leitura, data) VALUES {}".format(values)
cursor2.execute(ins)
bd_cloud.commit()
print('Concluido')    
print('Sincronizando termopar...')

query = ("SELECT COD, leitura, tensao, data FROM termopar ")
cursor.execute(query)
registros = cursor.fetchall()
for (COD, leitura, tensao, data) in registros:
    ins = "INSERT INTO termopar (COD, leitura, tensao, data, sync) VALUES ('"+COD+"',"+str(leitura)+","+str(tensao)+",'"+data.strftime("%Y-%m-%d %H:%M:%S")+"', 1)"
    cursor2.execute(ins)
    bd_cloud.commit()
    delet = "DELETE FROM termopar WHERE `COD` = '"+COD+"' "
    cursor.execute(delet)
    bd_local.commit()
print('Concluido')
    
#print('Sincronizando tensao e corrente...')


#query = ("SELECT COD, tensaoPainel, tensaoSensor, correntePainel, correnteSensor, data FROM tenCorrente ")
#cursor.execute(query)
#registros = cursor.fetchall()
#cont = 0

#for (COD, tensaoPainel, tensaoSensor, correntePainel, correnteSensor, data) in registros:
	
#	ins = "INSERT IGNORE INTO tenCorrente (COD, tensaoPainel, tensaoSensor, correntePainel, correnteSensor, data, sync) VALUES ('"+COD+"',"+str(tensaoPainel)+","+str(tensaoSensor)+","+str(correntePainel)+","+str(correnteSensor)+",'"+data.strftime("%Y-%m-%d %H:%M:%S")+"', 1)"
#	cursor2.execute(ins)
#	bd_cloud.commit()
#	delet = "UPDATE tenCorrente SET SYNC='1' WHERE `COD` = '"+COD+"' "
#	cursor.execute(delet)
#	bd_local.commit()
	
	



cursor.close()
cursor2.close()
bd_local.close()
bd_cloud.close()

print('SINCRONIZACAO CONCLUIDA, VERIFIQUE O BANCO NA NUVEM')
