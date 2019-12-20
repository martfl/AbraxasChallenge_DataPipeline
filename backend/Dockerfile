FROM python:buster
RUN pip install requests redis
COPY crontab /etc/cron.d/crontab
RUN apt-get update && apt-get install cron -y -qq
RUN chmod 0644 /etc/cron.d/crontab && crontab /etc/cron.d/crontab && touch /var/log/cron.log
COPY get_data.py .
CMD ["cron", "-f"]
