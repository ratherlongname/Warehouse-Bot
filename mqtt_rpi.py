import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import config
import uuid

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe(config.MQTT_CHANNEL_PUT + config.uid)

def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()

def generate_uid():
	uid = uuid.uuid1().hex
	config.uid = uid
	print("Our UID is: ", config.uid)

def start_server(on_message_func = on_message):
	client.on_connect = on_connect
	client.on_message = on_message_func
	client.connect(config.MQTT_SERVER, 1883, 60)
	client.loop_start()

def stop_server():
	client.loop_stop()

def send_message(msg):
	channel = config.MQTT_CHANNEL_GET + config.uid
	print("Sending message: {} to channel {}".format(msg, channel))
	publish.single(channel, msg, hostname=config.MQTT_SERVER)

def send_barrier(msg):
	channel = config.MQTT_CHANNEL_BARRIER
	print("Sending message: {} to channel {}".format(msg, channel))
	publish.single(channel, msg, hostname=config.MQTT_SERVER)

def menu():
	main_menu = ['q to quit',
				'p to publish']

	generate_uid()
	start_server()
	while True:
		print("\tMQTT RPI TEST MENU")
		for option in main_menu:
			print(option)

		choice = input()
		if choice is 'q':
			print("Stopping the listener...")
			stop_server()
			return
		elif choice is 'p':
			msg = input("Enter message:\n")
			send_message(msg)

if __name__ == "__main__":
	menu()
