import redis

# Connect to the Redis container
client = redis.Redis(
    host='localhost',
    port=6379,
    password='TopSecretDevPass123!',  # Use the password we set up
    decode_responses=True             # This makes Redis return normal strings instead of bytes
)

# Test the connection
try:
    print("Connecting to Redis...")
    response = client.ping()
    print(f"Connected! Server responded: {response}")
except Exception as e:
    print(f"Could not connect: {e}")