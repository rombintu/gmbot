FROM python:3.10.9-alpine3.16
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apk add --no-cache gcc libcurl libc-dev pkgconfig gpgme-dev python3-dev tzdata musl-locales musl-locales-lang && rm -rf /var/cache/apk/*
COPY ./internal ./*.py /opt/
WORKDIR /opt
RUN cp /usr/share/zoneinfo/Europe/Moscow  /etc/localtime
RUN echo "Europe/Moscow" >  /etc/timezone
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
CMD ["python3", "./main.py"]