from flask import Flask, jsonify, request
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
    db = client["sensor_db"]
    return db

@app.route('/')
def ping_server():
    return "Hola mi API REST para IOT"

@app.route('/sensores',methods=['GET','POST'])
def man_sensores():
    if request.method=='GET':
        db=""
        try:
            db = get_db()
            _sensores = db.sensor_tb.find()
            #{'id':1,'value':"+String(randNumber)+",type:'A'}
            sensores = [{"id": sensor["id"], "value": sensor["value"],"type": sensor["type"],"fecha_hora":sensor["fecha_hora"]} for sensor in _sensores]
            return jsonify({"sensores": sensores})
        except:
            pass
        finally:
            if type(db)==MongoClient:
                db.close()
    else:# POST 
        db=""
        try:
            db = get_db()
            #insertar datos en bd sensor_tb
            db.sensor_tb.insert_one(request.json)
            return jsonify({"respuesta": "OK"})
        except:
            pass
        finally:
            if type(db)==MongoClient:
                db.close()



if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)