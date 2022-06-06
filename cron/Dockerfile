FROM ubuntu:latest

ADD crontab /etc/cron.d/fetchdata-cron
RUN chmod 0644 /etc/cron.d/fetchdata-cron
RUN touch /var/log/cron.log
RUN apt-get update
RUN apt-get -y install cron
CMD cron && tail -f /var/log/cron.log