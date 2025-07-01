#!/bin/bash

set -e  # Остановить скрипт при любой ошибке

BIN_PATH=$(pwd)/../bin
cd "$BIN_PATH"

echo "✅ Распаковка Docker..."
tar xzvf docker-24.0.7.tgz

echo "📁 Установка бинарников Docker..."
sudo install -m 755 docker/* /usr/bin/

# Создание группы docker, если не существует
if ! getent group docker > /dev/null; then
    echo "👥 Создание группы docker..."
    sudo groupadd docker
else
    echo "👥 Группа docker уже существует."
fi

echo "➕ Добавление пользователя '$USER' в группу docker..."
sudo usermod -aG docker $USER

# Создание systemd сервиса без зависимости от containerd
echo "🛠️ Создание systemd-сервиса Docker..."
sudo tee /etc/systemd/system/docker.service > /dev/null <<EOF
[Unit]
Description=Docker Daemon
Documentation=https://docs.docker.com
After=network.target

[Service]
ExecStart=/usr/bin/dockerd
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
TimeoutStartSec=0
RestartSec=2
StartLimitBurst=3
StartLimitInterval=60s
Delegate=yes
KillMode=process
OOMScoreAdjust=-500
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
TasksMax=infinity

[Install]
WantedBy=multi-user.target
EOF

# Создание socket-файла (оставляем по желанию)
echo "🔌 Создание docker.socket..."
sudo tee /etc/systemd/system/docker.socket > /dev/null <<EOF
[Unit]
Description=Docker Socket for the API

[Socket]
ListenStream=/var/run/docker.sock
SocketMode=0660
SocketUser=root
SocketGroup=docker

[Install]
WantedBy=sockets.target
EOF

# Установка Docker Compose
echo "⚙️ Установка docker-compose..."
sudo cp docker-compose-linux-x86_64 /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

# Перезапуск systemd
echo "🔄 Перезапуск systemd и запуск Docker..."
sudo systemctl daemon-reload
sudo systemctl enable docker.service
sudo systemctl enable docker.socket
sudo systemctl start docker.socket
sudo systemctl start docker.service

# Проверка статуса
echo "🔍 Проверка статуса Docker:"
sudo systemctl status docker --no-pager

# Установка lazydocker
echo "📦 Установка LazyDocker..."
tar -xzf lazydocker_0.24.1_Linux_x86_64.tar.gz
sudo mv lazydocker /usr/local/bin/
sudo chmod +x /usr/local/bin/lazydocker

echo ""
echo "✅ Docker и LazyDocker установлены."
echo "🔄 Выйдите из системы и войдите снова, чтобы применить группу docker."
