#  All Rights Reserved
#  Copyright (c) 2023 Nyria
#
#  This code, including all accompanying software, documentation, and related materials, is the exclusive property
#  of Nyria. All rights are reserved.
#
#  Any use, reproduction, distribution, or modification of the code without the express written
#  permission of Nyria is strictly prohibited.
#
#  No warranty is provided for the code, and Nyria shall not be liable for any claims, damages,
#  or other liability arising from the use or inability to use the code.

from typing import Union
from redis.client import Redis

from zenith.ServicesManager import ServicesManager


class Scope:
    def __init__(self, category: str, prefix: str = "/"):
        self.__category = category
        self.__prefix = prefix

    @staticmethod
    async def __check_redis_connection() -> None:
        redis: Redis = await ServicesManager.get_service("redis")

        if redis is None:
            raise Exception("Redis is not registed and connected to the service manager.")

    async def get(self, key: str) -> Union[str, None]:

        """
        Get a value from the redisDatabase database

        Attributes
        ----------
        :param key: The key to get
        :return: Union[str, None]
        ----------
        """

        await self.__check_redis_connection()
        redis = await ServicesManager.get_service("redis")

        return redis.get(self.__prefix + key)

    async def set(self, key: str, value: str) -> None:

        """
        Set a value in the redisDatabase database

        Attributes
        ----------
        :param key: The key to set
        :param value: The value to set
        :return: None
        ----------

        """

        await self.__check_redis_connection()
        redis = await ServicesManager.get_service("redis")

        redis.set(self.__prefix + key, value)

    async def delete(self, key: str) -> None:

        """
        Delete a value from the redisDatabase database

        Attributes
        ----------
        :param key: The key to delete
        :return: None
        ----------

        """

        await self.__check_redis_connection()
        redis = await ServicesManager.get_service("redis")

        redis.delete(self.__prefix + key)

    async def exists(self, key: str) -> int:

        """
        Check if a value exists in the redisDatabase database

        Attributes
        ----------
        :param key: The key to check
        :return: bool
        ----------

        """

        await self.__check_redis_connection()
        redis = await ServicesManager.get_service("redis")

        return redis.exists(self.__prefix + key)

    async def expire(self, key: str, seconds: int) -> None:

        """
        Set a key to expire in the redisDatabase database

        Attributes
        ----------
        :param key: The key to expire
        :param seconds: The amount of seconds to expire the key in
        :return: None
        ----------

        """

        await self.__check_redis_connection()
        redis = await ServicesManager.get_service("redis")

        redis.expire(self.__prefix + key, seconds)

    async def ttl(self, key: str) -> int:

        """
        Get the time to live of a key in the redisDatabase database

        Attributes
        ----------
        :param key: The key to get the time to live of
        :return: int
        ----------

        """

        await self.__check_redis_connection()
        redis = await ServicesManager.get_service("redis")

        return redis.ttl(self.__prefix + key)

    async def keys(self, pattern: str) -> list:

        """
        Get all keys in the redisDatabase database that match a pattern

        Attributes
        ----------
        :param pattern: The pattern to match
        :return: list
        ----------

        """

        await self.__check_redis_connection()
        redis = await ServicesManager.get_service("redis")

        return redis.keys(self.__prefix + pattern)
