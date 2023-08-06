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


class RedisEngine:
    @staticmethod
    async def connect(
            host: str,
            port: int,
            db: int,
            password: Union[str, None] = None,
    ) -> Redis:

        """
        Connect to a Redis database.

        Attributes
        ----------
        :param host: The host of the Redis database.
        :param port: The port of the Redis database.
        :param password: The password of the Redis database.
        :param db: The database of the Redis database.
        :return: Redis
        ----------
        """

        redis = Redis(
            host=host,
            port=port,
            password=password,
            db=db
        )

        return redis
