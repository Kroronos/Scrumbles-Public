import hashlib, random, threading, os

#Thread local storage
thread_local = threading.local()


#Row ID Range; with highest bit always set
ID_RANGE = (2**62,2**63)

def get_random_row_id():

    try:
        thread_local_random = thread_local.random
    except AttributeError:
        thread_local_random = _init_thread_local_random()

    return thread_local_random.randrange(*ID_RANGE)

def _init_thread_local_random():
    rng = random.SystemRandom()
    hash_object = hashlib.sha1(hex(os.getpid()).encode())
    hash_object.update(hex(rng.randrange(*ID_RANGE)).encode())
    seed = int(hash_object.hexdigest(), 16)

    thread_local.random = random.Random(seed)

    return thread_local.random

test = get_random_row_id()
rand = get_random_row_id()
count = 0

while test != rand:
    print(count,rand)
    rand = get_random_row_id()
    count += 1

#Watched execution run for 1,000,000 iterations without collision.
#Pretty good, don't think our project will have 1,000,000 rows in one table
