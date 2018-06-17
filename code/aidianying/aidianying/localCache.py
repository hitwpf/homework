import os
import hashlib

try:
    import cPickle as pickle
except ImportError:
    import pickle


class localCache:
    __cache = {}
    __count = 0
    __max_size = 1000

    @classmethod
    def add(cls, key, value):
        if cls.__count > cls.__max_size:
            for key in cls.__cache.keys():
                del cls.__cache[key]
        cls.__cache[key] = value
        if key == 1:
            cls.persistent(value, key)

    @classmethod
    def get(cls, key):
        if cls.__cache.__contains__(key):
            return cls.__cache[key]
        if key == 1:
            result = cls.getPersistent(key)
            if result is not None:
                cls.add(key, result)
                return result
        return None

    @classmethod
    def persistent(cls, obj, key):
        hl = hashlib.md5()
        hl.update(str(key).encode(encoding='utf-8'))
        f = open(os.path.abspath('.') + "/temp/" + hl.hexdigest() + ".dat", "wb")
        pickle.dump(obj, f)
        f.close()

    @classmethod
    def getPersistent(cls, key):
        hl = hashlib.md5()
        hl.update(str(key).encode(encoding='utf-8'))
        path = os.path.abspath('.') + "/temp/" + hl.hexdigest() + ".dat"
        if not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            return pickle.load(f)