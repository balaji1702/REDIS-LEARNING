import redis
from redis.exceptions import ConnectionError, TimeoutError

class RedisProductionClient:
    def __init__(self, host='localhost', port=6379, password=None, db=0):
        # 1. Initialize a connection pool to manage reusable connections safely
        self.pool = redis.ConnectionPool(
            host=host, 
            port=port, 
            password=password, 
            db=db,
            decode_responses=True, # Automatically converts bytes to Python strings
            max_connections=10,    # Prevents overloading the Redis server
            socket_timeout=2.0     # Blow up if the network hangs for > 2 seconds
        )
        self.client = redis.Redis(connection_pool=self.pool)

    def get_client(self):
        return self.client

    def execute_transaction(self, operations_callback):
        """
        Executes multiple commands in a single network round-trip.
        """
        # 2. Create a pipeline pipeline context manager
        with self.client.pipeline(transaction=True) as pipe:
            try:
                # Pass the pipeline to our custom logic function
                operations_callback(pipe)
                # Execute everything bundled together
                return pipe.execute()
            except (ConnectionError, TimeoutError) as e:
                print(f"Production Alert: Redis network failure! {e}")
                raise