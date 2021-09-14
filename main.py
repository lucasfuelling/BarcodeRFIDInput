#!/usr/bin/env python
import json
import paho.mqtt.publish as publish
import os
import RPi.GPIO as GPIO
import time

token = "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"
employee_ID = "000"
order_qty = 1
order_ID = "0001"
mqttbroker="10.116.1.100"
greenled = 23
redled = 4
yellowled = 27

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
        GPIO.output(yellowled, GPIO.HIGH)
        if my_input.startswith("Q"):
            order_qty = int(my_input[1:])
            input1 = 1
        elif my_input.startswith("ID"):
            order_ID = my_input[2:]
            input2 = 1
        elif my_input.startswith("M"):
            machine = my_input[1:]
            input3 = 1
        elif my_input == "off":
            GPIO.cleanup()
            os.system("sudo shutdown -h now")
        else:
            employee_ID = my_input
            input4 = 1
    mydict = {
        "employee_id":employee_ID,
        "order_qty": order_qty,
        "order_id": order_ID,
        "machine": machine
    }

    print(json.dumps(mydict))
    output_msg = json.dumps(mydict)
    publish.single(machine + "/setup", output_msg, hostname=mqttbroker)
    GPIO.output(greenled, GPIO.HIGH)
    GPIO.output(yellowled, GPIO.LOW)
    GPIO.output(redled, GPIO.LOW)
    time.sleep(2)
    GPIO.output(greenled, GPIO.LOW)
    GPIO.output(yellowled, GPIO.LOW)
    GPIO.output(redled, GPIO.LOW)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(redled, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(yellowled, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(greenled, GPIO.OUT, initial=GPIO.LOW)
    print("starting program")
    while True:
        get_send_input()
    GPIO.cleanup()
