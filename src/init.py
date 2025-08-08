from src.config import settings
from src.connectors.redis_connector import RedisConnector

redis_manager = RedisConnector(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
