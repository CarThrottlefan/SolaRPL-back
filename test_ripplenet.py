import requests
import xrpl.wallet
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountInfo
import time
from xrpl.models.transactions import Payment
from xrpl.transaction import submit_and_wait, submit

#completely unrelated to other scripts, therefore double functions
def generate_wallet():
    wallet = xrpl.wallet.Wallet.create()
    print(f"Generated Wallet Address: {wallet.classic_address}")
    print(f"Generated Wallet Seed: {wallet.seed}")
    return wallet

def fund_wallet(wallet):
    faucet_url = "https://faucet.altnet.rippletest.net/accounts"
    response = requests.post(faucet_url, json={"destination": wallet.classic_address})
    if response.status_code == 200:
        print(f"Successfully funded wallet: {wallet.classic_address}")
        return response.json()
    else:
        print(f"Failed to fund wallet: {wallet.classic_address}")
        return None


def check_account_balance(client, wallet):
    account_info = AccountInfo(
        account=wallet.classic_address,
        ledger_index="validated",
        strict=True
    )
    response = client.request(account_info)
    return response.result

def create_payment_transaction(wallet, destination_address, amount):
    payment = Payment(
        account=wallet.classic_address,
        amount=str(amount),
        destination=destination_address
    )
    return payment


def send_payment(wallet, client, destination_address, amount):
    payment_tx = create_payment_transaction(wallet, destination_address, amount)
    signed_tx = submit_and_wait(payment_tx, client, wallet)
    response = submit(signed_tx)
    return response

def main():

    wallet1 = generate_wallet()
    wallet2 = generate_wallet()

    fund_wallet(wallet1)
    fund_wallet(wallet2)

#it takess some time to connect 
    time.sleep(30)


    client = JsonRpcClient("https://s.altnet.rippletest.net:51234/")

  
    print("Checking balance of Wallet 1:")
    balance_response1 = check_account_balance(client, wallet1)
    print(balance_response1)

    print("Checking balance of Wallet 2:")
    balance_response2 = check_account_balance(client, wallet2)
    print(balance_response2)

    print("Sending payment from Wallet 1 to Wallet 2")
    payment_response = send_payment(wallet1, client, wallet2.classic_address, "1000000")
    print(payment_response)
    print("Checking balance of Wallet 1 after payment:")
    balance_response1_after = check_account_balance(client, wallet1)
    print(balance_response1_after)

    print("Checking balance of Wallet 2 after payment:")
    balance_response2_after = check_account_balance(client, wallet2)
    print(balance_response2_after)

if __name__ == "__main__":
    main()

