#!/bin/bash

# check correttezza sintax qos plug-in
if python -m py_compile /home/marco/openstack/heat_juno/heat/engine/resources/neutron/qos.py; then
	echo "plug-in qos.py syntax correct"
else exit 1
fi

# se sintassi corretta, copio sorgente plugin heat su VM
sshpass -p nextworks scp /home/marco/openstack/heat_juno/heat/engine/resources/neutron/qos.py nextworks@10.0.11.120:/opt/stack/heat/heat/engine/resources/neutron
echo "resource plug-in qos.py sended to 10.0.11.120"

# check correttezza sintax port plug-in
if python -m py_compile /home/marco/openstack/heat_juno/heat/engine/resources/neutron/port.py; then
	echo "plug-in port.py syntax correct"
else exit 1
fi

# invio i sorgenti delle risorse port e network destinate a ospitare risorse di tipo QOS
sshpass -p nextworks scp /home/marco/openstack/heat_juno/heat/engine/resources/neutron/port.py nextworks@10.0.11.120:/opt/stack/heat/heat/engine/resources/neutron
echo "resource plug-in port.py sended to 10.0.11.120"

# check correttezza sintax net plug-in
if python -m py_compile /home/marco/openstack/heat_juno/heat/engine/resources/neutron/net.py; then
	echo "plug-in ne.py syntax correct"
else exit 1
fi

# invio i sorgenti delle risorse port e network destinate a ospitare risorse di tipo QOS
sshpass -p nextworks scp /home/marco/openstack/heat_juno/heat/engine/resources/neutron/net.py nextworks@10.0.11.120:/opt/stack/heat/heat/engine/resources/neutron
echo "resource plug-in net.py sended to 10.0.11.120"

# check correttezza sintax client neutron plug-in
if python -m py_compile /home/marco/openstack/python-neutronclient-v2.3.11/neutronclient/v2_0/client.py; then
	echo "client plug-in client.py syntax correct"
else exit 1
fi

# invio i sorgenti delle risorse port e network destinate a ospitare risorse di tipo QOS
sudo sshpass -p nextworks scp /home/marco/openstack/python-neutronclient-v2.3.11/neutronclient/v2_0/client.py nextworks@10.0.11.120:/usr/local/lib/python2.7/dist-packages/neutronclient/v2_0
echo "client plug-in client.py sended to 10.0.11.120"


# copio classe astratta metodi in neutron
#sshpass -p nextworks scp /home/marco/Scrivania/openstack/neutron_juno/neutron/neutron_plugin_basev2.py nextworks@10.0.11.120:/opt/stack/neutron/neutron/
#echo "abstract class neutron_plugin_basev2.py sended to 10.0.11.120"

# classe che implementa i metodi astratti di neutron
#sshpass -p nextworks scp /home/marco/Scrivania/openstack/neutron_juno/neutron/db/db_base_plugin_v2.py nextworks@10.0.11.120:/opt/stack/neutron/neutron/db/
#echo "concrete class db_base_plugin_v2.py sended to 10.0.11.120"

# invio template di test allocamento risorsa stand-alone
#sshpass -p nextworks scp /home/marco/openstack/heat_templates/qos_easy_test_stand-alone.yaml nextworks@10.0.11.120:/home/nextworks/openstack/heat_templates
#echo "qos_easy_test_stand-alone.yaml sended to 10.0.11.120"

# invio cartella template
sshpass -p nextworks scp -r /home/marco/openstack/heat_templates/ nextworks@10.0.11.120:/home/nextworks/openstack/
echo "~/openstack/heat_templates/ sended to 10.0.11.120:/home/nextworks/openstack/"
