import serial
import mysql.connector

def main():

	try:
		bd = mysql.connector.connect(user='gesep', password='Q1w2e3rtghnjmk,.;!',host='127.0.0.1',database='gesep')
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
				buffer = ser.read(1)
				temp = str(ser.read(int(buffer)))
				buffer = ser.read(1)
				umid = str(ser.read(int(buffer)))
				insert = ("INSERT INTO dht (COD, temp, umidade) VALUES (uuid(),"+temp+","+umidade+")")
				cursor.execute(insert)
			elif ident == 'b':
				buffer = ser.read(1)
				leitura = str(ser.read(int(buffer)))
				insert = ("INSERT INTO ldr (COD, id, leitura) VALUES (uuid(),'1k',"+leitura+")")
				cursor.execute(insert)
			elif ident == 'c':
				buffer = ser.read(1)
				leitura = str(ser.read(int(buffer)))
				insert = ("INSERT INTO ldr (COD, id, leitura) VALUES (uuid(),'750',"+leitura+")")
				cursor.execute(insert)
			elif ident == 'd':
				buffer = ser.read(1)
				leitura = str(ser.read(int(buffer)))
				insert = ("INSERT INTO ldr (COD, id, leitura) VALUES (uuid(),'470',"+leitura+")")
				cursor.execute(insert)
			elif ident == 'e':
				buffer = ser.read(1)
				cpainel = str(ser.read(int(buffer)))
				buffer = ser.read(1)
				csensor = str(ser.read(int(buffer)))
				buffer = ser.read(1)
				tpainel = str(ser.read(int(buffer)))
				buffer = ser.read(1)
				tsensor = str(ser.read(int(buffer)))
				insert = ("INSERT INTO tenCorrent (COD, correntePainel, correnteSensor, tensaoPainel, tensaoSensor) VALUES (uuid(),"+cpainel+","+csensor+","+tpainel+","+tsensor+")")
				cursor.execute(insert)
			elif ident == 'f':
				buffer = ser.read(1)
				ir = str(ser.read(int(buffer))) 
				insert = ("INSERT INTO piranometro (COD,leitura) VALUES (uuid(),"+ir+")") 
				cursor.execute(insert)
			elif ident == 'g':
				buffer = ser.read(1)
				leitura = str(ser.read(int(buffer)))
				insert = ("INSERT INTO termopar (COD,leitura) VALUES (uuid(),"+leitura+")")
				cursor.execute(insert)
			bd.commit()
	except:
		print('deu merda')

main()
