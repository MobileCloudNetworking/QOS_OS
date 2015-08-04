# utils.sh - Devstack extras script

git_clone_openstack_qos() {
    git clone --single-branch -b mcn_qos ssh://robertom@10.0.2.10/pub/scm/git/openstack openstack_qos
}

git_update_openstack_qos() {
    cd openstack_qos
    git pull
    cd - >/dev/null
}
