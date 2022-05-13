FROM python:3.8

WORKDIR /server
RUN mkdir /server/images
COPY . .

RUN pip3 install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

EXPOSE 5000

CMD /wait && -u python app.py
