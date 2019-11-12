def message_to_coordinates(message):
    # TODO
    return (0, 0)

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
    graph.add_barrier(curr_loc)
    all_rpis[uid]['loc'] = curr_loc
    if all_rpis[uid]['pick'] is not (-1, -1):
        if curr_loc is all_rpis[uid]['pick']:
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
            # go to pickup
            route, _ = routing.AStarSearch(curr_loc, all_rpis[uid]['pick'], graph)
            next_loc = route[1]
            graph.add_barrier(next_loc)
            command = get_direction(curr_loc, next_loc)
            mqtt_server.send_message(command, uid)

    elif all_rpis[uid]['drop'] is not (-1, -1):
        if curr_loc is all_rpis[uid]['drop']:
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
            # go to drop
            route, _ = routing.AStarSearch(curr_loc, all_rpis[uid]['drop'], graph)
            next_loc = route[1]
            graph.add_barrier(next_loc)
            command = get_direction(curr_loc, next_loc)
            mqtt_server.send_message(command, uid)

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
            if all_tasks:
                locs = all_tasks.pop(0)
                all_rpis[uid]['pick'] = locs[0]
                all_rpis[uid]['drop'] = locs[1]
                send_next_command(uid, curr_loc)
        else:

            send_next_command(uid, curr_loc)

#            graph.remove_barrier(all_rpis[uid]['loc'])
#            graph.add_barrier(curr_loc)
#            all_rpis[uid]['loc'] = curr_loc
#            if all_rpis[uid]['pick'] is not (-1, -1):
#                if curr_loc is all_rpis[uid]['pick']:
#                    # at pick loc
#                    # send msg to pickup
#                    # start going to drop
#                    all_rpis[uid]['pick'] = (-1, -1)
#                    
#                    import mqtt_server
#                    mqtt_server.send_message("up", uid)
#                    time.sleep(3)
#                    all_rpis[uid]['stepper'] = "up"
#
#                    import routing
#                    route, cost = routing.AStarSearch(curr_loc, all_rpis[uid]['drop'], graph)
#                    
#                else:
#                    # go to pickup
#                    pass
#            elif all_rpis[uid]['drop'] is not (-1, -1):
#                # go to drop
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

def menu():
    import routing
    main_menu = ['q to quit',
                'p to print map',
                'g to take stuff from a to b',
                'a to add barrier',
                'r to remove barrier',
                't to print current task queue']
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
                if all_rpis[uid]['pick'] is (-1, -1) and all_rpis[uid]['drop'] is (-1, -1):
                    is_allocated = True
                    all_rpis[uid]['pick'] = pick_loc
                    all_rpis[uid]['drop'] = drop_loc
                    break
            if not is_allocated:
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
