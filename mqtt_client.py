import config


def on_connect(client_local, userdata, flags, rc):  # pylint: disable=unused-argument
    print("Connected with result code " + str(rc))
    client_local.subscribe(config.MQTT_CHANNEL_PUT + config.UID)


def start_mqtt(client, on_message_func):

    client.on_connect = on_connect
    client.on_message = on_message_func
    client.connect(config.MQTT_SERVER, 1883, 60)
    client.loop_start()


def stop_mqtt(client):
    client.loop_stop()


def send_message(client, msg):
    channel = config.MQTT_CHANNEL_GET + config.UID
    print(f"Sending message: {msg} to channel {channel}")
    client.publish(channel, msg)


if __name__ == "__main__":
    raise Exception("This is not a top level module")
