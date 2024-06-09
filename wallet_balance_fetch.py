import flask
from flask import *
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountInfo
from main import get_consumer
import time

app = flask.Flask(__name__)
app.config["DEBUG"] = True

client = JsonRpcClient("https://s.altnet.rippletest.net:51234/")

@app.route('/wallet_balance')
def check_account_balance():
    time.sleep(30)
    consumer = get_consumer()
    account_info = AccountInfo(
        account=consumer.classic_address,
        ledger_index="validated",
        strict=True
    )
    response = client.request(account_info)
    return response.json