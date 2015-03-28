#!/usr/bin/env bash

echo "Installing MongoDB"
su -c /vagrant/scripts/bootstrap-mongodb.sh  - vagrant
echo "Installing PostgreSQL"
su -c /vagrant/scripts/bootstrap-postgresql.sh  - vagrant
echo "Installing Python"
su -c /vagrant/scripts/bootstrap-python.sh  - vagrant
echo "Installing Python VENV"
su -c /vagrant/scripts/bootstrap-venv.sh  - vagrant
echo "Installing NodeJS tools"
su -c /vagrant/scripts/bootstrap-node.sh  - vagrant
