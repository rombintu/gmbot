# Good Morning Bot

## Установка
```bash
git clone https://github.com/rombintu/gmbot.git /opt/gmbot
cd /opt/gmbot
docker build -t gmbot .
touch $(pwd)/store/db.sqlite # Init empty Database
docker run -d -e 'TOKEN=<YOUR_TOKEN>' -v $(pwd)/store/db.sqlite:/opt/store/db.sqlite --restart unless-stopped --name gmbot gmbot
```