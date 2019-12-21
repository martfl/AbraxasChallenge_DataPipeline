FROM redis
COPY redis.conf /usr/local/etc/redis/redis.conf
WORKDIR /var/lib/redis
COPY dump.rdb /var/lib/redis/dump.rdb
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
