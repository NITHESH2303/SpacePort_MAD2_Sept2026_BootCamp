import redis

redis_client = redis.Redis(host='localhost', port=6379, db=14, decode_responses=True)