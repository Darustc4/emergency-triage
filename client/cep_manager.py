import pika # RabbitMQ
import json

class ConnectionError(Exception):
    pass

class Cep_manager:
    # This class will publish events to a RabbitMQ server. Right now it is local and unsecured. (Please don't store actual passwords in source code)
    # We are using WSL - the IP to connect to RabbitMQ on the host machine is not localhost. Use cat /etc/resolv.conf to know which (nameserver).
    # Manager at http://localhost:15672/. Endpoint at http://172.31.144.1:5672 (smartdata:smartdata). Queue 'Messages'. Routing 'Messages'.
    def __init__(self) -> None:
        self._connect()

    def _connect(self):
        if not self.connection or self.connection.is_closed:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters('172.31.144.1', 5672, '/', pika.PlainCredentials('smartdata', 'smartdata')))
                self.channel = self.connection.channel()
            except pika.exceptions.AMQPConnectionError as e:
                raise ConnectionError("Could not connect to RabbitMQ. Is it running?") from e

    def publish_patient(self, patient):
        body = json.dumps({
            "eventTypeName": "Patient",
            "patient": patient.id,
            "ssn": patient.ssn,
            "age": patient.age,
            "is_male": patient.is_male,
            "latitude": patient.latitude,
            "longitude": patient.longitude
        })
        self._publish_to_queue('Messages', body)

    def publish_life_threat(self, id, life_threat_id):
        body = json.dumps({
            "eventTypeName": "LifeThreat",
            "patient": id,
            "type": life_threat_id
        })
        self._publish_to_queue('Messages', body)

    def publish_consciousness(self, id, consciousness_id):
        body = json.dumps({
            "eventTypeName": "Consciousness",
            "patient": id,
            "type": consciousness_id
        })
        self._publish_to_queue('Messages', body)

    def publish_haemorrhage(self, id, haemorrhage_id):
        body = json.dumps({
            "eventTypeName": "Haemorrhage",
            "patient": id,
            "type": haemorrhage_id
        })
        self._publish_to_queue('Messages', body)

    def publish_temperature(self, id, temperature_float):
        body = json.dumps({
            "eventTypeName": "Temperature",
            "patient": id,
            "value": temperature_float
        })
        self._publish_to_queue('Messages', body)

    def publish_pain_level(self, id, pain_level_id):
        body = json.dumps({
            "eventTypeName": "Pain",
            "patient": id,
            "type": pain_level_id
        })
        self._publish_to_queue('Messages', body)

    def publish_specific_symptom(self, id, symptom_name):
        body = json.dumps({
            "eventTypeName": "Symptom",
            "patient": id,
            "name": symptom_name
        })
        self._publish_to_queue('Messages', body)

    def _publish_to_queue(self, queue, body):
        print("Publishing to queue " + queue + ": " + body)
        self._connect()
        self.channel.basic_publish(exchange='', routing_key=queue, body=body)
