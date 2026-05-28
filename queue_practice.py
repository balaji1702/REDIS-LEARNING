from redis_utility import RedisCacheManager

if __name__ == "__main__":
    manager = RedisCacheManager(password='TopSecretDevPass123!')
    
    if manager.ping_server():
        queue_name = "queue:email_alerts"
        
        print("\n--- Phase 1: App Pushes Tasks to Queue ---")
        manager.push_to_queue(queue_name, "welcome_user_101")
        manager.push_to_queue(queue_name, "password_reset_user_202")
        
        print("\n--- Phase 2: Worker Pulls Tasks from Queue ---")
        # Worker pulls the first task
        task_1 = manager.pop_from_queue(queue_name)
        print(f"Worker processing: {task_1}")
        
        # Worker pulls the second task
        task_2 = manager.pop_from_queue(queue_name)
        print(f"Worker processing: {task_2}")
        
        # Worker tries to pull when queue is empty
        task_3 = manager.pop_from_queue(queue_name)
        print(f"Worker checked empty queue, got: {task_3}")