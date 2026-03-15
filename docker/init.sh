#!/bin/bash

set -e

if [ -d "/home/frappe/frappe-bench/apps/frappe" ]; then
	echo "Bench already exists, starting"
	cd /home/frappe/frappe-bench
	bench start
	exit 0
fi

echo "Creating new bench..."

bench init --skip-redis-config-generation frappe-bench --version version-15

cd /home/frappe/frappe-bench

# Use containers instead of localhost
bench set-mariadb-host mariadb
bench set-redis-cache-host redis://redis:6379
bench set-redis-queue-host redis://redis:6379
bench set-redis-socketio-host redis://redis:6379

# Remove redis, watch from Procfile
sed -i '/redis/d' ./Procfile
sed -i '/watch/d' ./Procfile

if [ -f "/workspace/crm/hooks.py" ]; then
	bench get-app crm /workspace
	cp -a /workspace/. /home/frappe/frappe-bench/apps/crm/
else
	bench get-app crm --branch main
fi

bench new-site crm.localhost \
    --force \
    --mariadb-root-password 123 \
    --admin-password admin \
    --no-mariadb-socket

bench --site crm.localhost install-app crm
bench --site crm.localhost set-config developer_mode 1
bench --site crm.localhost set-config mute_emails 1
bench --site crm.localhost set-config server_script_enabled 1
bench --site crm.localhost clear-cache
bench use crm.localhost

bench start
