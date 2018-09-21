import memcache

m = memcache.Client(['127.0.0.1:11211'],debug=True)
m.set('name','zhangsan',time=200)
print(m.get('name'))
m.delete('name')
print(m.get('name'))