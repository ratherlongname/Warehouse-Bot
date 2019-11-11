def server_message_handler(client, userdata, msg):
    # TODO
    uid = msg.topic.split('/')[2]
    message = str(msg.payload)
    print("UID: {}, Message: {}".format(uid, message))
    return

def start_server():
    import mqtt_server
    mqtt_server.start_server(server_message_handler)
    return

def run_server():
    start_server()
    return

if __name__ == "__main__":
    run_server()