#!/bin/bash

# Обновление системы
echo "Обновление системы..."
sudo apt update && sudo apt upgrade -y

# Установка Nginx и Tor
echo "Установка Nginx и Tor..."
sudo apt install -y nginx tor

# Настройка Nginx
SITE_NAME="yourdomain.onion"
SITE_DIR="/var/www/mysite"

echo "Настройка Nginx для сайта $SITE_NAME..."

# Создание конфигурационного файла для Nginx
sudo bash -c "cat > /etc/nginx/sites-available/mysite <<EOF
server {
    listen 80;
    server_name $SITE_NAME;

    location / {
        root $SITE_DIR;
        index index.html index.htm;
    }
}
EOF"

# Создание каталога для сайта и тестового файла
sudo mkdir -p $SITE_DIR
echo "<h1>Hello, Tor!</h1>" | sudo tee $SITE_DIR/index.html

# Включение конфигурации Nginx
sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# Настройка Tor
echo "Настройка Tor..."

# Добавление конфигурации для скрытой службы
sudo bash -c "echo -e 'HiddenServiceDir /var/lib/tor/hidden_service/\nHiddenServicePort 80 127.0.0.1:80' >> /etc/tor/torrc"

# Создание каталога для скрытой службы
sudo mkdir -p /var/lib/tor/hidden_service/
sudo chown -R debian-tor:debian-tor /var/lib/tor/hidden_service/

# Перезапуск Tor
sudo systemctl restart tor

# Получение .onion адреса
ONION_ADDRESS=$(sudo cat /var/lib/tor/hidden_service/hostname)

echo "Сайт успешно установлен! Ваш .onion адрес: $ONION_ADDRESS"
