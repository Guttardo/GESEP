import serial
import mysql.connector
import time

def main():

	try:
		print('Conectando ao banco')
		bd = mysql.connector.connect(user='gesep', password='Q1w2e3rtghnjmk,.;!',host='127.0.0.1',database='gesep')
		#bd = mysql.connector.connect(user='root', password='raspberry',host='10.0.0.150',database='sensores')
		cursor = bd.cursor()
		print('Sucesso!')
		print('Iniciando comunicacao serial')
		ser = serial.Serial("/dev/ttyUSB0",115200)
		print(ser.name)

		while(True):
			verifica_inicio = ser.read(1).decode('utf-8')
			if(verifica_inicio=='T'):
				break
		print('Sucesso!')
		print('Coletando dados...')
		while(True):
			ident = ser.read(1).decode('utf-8')
			if ident == 'a':
				buffer = ser.read(1).decode('utf-8')
				umid = ser.read(int(buffer)).decode('utf-8')
				print('\n === Dados coletados ===')
				print('Umidade (DHT): {}%'.format(umid))
				buffer = ser.read(1).decode('utf-8')
				temp = ser.read(int(buffer)).decode('utf-8')
				print('Temperatura (DHT): {}°C'.format(temp))
				if(temp != ' NAN'):
					insert = ("INSERT INTO dht (COD, temp, umidade) VALUES (uuid(),"+temp+","+umid+")")
					cursor.execute(insert)
			elif ident == 'b':
				buffer = ser.read(1).decode('utf-8')
				leitura = ser.read(int(buffer)).decode('utf-8')
				print('LDR 1k: {}V'.format(leitura))
				insert = ("INSERT INTO ldr (COD, id, leitura) VALUES (uuid(),'1k',"+leitura+")")
				cursor.execute(insert)
			elif ident == 'c':
				buffer = ser.read(1).decode('utf-8')
				leitura = ser.read(int(buffer)).decode('utf-8')
				print('LDR 470: {}V'.format(leitura))
				insert = ("INSERT INTO ldr (COD, id, leitura) VALUES (uuid(),'470',"+leitura+")")
				cursor.execute(insert)
			elif ident == 'd':	
				buffer = ser.read(1).decode('utf-8')
				leitura = ser.read(int(buffer)).decode('utf-8')
				print('LDR 760: {}V'.format(leitura))
				insert = ("INSERT INTO ldr (COD, id, leitura) VALUES (uuid(),'760',"+leitura+")")
				cursor.execute(insert)
			elif ident == 'e':
				buffer = ser.read(1).decode('utf-8')
				cpainel = ser.read(int(buffer)).decode('utf-8')
				buffer = ser.read(1).decode('utf-8')
				csensor = ser.read(int(buffer)).decode('utf-8')
				buffer = ser.read(1).decode('utf-8')
				tpainel = ser.read(int(buffer)).decode('utf-8')
				buffer = ser.read(1).decode('utf-8')
				tsensor = ser.read(int(buffer)).decode('utf-8')
				print('Corrente do painel: {}A'.format(cpainel))
				print('Tensão do painel: {}V'.format(tpainel))
				insert = ("INSERT INTO tenCorrente (COD, correntePainel, correnteSensor, tensaoPainel, tensaoSensor) VALUES (uuid(),"+cpainel+","+csensor+","+tpainel+","+tsensor+")")
				cursor.execute(insert)
			elif ident == 'f':
				buffer = ser.read(1).decode('utf-8')
				ir = ser.read(int(buffer)).decode('utf-8')
				print('Irradiância (PIR): {} W/m2'.format(ir))
				buffer = ser.read(1).decode('utf-8')
				tensao = ser.read(int(buffer)).decode('utf-8')
				insert = ("INSERT INTO piranometro (COD, leitura, tensao) VALUES (uuid(),"+ir+","+tensao+")") 
				cursor.execute(insert)
			elif ident == 'g':
				buffer = ser.read(1).decode('utf-8')
				leitura = ser.read(int(buffer)).decode('utf-8')
				buffer = ser.read(1).decode('utf-8')
				tensao = ser.read(int(buffer)).decode('utf-8')
				insert = ("INSERT INTO termopar (COD, leitura, tensao) VALUES (uuid(),"+leitura+","+tensao+")")
				cursor.execute(insert)
			bd.commit()
	except:
		time.sleep(10)
		print('Erro na coleta, reiniciando conexões...')
		main()		
	
main()
