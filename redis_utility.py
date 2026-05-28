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