VERSION=10

# stop service
systemctl stop postgresql.service

# upgrade
pacman -S postgresql postgresql-libs postgresql-old-upgrade

# backup data
mv /var/lib/postgres/data /var/lib/postgres/olddata
mkdir /var/lib/postgres/data /var/lib/postgres/tmp

# init database
chown postgres:postgres /var/lib/postgres/data /var/lib/postgres/tmp
sudo -u postgres -i
[postgres]$ initdb -D '/var/lib/postgres/data'

# data recovery
cd /var/lib/postgres/tmp
pg_upgrade -b /opt/pgsql-$VERSION/bin -B /usr/bin -d /var/lib/postgres/olddata -D /var/lib/postgres/data

# resatrt service
systemctl start postgresql.service