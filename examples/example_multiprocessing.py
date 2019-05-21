import multiprocessing
import random
from string import ascii_lowercase
import time


from glutemulo.kafka.producer import JsonKafka as Producer
from glutemulo.kafka.consumer import JsonKafka as Consumer


def producer():
    """worker function"""
    productor = Producer(bootstrap_servers="localhost:9092")
    for _ in range(50):
        letters = "".join(random.choice(ascii_lowercase) for _ in range(5))
        productor.produce("simple-topic", dict(value=letters))
        time.sleep(random.randint(1, 3))


def consumer():
    consumer = Consumer(
        "simple-topic", bootstrap_servers="localhost:9092", group_id="Same group"
    )
    name = multiprocessing.current_process().name
    while True:
        for msg in consumer.consume():
            print(f"{name} - Received: {msg}")


if __name__ == "__main__":
    jobs = []
    prod = multiprocessing.Process(target=producer)
    jobs.append(prod)
    prod.start()

    for i in range(5):
        p = multiprocessing.Process(target=consumer)
        jobs.append(p)
        p.start()
