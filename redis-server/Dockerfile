FROM redis
COPY redis.conf /usr/local/etc/redis/redis.conf
COPY dump.rdb /usr/local/var/db/redis/dump.rdb
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
