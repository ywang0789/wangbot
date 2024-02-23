#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

apt-get update

# git
apt-get install -y git

# ptyhon stuff
apt-get install -y python3 python3-pip python3-venv

# tmux <3
apt-get install -y tmux




