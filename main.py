#!/usr/bin/env python2.7

import requests
import time
from ethjsonrpc import EthJsonRpc
from ethjsonrpc.utils import wei_to_ether, ether_to_wei
from ethjsonrpc.exceptions import BadResponseError
import serial

API_KEY = "e480927a0fbd0e53c0cee71e8782515d"
DEVICE = "5fc84eb009b013c0545eb2911d180b9d"

# from_address = "0x90b983390bef91b17f3a2f2d7eb9121c1214fc6b"

geth_rpc_ip = "192.168.1.129"

headers = {
    "X-M2X-KEY": API_KEY
}


def send_payment(command):

    to_address = command["data"]["to_address"]
    from_address = command["data"]["from_address"]

    amount = float(command["data"]["amount"])

    amount_wei = int(ether_to_wei(amount))

    print "Sending {0} ETH {1} Wei to {2}".format(amount, amount_wei, to_address)

    client = EthJsonRpc(geth_rpc_ip, 8545)

    print client.transfer(from_address, to_address, amount_wei)

    # ser = serial.Serial('/dev/cu.usbmodem1421', 9600)
    #
    # for i in range(190009):
    #     print "blink"
    #     ser.write('1')



def process_command(command):

    print "Processing command :"

    print command

    if command["name"] == "SEND_PAYMENT":

        try:
            send_payment(command)
        except BadResponseError as er:
            print(er)

    mark_processed(command)


def mark_processed(command):

    print "Marking command {0} as processed".format(command["id"])

    process_request = requests.post("https://api-m2x.att.com/v2/devices/" + DEVICE + "/commands/" + command["id"] + "/process", headers=headers)

    print process_request


while True:

    print "Loading new commands"

    commands = requests.get("https://api-m2x.att.com/v2/devices/{0}/commands".format(DEVICE), headers=headers).json()["commands"]

    for command_object in commands:

        command_url = command_object["url"]

        command = requests.get(command_url, headers=headers).json()

        if command["status"] == "pending":

            process_command(command)

    time.sleep(1)


