db = db.getSiblingDB("sensor_db");
db.sensor_tb.drop();

db.sensor_tb.insertMany([
    {
        "id": 1,
        "value": 4.0,
        "type": "H",
        "fecha_hora":""
    }
]);