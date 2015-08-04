# neutron.sh (extras script) - Customize NEUTRON

pypref="/usr/local/lib/python2.7/dist-packages"
pyncv="python-neutronclient-v2.3.11"

files_neutron="neutron/plugins/ml2/plugin.py "
#files_neutron+="neutron/plugins/ml2/managers.py "
#files_neutron+="neutron/plugins/ml2/driver_api.py "
#files_neutron+="neutron/db/migration/models/frozen.py "

files_neutron_client="neutronclient/v2_0/client.py"


if is_service_enabled neutron; then
    cd ${DEST}
    source $TOP_DIR/extras.d/utils.sh

    if [[ "$1" == "stack" && "$2" == "install" ]]; then
        echo "Clone/Update the OPENSTACK-QOS repository"
        if [ ! -d openstack_qos ]; then
            git_clone_openstack_qos
        else
            git_update_openstack_qos
        fi

        echo "Update the NEUTRON-code using the OPENSTACK-QOS repository"
        for f in ${files_neutron}; do
            echo "copy openstack_qos/neutron_juno/${f} into neutron/${f}"
            cp openstack_qos/neutron_juno/${f} neutron/${f}
        done
    fi
    if [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        for f in ${files_neutron_client}; do
            echo "copy openstack_qos/${pyncv}/${f} ${pypref}/${f}"
            sudo cp openstack_qos/${pyncv}/${f} ${pypref}/${f}
        done
    fi

    cd - >/dev/null
fi
