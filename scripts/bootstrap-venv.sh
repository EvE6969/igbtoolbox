#!/usr/bin/env bash

# create dedicated python virtual environment
mkdir /home/vagrant/venv
cd /home/vagrant/venv
virtualenv-3.4 -p python3 igbtoolbox-3
source igbtoolbox-3/bin/activate

# activate venv on login
echo 'source /home/vagrant/venv/igbtoolbox-3/bin/activate' > ~/.bash_aliases

# install python dependencies in venv
pip install tornado
pip install motor
pip install sockjs-tornado
pip install apscheduler
pip install PyYAML
#pip install networkx
pip install aiopg

sudo bash -c "echo '127.0.0.1 database' >> /etc/hosts"
