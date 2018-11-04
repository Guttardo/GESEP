import serial
import mysql.connector

bd = mysql.connector.connect(user='root', password='raspberry',host='192.168.0.140',database='sensores')
#bd = mysql.connector.connect(user='root', password='raspberry',host='10.0.0.150',database='sensores')
cursor = bd.cursor()

ser = serial.Serial("/dev/ttyS0",9600)

while(True):
	verifica_inicio = ser.read(1)
	if(verifica_inicio=='T'):
		break

while(True):
	ident = ser.read(1)
	if ident == 'a':
		buf = ser.read(1)
		leitura = str(ser.read(int(buf)))
		ins = ("INSERT INTO bh1750 (COD,leitura) VALUES (uuid(),"+leitura+")")
		cursor.execute(ins)
	elif ident == 'b':
		buf = ser.read(1)
		leitura = str(ser.read(int(buf)))
		ins = ("INSERT INTO bmp180 (COD,leitura) VALUES (uuid(),"+leitura+")")
		cursor.execute(ins)
	elif ident == 'c':
		buf = ser.read(1)
		leitura = str(ser.read(int(buf)))
		ins = ("INSERT INTO LDR (COD,id,leitura) VALUES (uuid(),'1',"+leitura+")")
		cursor.execute(ins)
	elif ident == 'd':
		buf = ser.read(1)
		print("O buffer foi: "+buf)
		leitura = str(ser.read(int(buf)))
		ins = ("INSERT INTO LDR (COD,id,leitura) VALUES (uuid(),'2',"+leitura+")")
		cursor.execute(ins)
	elif ident == 'e':
		buf = ser.read(1)
		leitura = str(ser.read(int(buf)))
		ins = ("INSERT INTO LDR (COD,id,leitura) VALUES (uuid(),'3',"+leitura+")")
		cursor.execute(ins)
	elif ident == 'f':
		buf = ser.read(1)
		ir = str(ser.read(int(buf))) 
		buf = ser.read(1)
		full = str(ser.read(int(buf))) 
		buf = ser.read(1)
		vi = str(ser.read(int(buf))) 
		buf = ser.read(1)
		lx = str(ser.read(int(buf)))
		ins = ("INSERT INTO tsl2561 (COD,full,infra,visivel,lux) VALUES (uuid(),"+full+","+ir+","+vi+","+lx+")") 
		cursor.execute(ins)
	elif ident == 'g':
		buf = ser.read(1)
		leitura = str(ser.read(int(buf)))
		ins = ("INSERT INTO temt6000 (COD,leitura) VALUES (uuid(),"+leitura+")")
		cursor.execute(ins)
	bd.commit()

cursor.close()
bd.close()
