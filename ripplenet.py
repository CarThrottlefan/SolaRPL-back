import requests
import xrpl.wallet
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountInfo
import time
from xrpl.models.transactions import Payment
from xrpl.transaction import submit, submit_and_wait
from main import get_consumer, get_owner

class Consumer:
    def __init__(self):
        self.wallet = generate_wallet("consumer")

class Owner:
    def __init__(self):
        self.wallet = generate_wallet("owner")

client = JsonRpcClient("https://s.altnet.rippletest.net:51234/")

def generate_wallet(wallet_owner):
    wallet = xrpl.wallet.Wallet.create()
    print("Generating wallet for:" + wallet_owner)
    print(f"Generated Wallet Address: {wallet.classic_address}")
    print(f"Generated Wallet Seed: {wallet.seed}")
    if wallet_owner == "owner":
        fund_wallet(wallet)
    return wallet

def send_payment(amount):
    owner = get_owner()
    consumer = get_consumer()
    payment_tx = create_payment_transaction(owner.wallet, consumer.wallet.classic_address, amount)
    signed_tx = submit_and_wait(payment_tx, client, owner.wallet)
    response = submit(signed_tx, client)
    if response.status_code == 200:
        print(f"Successfully sent transaction: {consumer.wallet.classic_address}")
        return response.json()
    else:
        print(f"Failed to send transaction: {consumer.wallet.classic_address}")
        return None

def create_payment_transaction(wallet, destination_address, amount):
    payment = Payment(
        account=wallet.classic_address,
        amount=str(amount),
        destination=destination_address,
    )
    return payment

def fund_wallet(wallet):
    faucet_url = "https://faucet.altnet.rippletest.net/accounts"
    response = requests.post(faucet_url, json={"destination": wallet.classic_address})
    if response.status_code == 200:
        print(f"Successfully funded wallet: {wallet.classic_address}")
        return response.json()
    else:
        print(f"Failed to fund wallet: {wallet.classic_address}")
        return None

def check_account_balance(wallet):
    account_info = AccountInfo(
        account=wallet.classic_address,
        ledger_index="validated",
        strict=True
    )
    response = client.request(account_info)
    return response.result