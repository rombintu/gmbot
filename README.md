# Good Morning Bot

## Установка
```bash
git clone https://github.com/rombintu/gmbot.git /opt/gmbot
cd /opt/gmbot
docker build -t gmbot .
docker run -d -e 'TOKEN=<YOUR_TOKEN>' -v $PWD/store:/opt/gmbot/store -name gmbot gmbot
```