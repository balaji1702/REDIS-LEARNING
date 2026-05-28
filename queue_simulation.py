import time
from redis_utility import RedisCacheManager


if __name__ == "__main__":

    manager = RedisCacheManager(password='TopSecretDevPass123!')

    if manager.ping_server():

        while True :

            task = manager.pop_from_queue("task")

            if task:

                print("working on the task:",task)
                time.sleep(4)
            else:
                print("watching out for the task")
                time.sleep(4)

