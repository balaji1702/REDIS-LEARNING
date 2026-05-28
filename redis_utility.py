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
        
    def set_value(self, key, value):
        """Safely write a string value to Redis."""
        try:
            # We use the internal client to execute the standard SET command
            self.client.set(key, value)
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