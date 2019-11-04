import config

if __name__ == "__main__":
    main_menu = ['q to quit', 'm to test motors', 'r to become rpi', 's to become server']
    motor_setup_done = False
    while True:
        print("\tMAIN MENU")
        for option in main_menu:
            print(option)
        
        choice = input()
        
        if choice is 'q':
            print("Exiting...")
            exit()
        
        elif choice is 'm':
            import motor_test
            if not motor_setup_done:
                motor_test.setup_motors()
                motor_setup_done = True
            motor_test.menu()
        
        elif choice is 'r':
            import mqtt_rpi
            mqtt_rpi.menu()

        elif choice is 's':
            import mqtt_server
            mqtt_server.menu()
