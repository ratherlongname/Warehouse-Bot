def message_to_coordinates(message):
    return graph.qr_loc_map[message]

def get_direction(curr_loc, next_loc):
    x_curr, y_curr = curr_loc
    x_next, y_next = next_loc
    if x_next is x_curr + 1 and y_next is y_curr:
        return "R"
    elif x_next is x_curr - 1 and y_next is y_curr:
        return "L"
    elif x_next is x_curr and y_next is y_curr + 1:
        return "B"
    elif x_next is x_curr and y_next is y_curr - 1:
        return "F"
    else:
        raise AssertionError("next_loc and curr_loc are not adjacent")

def send_next_command(uid, curr_loc):
    import mqtt_server
    import time
    import routing
    graph.remove_barrier(all_rpis[uid]['loc'])
    print("remove barrier from {}".format(all_rpis[uid]['loc']))
    graph.add_barrier(curr_loc)
    print("add barrier at {}".format(curr_loc))
    all_rpis[uid]['loc'] = curr_loc
    if all_rpis[uid]['pick'] != (-1, -1):
        print("pick is not -1 -1")
        if curr_loc == all_rpis[uid]['pick']:
            print("curr loc is pick loc")
            # at pick loc
            # send msg to pickup
            # start going to drop
            all_rpis[uid]['pick'] = (-1, -1)

            mqtt_server.send_message("UP", uid)
            time.sleep(5)
            all_rpis[uid]['stepper'] = "up"

            route, _ = routing.AStarSearch(curr_loc, all_rpis[uid]['drop'], graph)
            next_loc = route[1]
            graph.add_barrier(next_loc)
            command = get_direction(curr_loc, next_loc)
            mqtt_server.send_message(command, uid)

        else:
            print("curr loc is not pick loc")
            # go to pickup
            route, _ = routing.AStarSearch(curr_loc, all_rpis[uid]['pick'], graph)
            next_loc = route[1]
            graph.add_barrier(next_loc)
            command = get_direction(curr_loc, next_loc)
            mqtt_server.send_message(command, uid)

    elif all_rpis[uid]['drop'] != (-1, -1):
        print("drop is not -1 -1")
        if curr_loc == all_rpis[uid]['drop']:
            print("curr loc is drop loc")
            # at drop loc
            # send msg to drop
            all_rpis[uid]['drop'] = (-1, -1)

            mqtt_server.send_message("DOWN", uid)
            time.sleep(5)
            all_rpis[uid]['stepper'] = "down"

            if all_tasks:
                locs = all_tasks.pop(0)
                all_rpis[uid]['pick'] = locs[0]
                all_rpis[uid]['drop'] = locs[1]
                send_next_command(uid, curr_loc)

        else:
            print("curr loc is not drop loc")
            # go to drop
            route, _ = routing.AStarSearch(curr_loc, all_rpis[uid]['drop'], graph)
            next_loc = route[1]
            graph.add_barrier(next_loc)
            command = get_direction(curr_loc, next_loc)
            mqtt_server.send_message(command, uid)

def server_message_handler(client, userdata, msg):
    message = msg.payload.decode('latin-1')
    channel = msg.topic.split('/')
    print("received {} on channel {}".format(message, channel))

    if channel[0] == "block":
        graph.add_barrier(message_to_coordinates(message))
    elif channel[0] == "rpi":
        print("ab idhar")
        curr_loc = message_to_coordinates(message)
        uid = channel[2]
        print("UID: {}, Message: {}".format(uid, message))
        if uid not in all_rpis:
            print("new rpi")
            graph.add_barrier(curr_loc)
            all_rpis[uid] = {'loc':curr_loc,
                            'pick':(-1, -1),
                            'drop':(-1, -1),
                            'stepper':'down'}
            print("added new rpi")
            if all_tasks:
                locs = all_tasks.pop(0)
                all_rpis[uid]['pick'] = locs[0]
                all_rpis[uid]['drop'] = locs[1]
                send_next_command(uid, curr_loc)
        else:
            print("existing rpi")
            send_next_command(uid, curr_loc)
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

def print_all_rpis():
    for uid in all_rpis:
        print("uid {}: {}".format(uid, all_rpis[uid]))

def menu():
    import routing
    main_menu = ['q to quit',
                'p to print map',
                'g to take stuff from a to b',
                'a to add barrier',
                'r to remove barrier',
                't to print current task queue',
                'i to see all rpis']
    while True:
        print("\tWAREHOUSE SOFTWARE MENU")
        for option in main_menu:
            print(option)

        choice = input()
        if choice == 'q':
            return
        elif choice == 'p':
            graph.print_map()
        elif choice == 'g':
            print("Enter pickup point (x,y):")
            pick_loc = tuple([int(x) for x in input().split(',')])
            print("Enter drop point (x,y):")
            drop_loc = tuple([int(x) for x in input().split(',')])
            result, _ = routing.AStarSearch(pick_loc, drop_loc, graph)
            print ("Route: {}".format(result))
            routing.draw_route(graph, result)
            is_allocated = False
            for uid in all_rpis:
                print("checking uid {}".format(uid))
                if all_rpis[uid]['pick'] == (-1, -1) and all_rpis[uid]['drop'] == (-1, -1):
                    is_allocated = True
                    all_rpis[uid]['pick'] = pick_loc
                    all_rpis[uid]['drop'] = drop_loc
                    print("allocated")
                    send_next_command(uid, all_rpis[uid]['loc'])
                    break
            if is_allocated:
                pass
            else:
                all_tasks.append([pick_loc, drop_loc])
                print("No rpi free right now, task added to queue")
        elif choice is 'a':
            print("Enter barrier point to add (x,y):")
            barrier = tuple([int(x) for x in input().split(',')])
            graph.add_barrier(barrier)
        elif choice is 'r':
            print("Enter barrier point to remove (x,y):")
            barrier = tuple([int(x) for x in input().split(',')])
            graph.remove_barrier(barrier)
        elif choice is 't':
            if all_tasks:
                print("S.No.\tPick\tDrop")
                for i, locs in enumerate(all_tasks):
                    print("{}.\t{}\t{}".format(i+1, locs[0], locs[1]))
            else:
                print("Task queue empty...")
        elif choice is 'i':
            print_all_rpis()
    return

def run_server():
    read_warehouse_map()
    global all_rpis
    global all_tasks
    all_tasks = []
    all_rpis = {}
    start_server()
    menu()
    return

if __name__ == "__main__":
    run_server()
