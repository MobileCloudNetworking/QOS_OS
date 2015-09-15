#!/bin/bash

cmd="$1"
vsctl="sudo ovs-vsctl"
ofctl="sudo ovs-ofctl"

case $cmd in
    up)
        echo "Prepare OVS Qos"
        set -x
        #$vsctl set port tap02 qos=@newqos -- --id=@newqos create qos type=linux-htb \
        #        other-config:max-rate=40000000000 \
        #        queues:123=@q1 queues:234=@q2 -- \
        #        --id=@q1 create queue other-config:max-rate=5000000 -- \
        #        --id=@q2 create queue other-config:max-rate=10000000
        $vsctl set port tap02 qos=@newqos -- --id=@newqos create qos type=linux-htb \
                other-config:max-rate=40000000000 \
                queues:123=@q1 -- \
                --id=@q1 create queue other-config:max-rate=5000000
        $ofctl add-flow obr0 in_port=1,dl_type=0x0800,nw_proto=17,action=set_queue:123,normal
        set +x
        ;;

    down)
        echo "Unprepare OVS Qos"
        set -x
        $ofctl del-flows obr0 in_port=1,dl_type=0x0800,nw_proto=17
        $vsctl clear port tap02 qos
        $vsctl -- --all destroy QoS -- --all destroy Queue
        set +x
        ;;

    *)
        echo "Usage: $0 up|down"
        exit 1
        ;;
esac
