import paho.mqtt.client as mqtt
from random import randint
from datetime import datetime as dt

random_id = randint(1000, 1000000)

message_callbacks = list()


def register_callback(callback):
    print(f'Register callback')
    message_callbacks.append(callback)


def unregister_callback(callback):
    print(f'Unregister callback')
    message_callbacks.remove(callback)


def on_message(client, userdata, message):
    print(f"{dt.now()} Received: {message.topic} {message.payload}")
    print(f'MQTT: Current number of callbacks {len(message_callbacks)}')
    for callback in message_callbacks:
        try:
            callback(message.payload)
        except Exception as e:
            print(f'Exception Calling MQTT Callback {e}')


def on_subscribe(client, userdata, mid, reason_codes, properties):
    print(f"{dt.now()} Subscribed")


def on_connect(client, userdata, mid, reason_codes, properties):
    print(f'{dt.now()} Connected')
    client.subscribe('121212/#')


def on_disconnect(client, userdata, flags, reason_code, properties):
    print(f'{dt.now()} Disconnected')


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                          client_id=f"client-id-{randint(1000, 1000000)}",
                          # protocol=mqtt.MQTTv311, #  do not work with this
                          clean_session=True)

mqtt_client.username_pw_set("makeraccess_api", "makeraccess_C6G27KMkn")  # do not WORK at the moment
# client.tls_set(certfile=None,
#               keyfile=None,
#               cert_reqs=ssl.CERT_REQUIRED)

mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_subscribe = on_subscribe
mqtt_client.connect('itsp.htl-leoben.at', 1883)
# mqtt_client.loop_start()


'''
import paho.mqtt.client as mqtt
import ssl
from datetime import datetime as dt
def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe(topic="RXB")
def on_message(client, userdata, message, properties=None):
    print(
        f"{dt.now()} Received message {message.payload} on topic '{message.topic}' with QoS {message.qos}"
    )
def on_subscribe(client, userdata, mid, qos, properties=None):
    print(f"{dt.now()} Subscribed with QoS {qos}")
client = mqtt.Client(client_id="clientid", protocol=mqtt.MQTTv311, clean_session=True)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.username_pw_set(username="username", password="password")
client.tls_set(ca_certs="cacerts/isrgrootx1.pem")
client.connect(host="example.cedalo.cloud", port=8883, keepalive=60)
client.loop_forever()
'''
