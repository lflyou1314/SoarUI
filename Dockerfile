FROM python:latest

RUN mkdir /root/soarui
COPY ./  /root/soarui

WORKDIR /root/soarui

RUN pip install -r requirements.txt

RUN chmod -R 777 ./soar
RUN chmod 777 ./script/docker-entrypoint.sh

ENTRYPOINT ["./script/docker-entrypoint.sh"]