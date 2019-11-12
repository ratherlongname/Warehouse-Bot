def message_to_coordinates(message):
    # TODO
    return (0, 0)

def server_message_handler(client, userdata, msg):
    # TODO
    message = str(msg.payload)
    channel = msg.topic.split('/')
    if channel[0] is "block":
        graph.add_barrier(message_to_coordinates(message))
    elif channel[0] is "rpi":
        curr_loc = message_to_coordinates(message)
        uid = msg.topic.split('/')[2]
        print("UID: {}, Message: {}".format(uid, message))
        if uid not in all_rpis:
            graph.add_barrier(curr_loc)
            all_rpis[uid] = {'loc':curr_loc,
                            'pick':(-1, -1),
                            'drop':(-1, -1),
                            'stepper':'down'}
        else:
            graph.remove_barrier(all_rpis[uid]['loc'])
            graph.add_barrier(curr_loc)
            all_rpis[uid]['loc'] = curr_loc
            if all_rpis[uid]['pick'] is not (-1, -1):
                if curr_loc is all_rpis[uid]['pick']:
                    # at pick loc
                    # send msg to pickup
                    # start going to drop
                    all_rpis[uid]['pick'] = (-1, -1)
                    
                    import mqtt_server
                    mqtt_server.send_message("up", uid)
                    time.sleep(3)
                    all_rpis[uid]['stepper'] = "up"

                    import routing
                    route, cost = routing.AStarSearch(curr_loc, all_rpis[uid]['drop'], graph)
                    
                else:
                    # go to pickup
            elif all_rpis[uid]['drop'] is not (-1, -1):
                # go to drop
    return

def start_server():
    import mqtt_server
    mqtt_server.start_server(server_message_handler)
    return

def read_warehouse_map():
    import routing
    map_filename = input("Give filename of warehouse map (default=warehouse_map):\n")
    global graph
    graph = routing.AStarGraph(map_filename)
    return

def run_server():
    read_warehouse_map()
    global all_rpis
    all_rpis = {}
    start_server()
    return

if __name__ == "__main__":
    run_server()