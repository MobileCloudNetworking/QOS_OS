#!/bin/bash

# check correttezza sintax qos plug-in
if python -m py_compile /home/marco/Scrivania/neutron_juno/neutron/extensions/qos.py; then
	echo "extension qos.py syntax correct"
else exit 1
fi

# se sintassi corretta, copio sorgente plugin heat su VM
sshpass -p nextworks scp /home/marco/Scrivania/neutron_juno/neutron/extensions/qos.py nextworks@10.0.11.120:/opt/stack/neutron/neutron/extensions/
echo "extension qos.py sended to 10.0.11.120"

# check correttezza sintax port plug-in
if python -m py_compile /home/marco/Scrivania/neutron_juno/neutron/db/qos_db.py; then
	echo "qos_db.py syntax correct"
else exit 1
fi

# invio i sorgenti delle risorse port e network destinate a ospitare risorse di tipo QOS
sshpass -p nextworks scp /home/marco/Scrivania/neutron_juno/neutron/db/qos_db.py nextworks@10.0.11.120:/opt/stack/neutron/neutron/db/
echo "qos_db.py sended to 10.0.11.120"
