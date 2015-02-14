#!/usr/bin/env bash

# install nodejs from external ppa
sudo add-apt-repository -y ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get -y install python-software-properties python g++ make nodejs

# node based dev tools
sudo npm install -g grunt-cli
sudo npm install -g bower
sudo npm install -g webpack

# bower dependencies
sudo apt-get -y install git

cd /vagrant
npm install
bower install --config.interactive=false
