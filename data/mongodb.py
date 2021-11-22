import pymongo
import googlesheet#impota la hoja de calculo


# PASO 1: Conexión al Server de MongoDB Pasandole el host y el puerto
mongoClient = pymongo.MongoClient('mongodb://root:pass@localhost',27017)#cadena mongodb_pass
# PASO 2: Conexión a la base de 
# datos
db = mongoClient.sensor_db
# PASO 3: Obtenemos una coleccion para trabajar con ella
collection = db.sensor_tb
values = [
    ["id","value","type","fecha_hora"]]
#print(type(values))
cursor = collection.find()
for p in cursor:
    values.append([p["id"],p["value"],p["type"],p["fecha_hora"]])

def setRange(rows,columns,sheet_name):
     r=sheet_name+'!A1:'+str(columns)+str(rows)
     return r
#https://docs.google.com/spreadsheets/d/1cg7L4ohlF_l5kEzMCFbIgzEO1HHA8bpcs5TY7UyJ9ws/edit?usp=sharing
SPREADSHEET_ID = '1cg7L4ohlF_l5kEzMCFbIgzEO1HHA8bpcs5TY7UyJ9ws'
RANGE_NAME = setRange(len(values),chr(len(values[0])+64),"Hoja 1")
print(RANGE_NAME)
service = googlesheet.Connection(SPREADSHEET_ID,RANGE_NAME)
googlesheet.saveValues(service,values,SPREADSHEET_ID,RANGE_NAME)
#googlesheet.getValues(service,SPREADSHEET_ID,RANGE_NAME)
