import memcache

mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def saveCache(key,value,time=0) :
    mc.set(key=key,val=value,time=time)

def getCache(key):
    return mc.get(key)

def delete(key):
    mc.delete(key)