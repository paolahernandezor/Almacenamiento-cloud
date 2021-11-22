#include <Dhcp.h>
#include <Dns.h>
#include <Ethernet.h>
#include <EthernetClient.h>
#include <EthernetServer.h>
#include <EthernetUdp.h>

#include <PubSubClient.h>

#include <MqttClient.h>


 //Direccion MAC
byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0xA0, 0x88 };
IPAddress ethernet (192, 168, 56, 1);

//**************************************
//*********** MQTT CONFIG **************
//**************************************
const char *mqtt_server = "192.168.0.13";
const int mqtt_port =  1883;
const char *mqtt_user = "usuario";
const char *mqtt_pass = "password";
const char *root_topic_subscribe = "estado/bebe/in";
const char *root_topic_publish = "estado/bebe";

//**************************************
//*********** GLOBALES   ***************
//**************************************
EthernetClient ethClient;
PubSubClient client(ethClient);
char msg[40];
const int Sensor_Microfono = A0;
int value = 0;

//************************
//** F U N C I O N E S ***
//************************
void callback(char* topic, byte* payload, unsigned int length);
void reconnect();
void setup_ethernet();

void setup() {
  Serial.begin(9600);
  if (Ethernet.begin(mac) ==0){
    Serial.println("fallo configuracion ethernet");
  }
  setup_ethernet();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  pinMode(Sensor_Microfono, INPUT); 
}


void loop(){
  
  if (!client.connected()) {
    reconnect();
  }
  value = analogRead(Sensor_Microfono);  //lectura digital de pin 
  //mandar mensaje a puerto serie en función del valor leido
  if (value <=850) {
    Serial.println("bebe Dormido");
  }
  else if ((value>850) and (value<860)){
    Serial.println("bebe Despierto");
  }
  else{
    Serial.println("bebe llorando");
  } 
  float randNumber = random(1, 10);
  String str = "{'id':1,'value':"+String(randNumber)+",'type':'A'}";
  str.toCharArray(msg,40);
  if (client.connected()){
    client.publish(root_topic_publish,msg);
    
  }
  delay(1000);
  client.loop();
}



//*****************************
//***    CONEXION ETHERNET     ***
//*****************************
void setup_ethernet(){
  delay(10);
  Serial.println("Conectado a Ethernet!");
  Serial.println("Dirección IP: ");
  Serial.println(Ethernet.localIP());
 
}

//*****************************
//***    CONEXION MQTT      ***
//*****************************

void reconnect() {

  while (!client.connected()) {
    Serial.print("Intentando conexión Mqtt...");
    // Creamos un cliente ID
    String clientId = "Arduino";
    clientId += String(random(0xffff), HEX);
    // Intentamos conectar
    if (client.connect(clientId.c_str(),mqtt_user,mqtt_pass)) {
      Serial.println("Conectado!");
      // Nos suscribimos
      if(client.subscribe(root_topic_subscribe)){
        Serial.println("Suscripcion ok");
      }else{
        Serial.println("fallo Suscripciión");
      }
    } else {
      Serial.print("falló :( con error -> ");
      Serial.print(client.state());
      Serial.println(" Intentamos de nuevo en 5 segundos");
      delay(5000);
    }
  }
}


//*****************************
//***       CALLBACK        ***
//*****************************

void callback(char* topic, byte* payload, unsigned int length){
  String incoming = "";
  Serial.print("Mensaje recibido desde -> ");
  Serial.print(topic);
  Serial.println("");
  for (int i = 0; i < length; i++) {
    incoming += (char)payload[i];
  }
  incoming.trim();
  Serial.println("Mensaje -> " + incoming);

}
