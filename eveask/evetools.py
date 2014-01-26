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

    def __init__(self, key_id=None, vcode=None, cache=True):
        if cache:
            self.client = eveapi.EVEAPIConnection(cacheHandler=RedisEveAPICacheHandler(debug=app.config['DEBUG']))
        else:
            self.client = eveapi.EVEAPIConnection()
        if key_id and vcode:
            self.auth(key_id, vcode)

    def auth(self, key_id, vcode):
        self.key_id = key_id
        self.vcode = vcode
        self.client = self.client.auth(keyID=key_id, vCode=vcode)
        self.authed = True

    def safe_request(self, request, kwargs=None):
        try:
            req = getattr(self.client, request)
            if kwargs is not None:
                results = req(**kwargs)
            else:
                results = req()
        except eveapi.Error as e:
            app.logger.exception(e)
            raise Exception('API Error, {}'.format(e.message))
        except RuntimeError as e:
            app.logger.exception(e)
            raise Exception('CCP Server Error, {}'.format(e.message))
        except Exception as e:
            app.logger.exception(e)
            raise Exception('System error, our team has been notified !')
        return results

    def check_key(self):
        key_info = self.safe_request('account/APIKeyInfo')
        access_mask, key_type, expires = key_info.key.accessMask, key_info.key.type, key_info.key.expires
        if access_mask != 8388608:
            raise Exception('Invalid access mask')
        if key_type not in ['Character', 'Account']:
            raise Exception('Invalid key type')
        if expires != "":
            raise Exception('Expiration detected on key')
        return True

    def get_characters(self):
        key_info = self.safe_request('account/APIKeyInfo')
        characters = []
        for character in key_info.key.characters:
            characters.append(self.safe_request('eve/CharacterInfo', {'characterID': character['characterID']}))
        return characters

