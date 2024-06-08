from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.transaction import send_reliable_submission
from xrpl.models.transactions import Payment


client = JsonRpcClient("https://s.altnet.rippletest.net:51234/")

wallet = Wallet.create()  # Creates a new wallet for simplicity

def create_payment_transaction(wallet, destination_address, amount):
    payment = Payment(
        account=wallet.classic_address,
        amount=str(amount),
        destination=destination_address,
        fee="12",
        sequence=wallet.sequence,
        transaction_type="Payment"
    )
    return payment

def send_payment(wallet, client, destination_address, amount):
    payment_tx = create_payment_transaction(wallet, destination_address, amount)
    response = send_reliable_submission(payment_tx, client)
    return response

def wallet():
    return wallet
