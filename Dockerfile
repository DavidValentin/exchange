# Imagen Python
FROM python:3.10

RUN apt-get update && apt-get -y install cron vim

WORKDIR /app

COPY crontab /etc/cron.d/crontab
COPY script.py /app/script.py
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# Run crond as main process of container
CMD ["cron", "-f"]