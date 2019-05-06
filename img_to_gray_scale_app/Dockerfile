FROM ubuntu:xenial

COPY ./requirements .

RUN apt-get update \
    && apt-get install -y curl python3 sqlite3 \
    && apt-get clean \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py \
    && pip install -r requirements && rm requirements

WORKDIR /usr/src/app/
COPY ./app/ .

EXPOSE 8080
CMD python3 manage.py runserver 0.0.0.0:8080 --insecure
