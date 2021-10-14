#!/bin/bash -xe

sudo apt-get update

sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release


curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker

sudo apt update
sudo apt install -y --force-yes docker-ce

USERNAME=$(cat /tmp/docker.username)
echo "LOADBALANCER IP: *********{$2}*******"


cat /tmp/docker.password | sudo docker login -u $USERNAME --password-stdin
sudo docker pull mgcrook11/quantum-app:1.5
sudo docker run -it -d --env-file /tmp/.env.deploy -p 80:8000 mgcrook11/quantum-app:1.5
sudo docker run -p 6379:6379 -d redis:5

apt-get update
apt-get -y install vim
