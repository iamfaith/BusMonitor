import redis
from openpyxl.compat.singleton import Singleton

import conf


class RedisConf(metaclass=Singleton):
    def __init__(self):
        self.pool = redis.ConnectionPool(host=conf.redis_server, port=conf.redis_port, decode_responses=True)
        print('init')

    def exist(self, key):
        re = redis.StrictRedis(connection_pool=self.pool)
        return re.exists(key)

    def hash_set(self, *args):
        re = redis.StrictRedis(connection_pool=self.pool)
        re.hset(*args)

    def hash_getall(self, name):
        re = redis.StrictRedis(connection_pool=self.pool)
        return re.hgetall(name)


if __name__ == '__main__':
    r = RedisConf()
    r.hash_set('test', 'aa', 'bb')
    print(r.hash_getall('test')['isOn'] is False)
    r = RedisConf()
