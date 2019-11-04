import paho.mqtt.publish as publish
import config

publish.single(config.MQTT_PATH, "Hello World!", hostname=config.MQTT_SERVER)