#!/usr/bin/env python2.7

import requests
import time
from pymongo import MongoClient
import datetime
import numpy
import time
from ethjsonrpc import EthJsonRpc
from ethjsonrpc.utils import wei_to_ether, ether_to_wei

api_key = "e480927a0fbd0e53c0cee71e8782515d"
device_id = "0904d16113289ea7b0f7d0dcbf8167ed"
stream_id = "wetness"

geth_rpc_ip = "192.168.1.129"

client_eth = EthJsonRpc(geth_rpc_ip, 8545)

seen_timestamps = []

client = MongoClient('mongodb://heroku_32wdl3g2:h06pp8p05rb81qa9lqco4di5s5@ds155820.mlab.com:55820/heroku_32wdl3g2')

db = client.heroku_32wdl3g2

spikes = db["spikes"].find({})

eth_usd = 43.80

#
# print spikes[0]

# green_values = range(0, 2000)
# yellow_values = range(2000, 3000)
# red_range = range(3000, 4096)


def get_wallet_balance(wallet):

    return wei_to_ether(client_eth.eth_getBalance(wallet))

def get_new_value():

    # print "Reading new values"

    req = requests.get("https://api-m2x.att.com/v2/devices/{0}/streams/wetness/values?limit=10".format(device_id))

    values = req.json()["values"]

    return values


def get_color():

    last_values = db["raw_values"].find({}).sort("timestamp", -1).limit(5)

    all_last_values = []

    for value in last_values:

        all_last_values.append(value["value"])

    last_average = numpy.mean(all_last_values)

    # print last_average

    if last_average <= 2000:
        return "green"

    if last_average <= 3000:
        return "yellow"

    return "red"


def plant_watered(spike):

    print "Plant has been watered"

    command_params = {
        "name": "SEND_PAYMENT",
        "data": {
            "to_address": spike["requestor"],
            "from_address": "0x" + spike["eth"],
            "amount": str(spike["bounty"])
        },
        "targets": {
            "devices": ["5fc84eb009b013c0545eb2911d180b9d"],
        }
    }

    print command_params

    headers = {
        "X-M2X-KEY": api_key
    }

    r = requests.post("https://api-m2x.att.com/v2/commands", json=command_params, headers=headers)

    print (r.json())


def set_color(color):

    print "Color " + color

    spike = db["spikes"].find({"dev": device_id}).limit(1)[0]

    if spike.get("state", "green") in ["yellow", "red"] and color == "green":
        plant_watered(spike)

    spike["state"] = color

    balance = get_wallet_balance("0x" + spike["eth"])

    spike["balance"] = balance
    spike["balance-usd"] = balance * eth_usd

    bounty_eth = 0.009

    spike["bounty"] = bounty_eth
    spike["bounty-usd"] = bounty_eth * eth_usd

    db["spikes"].update({'_id': spike["_id"]}, spike)


while True:

    stream_values = get_new_value()

    for value in stream_values:

        if value["timestamp"] not in seen_timestamps:

            seen_timestamps.append(value["timestamp"])

            value["timestamp"] = datetime.datetime.strptime(value["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")

            print value

            db["raw_values"].insert(value)

    color = get_color()

    set_color(color)

    time.sleep(1)
