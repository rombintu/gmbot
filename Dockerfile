FROM python:3.10.9-alpine3.16
WORKDIR /opt
COPY . .
RUN cp /usr/share/zoneinfo/Europe/Moscow  /etc/localtime
RUN echo "Europe/Moscow" >  /etc/timezone
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
RUN apk add --no-cache gcc libcurl libc-dev pkgconfig gpgme-dev python3-dev tzdata && rm -rf /var/cache/apk/*
RUN pip install -r deps.txt
CMD ["python3", "./main.py"]