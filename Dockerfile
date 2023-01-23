FROM python:3.10.9-alpine3.16
WORKDIR /opt
COPY . .
RUN apk add --no-cache gcc libcurl libc-dev pkgconfig gpgme-dev python3-dev && rm -rf /var/cache/apk/*
RUN pip install -r deps.txt
CMD ["python3", "./main.py"]