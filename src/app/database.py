import json

from dynaconf import settings
from pymongo import MongoClient
from pymongo.collation import Collation, CollationStrength
from redis import ConnectionPool, Redis

class MongoDBConnection:
    def __init__(self):
        self.host = settings.MONGO_HOST
        self.port = 27017
        self.client:MongoClient

    def __enter__(self):
        self.client = MongoClient(self.host, self.port)
        return self.client

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()


class  MongoDB:

    def drop_collection(self,coll) -> dict:
        """
        Reponsavel por deletar toda tabela MongoDB
        :params: Dict
        :params: coll: str
        :return: Dict
        """

        with MongoDBConnection() as client:
            _db_client = client[settings.MONGO_DB]
            collection = _db_client[coll]
            response = collection.drop()
        return {"message":"Drop sucesso.", "data":response}

    def find_and_update_by_options(self,coll: str, value_update: dict, value_id: dict) -> dict:
        """
        Find item mongo find_and_update_by_options
        :params: Dict
        :params: coll: str
        :return: Dict
        """

        with MongoDBConnection() as client:
            _db_client = client[settings.MONGO_DB]
            collection = _db_client[coll]
            response = collection.find_one_and_update(
                value_id,{'$set': value_update},
                upsert=True,
                collation=Collation(locale='de',strength=CollationStrength.SECONDARY)
            )
        return {"message":"Alteração realizada com sucesso.", "data":response}


class RedisConnection:
    """"
    Class manager cont redis db
    """

    def __init__(self, db: int):
        """"
        Class starting redis db
        """
        self.db = db
        self.pool: ConnectionPool = None
        self.connection: Redis = None

    def __enter__(self):
        """
        Open connection redis
        """
        self.pool = ConnectionPool(
            decode_responses=True,
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=self.db
        )
        self.connection = Redis(connection_pool=self.pool)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close connection redis
        """
        self.pool.disconnect()


class RedisDB:
    """
    Class responsible for cache
    """

    def __init__(self, db:int):
        """
        Class conn redis
        """
        self.db = db

    def flushall_key(self) -> int:
        """
        Count obj in scan redis
        """
        with RedisConnection(self.db) as redis:
            return redis.flushall()

    def search(self, key: str):
        """
        Search token in redis
        """

        with RedisConnection(self.db) as redis:
            return redis.get(key)

    def save(self,key:str, obj:str, ex_token: int) -> bool:
        """
        Save token in redis
        """

        obj_parse_json = json.dumps(obj)
        with RedisConnection(self.db) as redis:
            redis.set(key, obj_parse_json, ex_token)
        return True

    def keys(self) -> int:
        """
        Count obj in scan redis
        """
        with RedisConnection(self.db) as redis:
            return redis.keys()
