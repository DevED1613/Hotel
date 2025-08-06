from src.connectors.redis_connector import RedisConnector
from src.config import settings

redis_manager = RedisConnector(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
