#!/usr/bin/env bash

sudo apt-get install -y postgresql libpq-dev

sudo -u postgres createuser --superuser $USER
sudo -u postgres createdb $USER
sudo -u postgres createdb eve_sde
sudo -u postgres createdb eve_igbtoolbox

# eve user for tcp con
sudo -u postgres createuser --superuser eve
sudo -u postgres psql -U postgres -d postgres -c "alter user eve with password 'eve';"

echo "Installing EVE SDE"
cd $HOME
wget https://www.fuzzwork.co.uk/dump/postgres-latest.dmp.bz2
bzcat postgres-latest.dmp.bz2 | pg_restore --clean --no-acl --no-owner -d eve_sde && rm postgres-latest.dmp.bz2

# Use SSH tunneling as described here to get access with pgadmin:
# https://snakeycode.wordpress.com/2015/01/02/vagrant-postgresql-and-pgadmin/
# use user/password eve/eve
