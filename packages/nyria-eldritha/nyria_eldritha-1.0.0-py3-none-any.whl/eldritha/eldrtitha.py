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

from zenith.ServicesManager import ServicesManager

from eldritha.database.engine import Engine, AsyncEngine
from eldritha.redis_client.redis_engine import RedisEngine, Redis


class Eldritha:
    @staticmethod
    async def database_engine(url: str) -> Union[AsyncEngine]:

        """
        Connect to the database and register it as service.

        Attributes
        ----------
        :param url: The url to connect to the database with.
        :return: None
        ----------

        """

        engine: AsyncEngine = await ServicesManager.get_service("database")

        if engine is None:
            engine: AsyncEngine = await Engine.create_engine(url)
            await ServicesManager.register_service("database", engine)

        return engine

    @staticmethod
    async def connect_to_redis(host: str, port: int, db: int, password: Union[str, None] = None) -> Union[Redis]:

        """
        Connect to the redis_client database and register it globally as service.

        Attributes
        ----------
        :return:
        ----------

        """

        redis: Redis = await ServicesManager.get_service("redis_client")

        if redis is None:
            redis: Redis = await RedisEngine.connect(
                host=host,
                port=port,
                db=db,
                password=password
            )
            await ServicesManager.register_service("redis", redis)

        return redis
