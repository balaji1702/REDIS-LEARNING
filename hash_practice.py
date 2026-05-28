from redis_utility import RedisCacheManager

if __name__ == "__main__":
    manager = RedisCacheManager(password='TopSecretDevPass123!')
    
    if manager.ping_server():
        # 1. Define a sample user profile dictionary
        user_profile = {
            "name": "Alex",
            "role": "admin",
            "gold_balance": "100"  # Redis stores hash values as strings
        }
        
        # 2. Save the dictionary to Redis
        manager.set_hash("user:100", user_profile)
        
        # 3. Read it back
        retrieved_profile = manager.get_hash("user:100")
        print(f"Retrieved Hash Data: {retrieved_profile}")
        print(f"User's Name is: {retrieved_profile['name']}")