#! /bin/sh
# /etc/init.d/moviegrabber.sh
 
# function that stops the daemon/service
do_start()
{
	# create moviegrabber writeable directory for pid file
	if [ ! -e /var/run/moviegrabber ]; then
		mkdir /var/run/moviegrabber
		chown root:users /var/run/moviegrabber
		chmod 0777 /var/run/moviegrabber
	fi

	# run moviegrabber as root, specifying daemon flag and pid file (used to kill moviegrabber process)
	sudo -u root python /home/xxx/Desktop/moviegrabber/MovieGrabber.py --daemon --pidfile /var/run/moviegrabber/moviegrabber.pid&
}

# function that stops the daemon/service
do_stop()
{
	# if moviegrabber not running then return
	if [ ! -r /var/run/moviegrabber/moviegrabber.pid ]; then
		return
	fi

	# kill moviegrabber process by reading pid file
	kill $(cat /var/run/moviegrabber/moviegrabber.pid)
	sleep 3
	
	# if pid file exists then delete
	if [ -f /var/run/moviegrabber/moviegrabber.pid ]; then
		rm /var/run/moviegrabber/moviegrabber.pid
	fi

	# wait for pid file to be deleted
	while [ -e /var/run/moviegrabber/moviegrabber.pid ]; do
		sleep 1
	done
}
 
case "$1" in
	start)
	echo "Starting moviegrabber..."
	do_start
	;;

	stop)
	echo "Stopping moviegrabber..."
	do_stop
	sleep 1
	;;

	restart)
	echo "Restarting moviegrabber..."
	do_stop
	do_start
	;;
	
	enable)
	echo "Enable autostart of moviegrabber..."
	/usr/sbin/update-rc.d moviegrabber.sh defaults
	;;

	disable)
	echo "Disable autostart of moviegrabber..."
	/usr/sbin/update-rc.d -f moviegrabber.sh remove
	;;

	*)
	echo "Usage: /etc/init.d/moviegrabber{start|stop|restart|enable|disable}"
	exit 1
	;;

esac

exit 0
