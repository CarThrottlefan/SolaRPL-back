import threading
from initiate_grid import *
from ripplenet import Consumer, Owner

def get_consumer():
    return consumer

def get_owner():
    return owner

  # Generate wallets
consumer = Consumer()
owner = Owner()

#consumer = None
#owner = None

if __name__ == "__main__":
    t1 = threading.Thread(target=check_grid_usage,args=[start_time])
    t1.start()

    # Run app to fetch the wallet balance
    # Import run_app here to avoid circular dependency
    from wallet_balance_fetch import run_app
    run_app()

  

    # Run the simulation
    #for _ in range(24):  # Simulate for 24 hours
    #   balance_load()
    t1.join()
