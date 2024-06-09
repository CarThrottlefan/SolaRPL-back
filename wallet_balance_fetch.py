import flask
from flask import *
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountInfo
import time

app = flask.Flask(__name__)

client = JsonRpcClient("https://s.altnet.rippletest.net:51234/")

@app.route('/wallet_balance')
def check_account_balance():
    #time.sleep(30)
    # Import get_consumer here to avoid circular dependency
    from main import get_consumer
    consumer = get_consumer()
    account_info = AccountInfo(
        account=consumer.wallet.classic_address,  # Corrected attribute access
        ledger_index="validated",
        strict=True
    )
    response = client.request(account_info)
    return response.result

def run_app():
    app.run()
