import paho.mqtt.client as mqtt
import json
import os
import requests


class SubscribeInp:
    def __init__(self):
        # self.receive_obj = SubReceiver()
        PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        DATA_PATH = os.path.join(PATH, "config")
        with open(DATA_PATH + '/mqtt_config.json') as f:
            self.raw_data = json.load(f)
            self.mqtt_data = self.raw_data["mqtt"]
        broker_address = self.mqtt_data["broker_address"]
        mqtt_port = self.mqtt_data["mqtt_port"]
        mqtt_keepalive_interval = self.mqtt_data["mqtt_keepalive_interval"]
        client_id = self.mqtt_data["client_id"]
        self.mqtt_topic = self.mqtt_data["topic"]
        self.receiver_url = self.mqtt_data["receiver_url"]
        self.client = mqtt.Client(client_id)
        self.client.connect(broker_address, mqtt_port, mqtt_keepalive_interval)
        self.client.username_pw_set(self.mqtt_data["username"], self.mqtt_data["password"])

    #######################################
    # MQTT Functions
    #######################################

    def on_disconnect(self, client, userdata, flags, rc=0):
        m = "DisConnected flags" + "result code " + str(rc)
        print(m)
        client.connected_flag = False

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.client.connected_flag = True
            self.client.subscribe(self.mqtt_topic, 1)
            print("connected OK")
        else:
            self.client.bad_connection_flag = True
            print("Bad connection Returned code=", rc)

    def on_log(self, client, userdata, level, buf):
        print("log: ", buf)

    def on_message(self, client, userdata, message):
        ip_dict = {"Message received on ": message.topic,
                   "message received": str(message.payload.decode("utf-8")),
                   "message topic": message.topic,
                   "message qos": message.qos,
                   "message retain flag": message.retain}
        print(ip_dict)
        pub_response = requests.post(self.receiver_url, json=ip_dict)
        pub_result = pub_response.json()
        return pub_result
    ########################################

    def subscribe(self):
        try:
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_log = self.on_log
            self.client.on_message = self.on_message
        except Exception as e:
            print("Error Message: ", e)
        finally:
            self.client.loop_forever()
            print('Publisher connection closed.')


obj = SubscribeInp()
obj.subscribe()
