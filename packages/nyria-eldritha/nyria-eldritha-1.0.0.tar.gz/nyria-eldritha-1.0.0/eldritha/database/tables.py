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

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.asyncio import AsyncEngine

from zenith.ServicesManager import ServicesManager
from sqlalchemy.exc import ProgrammingError, DBAPIError


class Tables:
    @staticmethod
    async def create_tables(meta: MetaData) -> None:

        """
        Creates the tables in the database.

        Attributes
        ----------
        :param tables:
        :param meta:
        :return:
        ----------

        """

        engine: AsyncEngine = await ServicesManager.get_service("database")

        async with engine.begin() as conn:
            await conn.run_sync(meta.create_all)
