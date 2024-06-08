import threading
from Energy_grid_Idea import check_grid_usage, balance_load
from ripplenet import Consumer, Owner

consumer = None
owner = None

def get_owner():
    return owner

def get_consumer():
    return consumer

if __name__ == "__main__":
    t1 = threading.Thread(target=check_grid_usage)
    t1.start

    # Generate wallets
    consumer = Consumer()
    owner = Owner()

    # Run the simulation
    for _ in range(24):  # Simulate for 24 hours
        balance_load()
    t1.join()