import config

if __name__ == "__main__":
    main_menu = ['q to quit', 'm to test motors']
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
