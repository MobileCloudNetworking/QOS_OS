#!/bin/bash

source openrc
mysql -u root << EOF
use mysql;
drop database heat;
CREATE DATABASE heat;
GRANT ALL PRIVILEGES ON heat.* TO 'root'@'localhost' IDENTIFIED BY 'nextworks';
GRANT ALL PRIVILEGES ON heat.* TO 'root'@'%' IDENTIFIED BY 'nextworks';
exit
EOF
heat-manage db_sync

