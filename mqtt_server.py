import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import config

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(config.MQTT_CHANNEL_GET + "+")
    return

def on_message(client, userdata, msg):
    uid = msg.topic.split('/')[2]
    print("UID: {}, Message: {}".format(uid, str(msg.payload)))
    return

client = mqtt.Client()

def start_server():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(config.MQTT_SERVER, 1883, 60)

    client.loop_start()
    return

def stop_server():
    client.loop_stop()
    return

def send_message(cmd, uid):
    channel = config.MQTT_CHANNEL_PUT + uid
    print("Sending command: {} to channel {}".format(cmd, channel))
    publish.single(channel, cmd, hostname=config.MQTT_SERVER)
    return

def menu():
    main_menu = ['q to quit',
                'p to publish']

    start_server()
    while True:
        print("\tMQTT SERVER TEST MENU")
        for option in main_menu:
            print(option)

        choice = input()
        if choice is 'q':
            print("Stopping the server...")
            stop_server()
            return
        elif choice is 'p':
            cmd = input("Enter message:\n")
            uid = input("Send UID of rpi to send to:\n")
            send_message(cmd, uid)
    return

if __name__ == "__main__":
    menu()