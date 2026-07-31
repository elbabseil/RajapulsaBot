import time


class CacheService:

    def __init__(self):
        self._cache = {}

    def set(self, key, value, ttl=300):
        self._cache[key] = {
            "value": value,
            "expired": time.time() + ttl
        }

    def get(self, key):

        item = self._cache.get(key)

        if item is None:
            return None

        if time.time() > item["expired"]:
            del self._cache[key]
            return None

        return item["value"]

    def clear(self, key=None):

        if key:
            self._cache.pop(key, None)
        else:
            self._cache.clear()


cache = CacheService()