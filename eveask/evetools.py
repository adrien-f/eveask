import cPickle
import datetime
import eveapi
import redis
import time
from .app import app

class RedisEveAPICacheHandler(object):

    def __init__(self, debug=False):
        self.debug = debug
        self.r = redis.StrictRedis(host=app.config['REDIS'])

    def log(self, what):
        if self.debug:
            print "[%s] %s" % (datetime.datetime.now().isoformat(), what)

    def retrieve(self, host, path, params):
        key = hash((host, path, frozenset(params.items())))

        cached = self.r.get(key)
        if cached is None:
            self.log("%s: not cached, fetching from server..." % path)
            return None
        else:
            cached = cPickle.loads(cached)
            if time.time() < cached[0]:
                self.log("%s: returning cached document" % path)
                return cached[1]
            self.log("%s: cache expired, purging !" % path)
            self.r.delete(key)

    def store(self, host, path, params, doc, obj):
        key = hash((host, path, frozenset(params.items())))

        cachedFor = obj.cachedUntil - obj.currentTime
        if cachedFor:
            self.log("%s: cached (%d seconds)" % (path, cachedFor))

            cachedUntil = time.time() + cachedFor
            self.r.set(key, cPickle.dumps((cachedUntil, doc), -1))


class EveTools(object):
    client = eveapi.EVEAPIConnection(cacheHandler=RedisEveAPICacheHandler(debug=app.config['DEBUG']))

    def __init__(self, key_id=None, vcode=None):
        if key_id and vcode:
            self.auth(key_id, vcode)

    def auth(self, key_id, vcode):
        self.key_id = key_id
        self.vcode = vcode
        self.client = self.client.auth(keyID=key_id, vCode=vcode)
        self.authed = True

