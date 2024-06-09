import threading
from initiate_grid import *
from ripplenet import Consumer, Owner
from wallet_balance_fetch import run_app

consumer = None
owner = None

def get_owner():
    return owner

def get_consumer():
    return consumer

if __name__ == "__main__":
    t1 = threading.Thread(target=check_grid_usage)
    t1.start

    # Run app to fetch the wallet balance
    run_app()

    # Generate wallets
    consumer = Consumer()
    owner = Owner()
    
    check_grid_usage("2024-06-09 10:00")

    # Run the simulation
    #for _ in range(24):  # Simulate for 24 hours
    #   balance_load()
    t1.join()