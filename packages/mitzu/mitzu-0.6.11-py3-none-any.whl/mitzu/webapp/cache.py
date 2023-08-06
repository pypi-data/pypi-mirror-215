import mitzu.webapp.configs as configs
import redis
import diskcache
from typing import Any, Optional, List, Dict
from abc import ABC
from dataclasses import dataclass
import pickle
import mitzu.helper as H
import flask


class MitzuCache(ABC):
    def put(self, key: str, val: Any, expire: Optional[float] = None) -> None:
        """Puts some data to the storage

        Args:
            key (str): the key of the data
            val (Any): the picklable value
            expire (Optional[float], optional): seconds until expiration

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError()

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        raise NotImplementedError()

    def clear(self, key: str) -> None:
        raise NotImplementedError()

    def clear_all(self, prefix: Optional[str] = None) -> None:
        for key in self.list_keys(prefix):
            self.clear(key)

    def list_keys(
        self, prefix: Optional[str] = None, strip_prefix: bool = True
    ) -> List[str]:
        raise NotImplementedError()

    def health_check(self):
        raise NotImplementedError()


@dataclass(frozen=True, init=False)
class DiskMitzuCache(MitzuCache):

    _disk_cache: diskcache.Cache
    _global_prefix: Optional[str] = None

    def __init__(self, name: str, global_prefix: Optional[str] = None) -> None:
        super().__init__()
        object.__setattr__(
            self,
            "_disk_cache",
            diskcache.Cache(timeout=10, directory=f"./storage/{name}"),
        )
        object.__setattr__(
            self,
            "_global_prefix",
            global_prefix,
        )

    def __post_init__(self):
        H.LOGGER.info("Vacuuming disk cache")
        self._disk_cache._sql("vacuum")

    def _get_key(self, key: str) -> str:
        if self._global_prefix:
            return f"{self._global_prefix}.{key}"
        return key

    def put(self, key: str, val: Any, expire: Optional[float] = None):
        key = self._get_key(key)
        self.clear(key)
        if val is not None:
            H.LOGGER.debug(f"PUT: {key}: {type(val)}")
            self._disk_cache.add(key, value=val, expire=expire)
        else:
            H.LOGGER.debug(f"PUT: {key}: None")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        key = self._get_key(key)
        res = self._disk_cache.get(key)
        if res is not None:
            H.LOGGER.debug(f"GET: {key}: {type(res)}")
            return res
        else:
            H.LOGGER.debug(f"GET: {key}: None")
            return default

    def clear(self, key: str) -> None:
        key = self._get_key(key)
        H.LOGGER.debug(f"Clear {key}")
        self._disk_cache.pop(key)

    def list_keys(
        self, prefix: Optional[str] = None, strip_prefix: bool = True
    ) -> List[str]:
        if prefix is None:
            prefix = self._global_prefix
        else:
            prefix = self._get_key(prefix)

        keys = self._disk_cache.iterkeys()
        start_pos = len(prefix) if strip_prefix and prefix is not None else 0
        res = [k[start_pos:] for k in keys if prefix is None or k.startswith(prefix)]
        if H.LOGGER.getEffectiveLevel() == H.logging.DEBUG:
            H.LOGGER.debug(f"LIST {prefix}: {res}")
        return res

    def get_disk_cache(self) -> diskcache.Cache:
        return self._disk_cache

    def health_check(self):
        self.get_disk_cache().get("health_check", "ok")


@dataclass(frozen=True)
class RequestCache(MitzuCache):
    """This cache is in-memory however it is ephemeral, it only stores values until the end of the request
    This is because it is not picklable.
    """

    delegate: MitzuCache

    def _get_request_cache(self) -> Dict[str, Any]:
        if flask.has_app_context():
            if "request_cache" not in flask.g:
                flask.g.request_cache = {}
            return flask.g.get("request_cache")
        return {}

    def put(self, key: str, val: Any, expire: Optional[float] = None):
        self.delegate.put(key, val, expire)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        res = self._get_request_cache().get(key)
        if res is None:
            res = self.delegate.get(key, default)

        return res

    def clear(self, key: str) -> None:
        cache = self._get_request_cache()
        if key in cache:
            cache.pop(key)
        self.delegate.clear(key)

    def list_keys(
        self, prefix: Optional[str] = None, strip_prefix: bool = True
    ) -> List[str]:
        return self.delegate.list_keys(prefix, strip_prefix)

    def health_check(self):
        return self.delegate.health_check()


class RedisException(Exception):
    pass


@dataclass(init=False, frozen=True)
class RedisMitzuCache(MitzuCache):

    _redis: redis.Redis
    _global_prefix: Optional[str] = None

    def __init__(
        self,
        redis_cache: Optional[redis.Redis] = None,
        global_prefix: Optional[str] = None,
    ) -> None:
        super().__init__()

        if redis_cache is not None:
            object.__setattr__(self, "_redis", redis_cache)
            object.__setattr__(self, "_global_prefix", global_prefix)
        else:
            if configs.CACHE_REDIS_URL is None:
                raise ValueError(
                    "CACHE_REDIS_URL env variable is not set, can't create redis cache."
                )
            object.__setattr__(
                self, "_redis", redis.Redis.from_url(url=configs.CACHE_REDIS_URL)
            )
            object.__setattr__(self, "_global_prefix", global_prefix)

    def _get_key(self, key: str) -> str:
        if self._global_prefix:
            return f"{self._global_prefix}.{key}"
        return key

    def put(self, key: str, val: Any, expire: Optional[float] = None):
        key = self._get_key(key)
        pickled_value = pickle.dumps(val)
        if H.LOGGER.getEffectiveLevel() == H.logging.DEBUG:
            H.LOGGER.debug(f"PUT: {key}: {len(pickled_value)}")
        res = self._redis.set(name=key, value=pickled_value, ex=expire)
        if not res:
            raise RedisException(f"Couldn't set {key}")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        key = self._get_key(key)
        res = self._redis.get(name=key)
        if res is None:
            H.LOGGER.debug(f"GET: {key}: None")
            if default is not None:
                return default
            return None
        if H.LOGGER.getEffectiveLevel() == H.logging.DEBUG:
            H.LOGGER.debug(f"GET: {key}: {len(res)}")
        return pickle.loads(res)

    def clear(self, key: str) -> None:
        key = self._get_key(key)
        H.LOGGER.debug(f"CLEAR: {key}")
        self._redis.delete(key)

    def list_keys(
        self, prefix: Optional[str] = None, strip_prefix: bool = True
    ) -> List[str]:
        if prefix:
            prefix = self._get_key(prefix)
        elif self._global_prefix is not None:
            prefix = self._global_prefix
        else:
            prefix = ""
        keys = self._redis.keys(f"{prefix}*")
        start_pos = len(prefix) if strip_prefix else 0
        res = [k.decode()[start_pos:] for k in keys]
        if H.LOGGER.getEffectiveLevel() == H.logging.DEBUG:
            H.LOGGER.debug(f"LIST prefix={prefix}: {res}")
        return res

    def health_check(self):
        self._redis.get("health_check")
