from redis_utility import RedisCacheManager
import time 


if __name__ == "__main__":

    # Create the manager object
    manager = RedisCacheManager(host='localhost', port=6379, password='TopSecretDevPass123!')

    if manager.ping_server():
        # 1. Set a key with a short expiration time
        manager.set_value("temp:key", "This will expire soon", expire_seconds=5)
        
        # 2. Retrieve the key immediately
        value = manager.get_value("temp:key")
        print(f"Immediately retrieved value: {value}")
        
        # 3. Wait for 6 seconds to ensure the key has expired
        time.sleep(6)
        
        # 4. Try to retrieve the key again after expiration
        expired_value = manager.get_value("temp:key")
        print(f"Value after expiration (should be None): {expired_value}")
    