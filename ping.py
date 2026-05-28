from redis_utility import RedisCacheManager

# Testing our class setup
if __name__ == "__main__":
    # Create the manager object
    manager = RedisCacheManager(host='localhost', port=6379, password='TopSecretDevPass123!')
    
    # Test the connection
    if manager.ping_server():
        print("Success: Manager is ready for production actions!")
    else:
        print("Failure: Check your connection settings.")