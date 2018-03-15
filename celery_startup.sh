#!/bin/bash

start() {
  ./run_celery
}

stop() {
  killall -9 celery
}

case "$1" in 
    start)
       start
       ;;
    stop)
       stop
       ;;
    *)
    echo "Usage: $0 {start|stop}"
esac

exit 0