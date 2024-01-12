# Usa la imagen oficial de Python con Debian como base
# FROM python:3.9-slim-buster
FROM python:3.10
# FROM python:3.9.0b4-alpine3.12

RUN apt-get update && apt-get -y install cron libpq-dev gcc python3-dev vim procps

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el script de Python al directorio de trabajo
COPY script.py /app
RUN chmod +x /app/script.py

COPY crontab /etc/cron.d

RUN chmod 0644 /etc/cron.d/crontab

RUN pip install psycopg2-binary
ENV PATH=$PATH:/usr/bin/

# Instala las dependencias (si tienes algún archivo requirements.txt)
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

RUN /usr/bin/crontab /etc/cron.d/crontab

# Agrega el comando para ejecutar el script con cron
# CMD ["cron", "-f"]
# CMD service cron start && cron && tail -f /var/log/cron.log
CMD crond -l 2 -f >> /var/log/cron.log 2>&1