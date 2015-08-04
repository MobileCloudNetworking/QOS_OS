# heat.sh (extras script) - Customize HEAT

files="heat/engine/resources/neutron/qos.py "


if is_service_enabled heat; then
    cd ${DEST}
    source $TOP_DIR/extras.d/utils.sh

    if [[ "$1" == "stack" && "$2" == "install" ]]; then
        echo "Clone/Update the OPENSTACK-QOS repository"
        if [ ! -d openstack_qos ]; then
            git_clone_openstack_qos
        else
            git_update_openstack_qos
        fi

        echo "Update the HEAT-code using the OPENSTACK-QOS repository"
        for f in ${files}; do
            echo "copy openstack_qos/heat_juno/${f} into heat/${f}"
            cp openstack_qos/heat_juno/${f} heat/${f}
        done
    fi

    cd - >/dev/null
fi
