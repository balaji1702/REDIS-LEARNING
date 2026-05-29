from redis_utility import RedisCacheManager
if __name__ == "__main__":
    manager = RedisCacheManager(password='TopSecretDevPass123!')
    
    if manager.ping_server():
        set_key = "analytics:page_views:homepage"
        
        print("\n--- Phase 1: Simulating Web Traffic ---")
        # User 1 arrives
        manager.add_to_set(set_key, "192.168.1.50")
        # User 2 arrives
        manager.add_to_set(set_key, "203.0.113.12")
        # User 1 refreshes the page (Duplicate IP!)
        manager.add_to_set(set_key, "192.168.1.50")
        
        print("\n--- Phase 2: Fetching Unique Audience ---")
        unique_ips = manager.get_set_members(set_key)
        print(f"All Unique IP Addresses: {unique_ips}")
        print(f"Total Unique Visitors Count: {len(unique_ips)}")