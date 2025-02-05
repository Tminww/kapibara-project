FROM python:3.9

WORKDIR /code

RUN apt-get update 

# RUN apt-get update && apt-get install -y \
#     cron \
#     rsyslog
# COPY ./cron.config /etc/cron.d/sample
# RUN mkdir /data
# CMD service rsyslog start && service cron start && tail -f /var/log/syslog

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src/ /code/

CMD [ "python3.9", "main.py" ]



