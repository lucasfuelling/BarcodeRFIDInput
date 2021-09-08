#!/usr/bin/env python
import json
import paho.mqtt.publish as publish
import os

employee_ID = "000"
order_qty = 1
order_ID = "0001"


def get_send_input():
    #get all inputs for metadata
    global employee_ID, order_qty, order_ID
    input1 = 0
    input2 = 0
    input3 = 0
    input4 = 0

    while input1 + input2 + input3 + input4 < 4:
        my_input = input()
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        print("starting program")
        get_send_input()
