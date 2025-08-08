import logging

from redis.asyncio import Redis


class RedisConnector:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def connect(self):
        logging.info(f"starting connection to the Redis server {self.host}:{self.port}")
        self._redis = await Redis(host=self.host, port=self.port)
        logging.info(
            f"Successful connection to the Redis server {self.host}:{self.port}"
        )

    async def set(self, key: str, value: str, expiration: int | None = None):
        if expiration:
            await self._redis.set(key, value, ex=expiration)
        else:
            await self._redis.set(key, value)

    async def get(self, key: str):
        return await self._redis.get(key)

    async def delete(self, key: str):
        await self._redis.delete(key)

    async def close(self):
        if self._redis:
            await self._redis.close()
