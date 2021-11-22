import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']#alcanse uso de google data sheet

# The ID and range of a sample spreadsheet.
#SPREADSHEET_ID = '1G1T9PWxYHkAoVztsMDLI6rVGc6ilh9BB_5jC7rtdzHI'
#RANGE_NAME = 'Hoja 1!A1:B6'


#conexion a google sheet, permite hacer una autenticacion y hace una impresion del resultado
def Connection(SPREADSHEET_ID,RANGE_NAME):
    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES) # here enter the name of your downloaded JSON file -----valida las credenciales y
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service

#obtiene un valor(datos de la hoja de calculo: llama el servicio de google sheet y los valores de la hoja de calculo los consulta por el id)
def getValues(service,SPREADSHEET_ID,RANGE_NAME):
    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values_input = result_input.get('values', [])
    print(values_input)
    return values_input

#estructura de datos que se va a subir a google sheet
def saveValues(service, values,SPREADSHEET_ID,RANGE_NAME):
    # ejemplo de modelo para almacenar datos
    # values1 = [
    # ["Item", "Cost", "Stocked", "Ship Date"],
    # ["Wheel", "$20.50", "4", "3/1/2016"],
    # ["Door", "$15", "2", "3/15/2016"],
    # ["Engine", "$100", "1", "3/20/2016"],
    # ["Totals", '=SUM(B2:B4)', "=SUM(C2:C4)", "=MAX(D2:D4)"]]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW', 
        body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

