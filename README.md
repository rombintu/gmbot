# Good Morning Bot

## Установка
```bash
git clone https://github.com/rombintu/gmbot.git /opt/gmbot
cd /opt/gmbot
docker build -t gmbot .
touch $(pwd)/db.sqlite # Init empty Database
docker run -d -e 'TOKEN=<YOUR_TOKEN>' -v $(pwd)/db.sqlite:/opt/db.sqlite --restart unless-stopped --name gmbot gmbot
```