import config

if __name__ == "__main__":
    main_menu = ['q to quit',
                'm to test motors',
                'r to become rpi',
                's to become server',
                'g to test routing',
                'p to test ping sensor']
    while True:
        print("\tMAIN MENU")
        for option in main_menu:
            print(option)
        
        choice = input()
        
        if choice is 'q':
            print("Exiting...")
            exit()
        
        elif choice is 'm':
            import motor
            motor.menu()
        
        elif choice is 'r':
            import mqtt_rpi
            mqtt_rpi.menu()

        elif choice is 's':
            import mqtt_server
            mqtt_server.menu()

        elif choice is 'g':
            import routing
            routing.menu()
        elif choice is 'p':
            import ping
            ping.menu()