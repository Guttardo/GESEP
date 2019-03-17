from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time
import mysql.connector
import datetime
import csv

#Conectanco ao Banco
bd = mysql.connector.connect(user='gesep', password='Q1w2e3rtghnjmk,.;!',host='127.0.0.1',database='gesep')
cursor = bd.cursor()

#Permissões para ler e criar no drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)
    # Call the Drive v3 API
    ins = "SELECT leitura, data from ldr where id='1k' and data>='2019-03-17 00:00:00' and data<='2019-03-17 23:59:59' order by data"  
    cursor.execute(ins)
    with open("ldr_1k_2019-03-17.csv", "w") as csv_file:              # Python 2 version
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Leitura', 'Data']) # write headers
        csv_writer.writerows(cursor)
    file_metadata = {
        'name': 'Testando Planilha',
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }
    media = MediaFileUpload('ldr_750_29-11.csv',
                            mimetype='text/csv',
                            resumable=True)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

if __name__ == '__main__':
    main()