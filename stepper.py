import RPi.GPIO as GPIO
import time 
import config

def move_stepper(steps):
    GPIO.output(config.out1,GPIO.HIGH)
    GPIO.output(config.out2,GPIO.HIGH)
    GPIO.output(config.out3,GPIO.HIGH)
    GPIO.output(config.out4,GPIO.HIGH)
    x = int(steps)
    positive = 0
    negative = 0
    y = 0
    i = 0
    if x>0 and x<=400:
        for y in range(x,0,-1):
            if negative==1:
                if i==7:
                    i=0
                else:
                    i=i+1
                y=y+2
                negative=0
            positive=1
            #print((x+1)-y)
            if i==0:
                GPIO.output(config.out1,GPIO.HIGH)
                GPIO.output(config.out2,GPIO.LOW)
                GPIO.output(config.out3,GPIO.LOW)
                GPIO.output(config.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==1:
                GPIO.output(config.out1,GPIO.HIGH)
                GPIO.output(config.out2,GPIO.HIGH)
                GPIO.output(config.out3,GPIO.LOW)
                GPIO.output(config.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==2:  
                GPIO.output(config.out1,GPIO.LOW)
                GPIO.output(config.out2,GPIO.HIGH)
                GPIO.output(config.out3,GPIO.LOW)
                GPIO.output(config.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==3:    
                GPIO.output(config.out1,GPIO.LOW)
                GPIO.output(config.out2,GPIO.HIGH)
                GPIO.output(config.out3,GPIO.HIGH)
                GPIO.output(config.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==4:  
                GPIO.output(config.out1,GPIO.LOW)
                GPIO.output(config.out2,GPIO.LOW)
                GPIO.output(config.out3,GPIO.HIGH)
                GPIO.output(config.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==5:
                GPIO.output(config.out1,GPIO.LOW)
                GPIO.output(config.out2,GPIO.LOW)
                GPIO.output(config.out3,GPIO.HIGH)
                GPIO.output(config.out4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==6:    
                GPIO.output(config.out1,GPIO.LOW)
                GPIO.output(config.out2,GPIO.LOW)
                GPIO.output(config.out3,GPIO.LOW)
                GPIO.output(config.out4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==7:    
                GPIO.output(config.out1,GPIO.HIGH)
                GPIO.output(config.out2,GPIO.LOW)
                GPIO.output(config.out3,GPIO.LOW)
                GPIO.output(config.out4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            if i==7:
                i=0
                continue
            i=i+1
    
    
    elif x<0 and x>=-400:
        x=x*-1
        for y in range(x,0,-1):
            if positive==1:
                if i==0:
                    i=7
                else:
                    i=i-1
                y=y+3
                positive=0
            negative=1
            #print((x+1)-y) 
            if i==0:
                GPIO.output(config.out1,GPIO.HIGH)
                GPIO.output(config.out2,GPIO.LOW)
                GPIO.output(config.out3,GPIO.LOW)
                GPIO.output(config.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==1:
                GPIO.output(config.out1,GPIO.HIGH)
                GPIO.output(config.out2,GPIO.HIGH)
                GPIO.output(config.out3,GPIO.LOW)
                GPIO.output(config.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==2:  
                GPIO.output(config.out1,GPIO.LOW)
                GPIO.output(config.out2,GPIO.HIGH)
                GPIO.output(config.out3,GPIO.LOW)
                GPIO.output(config.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==3:    
                GPIO.output(config.out1,GPIO.LOW)
                GPIO.output(config.out2,GPIO.HIGH)
                GPIO.output(config.out3,GPIO.HIGH)
                GPIO.output(config.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==4:  
                GPIO.output(config.out1,GPIO.LOW)
                GPIO.output(config.out2,GPIO.LOW)
                GPIO.output(config.out3,GPIO.HIGH)
                GPIO.output(config.out4,GPIO.LOW)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==5:
                GPIO.output(config.out1,GPIO.LOW)
                GPIO.output(config.out2,GPIO.LOW)
                GPIO.output(config.out3,GPIO.HIGH)
                GPIO.output(config.out4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==6:    
                GPIO.output(config.out1,GPIO.LOW)
                GPIO.output(config.out2,GPIO.LOW)
                GPIO.output(config.out3,GPIO.LOW)
                GPIO.output(config.out4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            elif i==7:    
                GPIO.output(config.out1,GPIO.HIGH)
                GPIO.output(config.out2,GPIO.LOW)
                GPIO.output(config.out3,GPIO.LOW)
                GPIO.output(config.out4,GPIO.HIGH)
                time.sleep(0.03)
                #time.sleep(1)
            if i==0:
                i=7
                continue
            i=i-1 


def platform_down():
    move_stepper(config.down_steps)
    return

def platform_up():
    move_stepper(config.up_steps)
    return

def setup_stepper():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(config.out1,GPIO.OUT)
    GPIO.setup(config.out2,GPIO.OUT)
    GPIO.setup(config.out3,GPIO.OUT)
    GPIO.setup(config.out4,GPIO.OUT)
    return


def menu():
    try:
        main_menu = ['q to quit',
                     'u to go up',
                     'd to drop down',
                     's to give steps']
        setup_stepper()
        while True:
            print("\tSTEPPER TEST MENU")
            for option in main_menu:
                print(option)

            choice = input()
            if choice == 'q':
                return
            elif choice == 'u':
                platform_up()
            elif choice == 'd':
                platform_down()
            elif choice is 's':
                steps = input("Enter steps:\n")
                move_stepper(steps)
    finally:
        GPIO.cleanup()
    return


if __name__ == "__main__":
    menu()