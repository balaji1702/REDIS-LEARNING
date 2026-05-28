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