#!/usr/bin/env python2.7
import json

import requests

# M2X API
api_key = "e480927a0fbd0e53c0cee71e8782515d"
device_id = "5fc84eb009b013c0545eb2911d180b9d"


command_params = {
    "name": "SEND_PAYMENT",
    "data": {
        "to_address": "0x16Ba1a0e4F6bA1E9B614ae8C25d101eA7441A0a1",
        "from_address": "0x9f97d33281649c7b38b73ead0c12ccef8f70a2b6",
        "amount": "0.015225785057792946"
    },
    "targets": {
        "devices": [device_id],
    }
}

headers = {
    "X-M2X-KEY": api_key
}

r = requests.post("https://api-m2x.att.com/v2/commands", json=command_params, headers=headers)

print (r.json())

