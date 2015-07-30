#!/bin/bash

# check correttezza sintax risorsa
if python -m py_compile /home/marco/openstack/heat_juno/heat/engine/resources/neutron/qos.py; then
	echo "qos.py correct syntax"
else exit 1
fi
