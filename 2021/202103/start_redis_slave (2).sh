redis-server /etc/redis.conf
redis-server /etc/redis.slave.conf
redis-server /etc/redis.slave2.conf
redis-sentinel /etc/redis-sentinel.conf &
redis-sentinel /etc/redis-sentinel_26380.conf &
