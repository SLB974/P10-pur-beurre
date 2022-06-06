FROM ubuntu:latest
MAINTAINER slb-fullweb.tech
RUN apt-get update && apt-get -y install cron

# copy cron task to cron jobs
COPY fetchdata-weekly-crontab /etc/cron.d/fetchdata-weekly-crontab

# give execution rights on the cron task
RUN chmod 0644 /etc/cron.d/fetchdata-weekly-crontab

# reference cron task to cron daemon
RUN crontab /etc/cron/fetchdata-weekly-crontab

#
ENTRYPOINT ["cron", "-f"]