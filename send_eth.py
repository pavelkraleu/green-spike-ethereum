#!/usr/bin/env python2.7

from ethjsonrpc import EthJsonRpc
from ethjsonrpc.utils import wei_to_ether, ether_to_wei

c = EthJsonRpc('192.168.1.129', 8545)

from_address = "0x90b983390bef91b17f3a2f2d7eb9121c1214fc6b"
to_address = "0x16Ba1a0e4F6bA1E9B614ae8C25d101eA7441A0a1"

print c.net_version()

print c.web3_clientVersion()

print c.eth_gasPrice()

print c.eth_blockNumber()

print wei_to_ether(c.eth_getBalance(from_address))

print wei_to_ether(c.eth_getBalance(to_address))

# print c.web3_toWei(0.01, "ether")

amount = int(ether_to_wei(0.001))

print type(amount)

print amount

print hex(amount)

print c.transfer(from_address, to_address, amount)

print