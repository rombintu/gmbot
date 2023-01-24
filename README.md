# Good Morning Bot

## Установка
```bash
git clone https://github.com/rombintu/gmbot.git /opt/gmbot
cd /opt/gmbot
docker build -t gmbot .
docker run -d -e 'TOKEN=<YOUR_TOKEN>' --mount source=store,target=store --name gmbot gmbot
```