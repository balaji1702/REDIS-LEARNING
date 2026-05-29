import redis
from redis.exceptions import RedisError

class RedisCacheManager:
    def __init__(self, host='localhost', port=6379, password=None):
        """
        Initialize the production-ready Redis client.
        """
        print("Initializing Redis client...")
        # We create a connection pool to reuse connections efficiently
        self.pool = redis.ConnectionPool(
            host=host,
            port=port,
            password=password,
            decode_responses=True,
            max_connections=10  # Limits maximum open connections to save memory
        )
        self.client = redis.Redis(connection_pool=self.pool)

    def ping_server(self):
        """Test if the server is alive."""
        try:
            return self.client.ping()
        except RedisError as e:
            print(f"Database connection failed: {e}")
            return False
        
    def set_value(self, key, value , expire_seconds=None) :
        """Safely write a string value to Redis."""
        try:
            # We use the internal client to execute the standard SET command
            self.client.set(key, value , ex=expire_seconds)  # ex sets an expiration time in seconds
            print(f"Successfully set key: {key}")
            return True
        except RedisError as e:
            print(f"Production Error during SET: {e}")
            return False

    def get_value(self, key):
        """Safely read a string value from Redis."""
        try:
            # We use the internal client to execute the standard GET command
            value = self.client.get(key)
            return value
        except RedisError as e:
            print(f"Production Error during GET: {e}")
            return None
        
    def set_hash(self, key, dictionary_data):
        """Safely store a Python dictionary as a Redis Hash."""
        try:
            # 'mapping' takes a standard Python dict and saves it as key-value fields
            self.client.hset(key, mapping=dictionary_data)
            print(f"Successfully saved Hash: {key}")
            return True
        except RedisError as e:
            print(f"Production Error during HSET: {e}")
            return False

    def get_hash(self, key):
        """Safely retrieve an entire Redis Hash as a Python dictionary."""
        try:
            # hgetall returns a dictionary of all fields and values inside the hash
            data = self.client.hgetall(key)
            return data if data else None
        except RedisError as e:
            print(f"Production Error during HGETALL: {e}")
            return None
        
    def push_to_queue(self, queue_name, item):
        """Safely push a new item onto the end of a queue."""
        try:
            # rpush adds the item to the right side of the list
            self.client.rpush(queue_name, item)
            print(f"Pushed item into queue '{queue_name}': {item}")
            return True
        except RedisError as e:
            print(f"Production Error during RPUSH: {e}")
            return False

    def pop_from_queue(self, queue_name):
        """Safely pull and remove the oldest item from the front of the queue."""
        try:
            # lpop removes and returns the leftmost item
            item = self.client.lpop(queue_name)
            return item  # This will be None if the queue is empty
        except RedisError as e:
            print(f"Production Error during LPOP: {e}")
            return None
        
    def add_to_set(self, set_key, item):
        """Safely add an item to a Set. Returns True if it's a new item."""
        try:
            # sadd returns the number of new elements successfully added
            result = self.client.sadd(set_key, item)
            if result > 0:
                print(f"Added new member to set '{set_key}': {item}")
                return True
            else:
                print(f"Ignored duplicate member in set '{set_key}': {item}")
                return False
        except RedisError as e:
            print(f"Production Error during SADD: {e}")
            return False

    def get_set_members(self, set_key):
        """Safely retrieve all unique items from a Set."""
        try:
            # smembers returns a Python set containing all items
            members = self.client.smembers(set_key)
            return members if members else set()
        except RedisError as e:
            print(f"Production Error during SMEMBERS: {e}")
            return set()
        
    def update_score(self, leaderboard_name, member, score):
        """Safely add or update a member's score in a Sorted Set."""
        try:
            # zadd takes a Python dictionary mapping {member_name: score}
            self.client.zadd(leaderboard_name, {member: score})
            print(f"Updated score for '{member}' in '{leaderboard_name}' to {score}")
            return True
        except RedisError as e:
            print(f"Production Error during ZADD: {e}")
            return False

    def get_top_rankings(self, leaderboard_name, top_n=10):
        """Safely retrieve the top N highest-scoring members with their scores."""
        try:
            # zrevrange fetches items from highest to lowest score
            # 0 is the first item, (top_n - 1) gives us exactly N items
            rankings = self.client.zrevrange(
                leaderboard_name, 
                0, 
                top_n - 1, 
                withscores=True
            )
            return rankings
        except RedisError as e:
            print(f"Production Error during ZREVRANGE: {e}")
            return []