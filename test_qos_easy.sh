#!/bin/bash

# attacca screen 
screen -x stack

#lancia demon heat engine
/opt/stack/heat/bin/heat-engine --config-file=/etc/heat/heat.conf & echo $! >/opt/stack/status/stack/h-eng.pid; fg || echo "h-eng failed to start" | tee "/opt/stack/status/stack/h-eng.failure"
