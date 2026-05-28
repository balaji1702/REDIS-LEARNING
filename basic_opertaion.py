from calendar import c
from redis_utility import RedisCacheManager

if __name__ == "__main__":
    # Create the manager object
    manager = RedisCacheManager(host='localhost', port=6379, password='TopSecretDevPass123!')
    
    if manager.ping_server():
        # 1. Test our new safe SET method
        manager.set_value("app:status", "running")
        
        # 2. Test our new safe GET method
        status = manager.get_value("app:status")
        print(f"Retrieved status: {status}")