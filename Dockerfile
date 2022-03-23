FROM python:3.8

WORKDIR /server
COPY . .

RUN pip3 install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

EXPOSE 8000

CMD /wait && python3 auth_test.py