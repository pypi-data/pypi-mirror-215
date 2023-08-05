import motor.motor_asyncio

from bs_common_fastapi_mongodb.common.config.base import mongo_settings


async def get_db():
    db = motor.motor_asyncio.AsyncIOMotorClient(mongo_settings.MONGODB_URI)
    database = db[mongo_settings.MONGODB_DBNAME]
    try:
        yield database
    finally:
        db.close()
