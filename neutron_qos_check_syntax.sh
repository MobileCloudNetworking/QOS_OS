#!/bin/bash

# check correttezza sintax risorsa
if python -m py_compile /home/marco/Scrivania/neutron_juno/neutron/db/qos_db.py; then
	echo "qos_db.py correct syntax"
else exit 1
fi

#!/bin/bash

# check correttezza sintax risorsa
if python -m py_compile /home/marco/Scrivania/neutron_juno/neutron/extensions/qos.py; then
	echo "extension qos.py correct syntax"
else exit 1
fi
