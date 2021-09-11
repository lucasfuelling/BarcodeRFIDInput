#!/usr/bin/env python
import json
import paho.mqtt.publish as publish
import os
import RPi.GPIO as GPIO

employee_ID = "000"
order_qty = 1
order_ID = "0001"
mqttbroker="10.116.1.100"

def get_send_input():
    #get all inputs for metadata
    global employee_ID, order_qty, order_ID, mqttbroker
    input1 = 0
    input2 = 0
    input3 = 0
    input4 = 0
    GPIO.output(4, GPIO.HIGH)
    while input1 + input2 + input3 + input4 < 4:
        my_input = input()
        GPIO.output(27, GPIO.HIGH)
        if my_input.startswith("Qty:"):
            order_qty = int(my_input[4:])
            input1 = 1
        elif my_input.startswith("OrderID:"):
            order_ID = my_input[8:]
            input2 = 1
        elif my_input.startswith("MC:"):
            machine = my_input[3:]
            input3 = 1
        elif my_input == "off":
            GPIO.cleanup()
            os.system("sudo shutdown -h now")
        else:
            employee_ID = my_input
            input4 = 1
    mydict = {
        "EmployeeID":employee_ID,
        "OrderQty": order_qty,
        "OrderID": order_ID
    }

    print(json.dumps(mydict))
    output_msg = json.dumps(mydict)
    publish.single(machine + "/input", output_msg, hostname="192.168.1.98")
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(4, GPIO.LOW)
    sleep(2)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
    try:
        while True:
            print("starting program")
            get_send_input()
    except:
        print("error")
    finally:
        GPIO.cleanup()