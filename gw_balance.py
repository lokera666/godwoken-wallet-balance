#encoding: utf-8

import requests
import prometheus_client
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask, request, current_app
import os
import sys


GODWOKEN_RPC = sys.argv[1]
GODWOKEN_wallet = sys.argv[2]

NodeFlask = Flask(__name__)

def convert_int(value):
    try:
        return int(value)
    except ValueError:
        return int(value, base=16)
    except Exception as exp:
        raise exp

class RpcGet(object):
    def __init__(self, GODWOKEN_RPC):
        self.GODWOKEN_RPC = GODWOKEN_RPC

    def get_godwoken_info(self):
        headers = {"Content-Type":"application/json"}
        data = '{"id": 1,"jsonrpc": "2.0","method": "eth_getBalance","params": ["%s","latest"],"id":1}' % (GODWOKEN_wallet)
        try:
            r = requests.post(
                url="%s" %(self.GODWOKEN_RPC),
                data=data,
                headers=headers
            )
            replay = r.json()["result"]
            return {
                "wallet_balance": convert_int(replay)/1000000000000000000,
            }
        except:
            return {
                "wallet_balance": "-1",
            }

@NodeFlask.route("/metrics/balance")
def rpc_get():
    GODWOKEN_Chain = CollectorRegistry(auto_describe=False)
    Get_godwoken_Info = Gauge("get_wallet_balance",
                                   "Get wallet_balance, Show godwoken wallet balance",
                                   ["godwoken_wallet"],
                                   registry=GODWOKEN_Chain)

    get_result = RpcGet(GODWOKEN_RPC)
    godwoken_last_block_info = get_result.get_godwoken_info()
    Get_godwoken_Info.labels(
        godwoken_wallet=GODWOKEN_wallet
    ).set(godwoken_last_block_info["wallet_balance"])
    return Response(prometheus_client.generate_latest(GODWOKEN_Chain), mimetype="text/plain")

if __name__ == "__main__":
    NodeFlask.run(host="0.0.0.0",port=3000)
