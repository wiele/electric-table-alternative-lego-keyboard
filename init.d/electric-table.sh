#! /bin/sh
### BEGIN INIT INFO
# Provides:          electric-table.py
# Required-Start:    $all
# Required-Stop:     
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Driver for the alternative lego keybord of the electric table in Filip's room :)))
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/bin

. /lib/init/vars.sh
. /lib/lsb/init-functions
# If you need to source some other scripts, do it here

case "$1" in
  start)
    log_begin_msg "Starting electric table alternative lego keyboard service..."
	/home/pi/electric-table-alternative-lego-keyboard/electric-table.py >> /var/log/electric-table.log &
    log_end_msg $?
    exit 0
    ;;
  stop)
    log_begin_msg "Stopping electric table alternative lego keyboard service..."
	# TODO: do it more elegantly
	killall electric-table.py
    log_end_msg $?
    exit 0
    ;;
  *)
    echo "Usage: /etc/init.d/electric-table {start|stop}"
    exit 1
    ;;
esac
