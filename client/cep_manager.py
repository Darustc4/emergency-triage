import pika # RabbitMQ
import json
from threading import Thread
import re

def connection_factory():
    # These classes will publish events to a RabbitMQ server and sub to them. Right now it is local and unsecured. (Please don't store actual passwords in source code)
    # We are using WSL - the IP to connect to RabbitMQ on the host machine is not localhost. Use cat /etc/resolv.conf to know which (nameserver).
    # Manager at http://localhost:15672/. Endpoint at http://172.31.144.1:5672 (smartdata:smartdata). Queue 'Messages'. Routing 'Messages'.
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('172.31.144.1', 5672, '/', pika.PlainCredentials('smartdata', 'smartdata'), heartbeat=600, blocked_connection_timeout=300))
        channel = connection.channel()
    except pika.exceptions.AMQPConnectionError as e:
        raise ConnectionError("Could not connect to RabbitMQ. Is it running?") from e

    return connection, channel

class ConnectionError(Exception):
    pass

class PikaSubscriber():
    exchange_name = ''

    def __init__(self, *args, **kwargs):
        self.conn, self.channel = connection_factory()

    def consume(self, callback):
        for method_frame, properties, body in self.channel.consume('MuleOut'):
            self.channel.basic_ack(method_frame.delivery_tag)

            s = body.decode("utf-8") # Cursed JSON: https://stackoverflow.com/questions/68682209/parse-json-without-quotes-in-python
            s = re.sub('\s', '', s) # Remove whitespace
            s = re.sub('(\w+)', '"\g<1>"', s) # Add quotes around keys and vals
            s = re.sub('=', ':', s) # Replace = with :

            callback(json.loads(s)["stmt0_out0"])

    def close(self):
        self.conn.add_callback_threadsafe(self._close_callback)

    def _close_callback(self):
        self.channel.stop_consuming()
        self.channel.close()
        self.conn.close()

class Cep_manager:
    def __init__(self):
        self.pattern_cb = None
        self.connection = None
        self.channel = None

        self.conn, self.channel = connection_factory()
        self.consumer = None

    def start_consuming(self, pattern_cb):
        self.pattern_cb = pattern_cb

        # Lauch thread for subscriber
        subscriber = Thread(target=self._subscribe, args=(pattern_cb,))
        subscriber.start()

    def _subscribe(self, callback):
        self.consumer = PikaSubscriber()
        self.consumer.consume(callback)

    def publish_patient(self, patient):
        body = json.dumps({
            "eventTypeName": "Patient",
            "patient": patient.id,
            "ssn": patient.ssn if patient.ssn != "" else None,
            "age": int(patient.age)*12 if patient.age != "" else None, # Months
            "is_male": patient.is_male,
            "latitude": patient.latitude if patient.latitude != "" else None,
            "longitude": patient.longitude if patient.longitude != "" else None,
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
            "eventTypeName": "ConsciousnessLevel",
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
        self.channel.basic_publish(exchange='', routing_key=queue, body=body)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.channel.close()
        self.conn.close()

        if self.consumer:
            self.consumer.close()
