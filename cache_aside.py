from redis_utility import RedisCacheManager
def get_cached_user_profile(manager, user_id):
        """
        Production Cache-Aside Pattern:
        1. Check Redis cache first.
        2. If missing, 'read from DB' and update cache.
        """
        key = f"user:{user_id}"
        
        # Step 1: Check the cache
        profile = manager.get_hash(key)
        
        if profile:
            print(f"🎯 Cache Hit! Retrieved from Redis instantly.")
            return profile
        else:
            print(f"❌ Cache Miss! Fetching from slow Database...")
            # Step 2: Simulate a slow database query
            # In production, this would be a query like: db.query("SELECT * FROM users...")
            fresh_db_data = {
                "name": f"User_{user_id}",
                "role": "member",
                "status": "active"
            }
            
            # Step 3: Populate the cache so the next request is fast
            manager.set_hash(key, fresh_db_data)
            
            # Optional: Set a TTL so old data eventually clears out
            manager.client.expire(key, 10) # Expires in 1 hour
            
            return fresh_db_data
        

if __name__ == "__main__":
    manager = RedisCacheManager(password='TopSecretDevPass123!')
    
    if manager.ping_server():
        print("\n--- Request 1: First time looking for User 999 ---")
        user_data_1 = get_cached_user_profile(manager, "999")
        print(f"Result 1: {user_data_1}")
        
        print("\n--- Request 2: Immediate second request for User 999 ---")
        user_data_2 = get_cached_user_profile(manager, "999")
        print(f"Result 2: {user_data_2}")