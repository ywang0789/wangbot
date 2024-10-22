#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

apt-get update -y && apt-get upgrade -y && apt-get dist-upgrade -y 

# git
apt-get install -y git

# ptyhon stuff
apt-get install -y python3 python3-pip python3-venv

# tmux <3
apt-get install -y tmux

git clone https://github.com/ywang0789/wangbot.git
git pull origin master
python3 -m venv wangbot/venv
source wangbot/venv/bin/activate
pip3 install -r wangbot/requirements.txt




