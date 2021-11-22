import ssl
import sys
import requests
import json
import datetime


#import paho.mqtt.client as mqtt
import paho.mqtt.client as mqtt

#este metodo se ejecutará cuando se realice una conexión al servidor MQTT
def on_connect(client,userdata,flags,rc):
    print("Connected (%s)" % client._client_id)
    #publish(topic, payload=None, qos=0, retain=False)
    client.subscribe(topic='estado/bebe',qos=2)

#este método se ejecuta cuando se recibe un mensaje
def on_message(client,userdata,msg):
    #print('topic:%s' %msg.topic)
    #print('payload:%s' %msg.payload)
    #print('qos:%d' %msg.qos)
    _d=msg.payload.decode("utf-8")
    d=_d.replace("'",'"')
    _payload = json.loads(d)
    _datetimeSensor = datetime.datetime.now()
    _payload['fecha_hora'] = _datetimeSensor.strftime("%Y-%m-%d %H:%M:%S")
    savedata(_payload)

def main():
    #se realiza la conexión con el servidor
    #client = mqtt.Client(client_id="dev1", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
    client = mqtt.Client(client_id="raspberry", clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    #client.username_pw_set("usuario","password")
    client.connect(host='192.168.0.13', port=1883,keepalive=60)
    client.loop_forever()

def savedata(payload):
    print(payload)
    headers = {'content-type': 'application/json'}
    r = requests.post('http://localhost:5000/sensores',headers=headers ,data=json.dumps(payload))
    print(r.text)

if __name__ == '__main__':
    main()
    #savedata()

sys.exit(0)