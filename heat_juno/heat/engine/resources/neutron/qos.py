#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from heat.engine.resources.neutron import neutron
from heat.common.i18n import _
from heat.engine import properties
from heat.engine import constraints
from heat.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class qos(neutron.NeutronResource):
    """
    A resource for creating Qos for neutron
    """
    PROPERTIES = (
        TYPE, INGRESS_ID, EGRESS_ID, NET_ID, QOS_PARAMETERS
    ) = (
        'type', 'ingress_id', 'egress_id', 'network_id', 'qos_parameters'
    )

    properties_schema = {
        TYPE: properties.Schema(
            properties.Schema.STRING,
            _('QoS type.'),
            required=True,
            update_allowed=True,
            constraints=[
                constraints.AllowedValues(['unidir', 'bidir']),
            ]
        ),
        INGRESS_ID: properties.Schema(
            properties.Schema.STRING,
            _('Source interface identifier.'),
            required=True,
            update_allowed=True
        ),
        EGRESS_ID: properties.Schema(
            properties.Schema.STRING,
            _('Destination interface identifier.'),
            required=True,
            update_allowed=True
        ),
        NET_ID: properties.Schema(
            properties.Schema.STRING,
            _('Network identifier.'),
            required=True,
            update_allowed=True
        ),
        QOS_PARAMETERS: properties.Schema(
            properties.Schema.LIST,
            _('At least one qos_param.'),
            required=True
        ),
    }

    def handle_create(self):
        params = "(type %s, inID=%s, outID=%s, netID=%s, qos_params=%s)" %\
            (self.properties[self.TYPE], self.properties[self.INGRESS_ID],
             self.properties[self.EGRESS_ID], self.properties[self.NET_ID],
             self.properties[self.QOS_PARAMETERS])
        LOG.info("qos-handle_create params=%s" % (params,))

        info = {
            'type': self.properties[self.TYPE],
            'ingress_id': self.properties[self.INGRESS_ID],
            'egress_id': self.properties[self.EGRESS_ID],
            'net_id': self.properties[self.NET_ID],
            'qos_params': self.properties[self.QOS_PARAMETERS]
        }

        req = {'qos': info}

        LOG.debug("request=%s" % req)
        resp = self.neutron().create_qos(req)
        LOG.debug("resp=%s" % (resp,))
        self.resource_id_set(resp.get('qos').get('id'))

        LOG.info("QOS successfully created: rID=%s" % (self.resource_id,))

    def handle_delete(self):
        LOG.info("qos-handle_delete rID=%s" % (self.resource_id,))

        if self.resource_id is not None:
            try:
                self.neutron().delete_qos(self.resource_id)

            except Exception as e:
                LOG.error("QOS exception: %s" % (e,))
                self.client_plugin('neutron').ignore_not_found(e)


class qos_param(neutron.NeutronResource):
    """
    A resource for creating Qos-Param for neutron
    """
    PROPERTIES = (
        TYPE, POLICY, QOS_CLASSIFIERS,
    ) = (
        'type', 'policy', 'qos_classifiers'
    )

    properties_schema = {
        TYPE: properties.Schema(
            properties.Schema.STRING,
            _('Type of parameter to monitor.'),
            required=True,
            update_allowed=True,
            constraints=[
                constraints.AllowedValues(['rate-limit', 'dscp',
                                           'minimum-reserved-bandwidth',
                                           'delay', 'jitter']),
            ]
        ),
        POLICY: properties.Schema(
            properties.Schema.STRING,
            _('Threshold not to exceeded for the selected type.'),
            required=True,
            update_allowed=True,
        ),
        QOS_CLASSIFIERS: properties.Schema(
            properties.Schema.LIST,
            _('Qos_classifiers if required.'),
            default=[],
            required=False,
            update_allowed=True,
        ),
    }

    def handle_create(self):
        params = "(type %s, policy=%s, qos_classifier=%s)" %\
            (self.properties[self.TYPE], self.properties[self.POLICY],
             self.properties[self.QOS_CLASSIFIERS])
        LOG.info("qos-param-handle_create params=%s" % (params,))

        info = {
            'type': self.properties[self.TYPE],
            'policy': self.properties[self.POLICY],
            'qos_classifiers': self.properties[self.QOS_CLASSIFIERS]
        }
        req = {'qos_param': info}

        LOG.debug("request=%s" % req)
        resp = self.neutron().create_qos_param(req)
        LOG.debug("resp=%s" % (resp,))
        self.resource_id_set(resp.get('qos_param').get('id'))

        LOG.info("QOS-PARAM successfully created: rID=%s" %
                 (self.resource_id,))

    def handle_delete(self):
        LOG.info("qos-param-handle_delete rID=%s" % (self.resource_id,))

        if self.resource_id is not None:
            try:
                self.neutron().delete_qos_param(self.resource_id)

            except Exception as e:
                LOG.error("QOS-PARAM exception: %s" % (e,))
                self.client_plugin('neutron').ignore_not_found(e)


class qos_classifier(neutron.NeutronResource):
    """
    A resource for creating Qos Classifier for neutron
    """
    PROPERTIES = (
        TYPE, POLICY,
    ) = (
        'type', 'policy',
    )

    properties_schema = {
        TYPE: properties.Schema(
            properties.Schema.STRING,
            _('Type of interface to monitor.'),
            required=True,
            update_allowed=True,
            constraints=[
                constraints.AllowedValues(['l4-protocol']),
            ]
        ),
        POLICY: properties.Schema(
            properties.Schema.STRING,
            _('a level 4 protocol if type is l4_protocol'),
            required=True,
            update_allowed=True,
            constraints=[
                constraints.AllowedValues(['udp', 'tcp']),
            ]
        ),
    }

    def handle_create(self):
        params = "(type %s, policy=%s)" %\
            (self.properties[self.TYPE], self.properties[self.POLICY],)
        LOG.info("qos-classifier-handle_create params=%s" % (params,))

        info = {'type': self.properties[self.TYPE],
                'policy': self.properties[self.POLICY]}
        req = {'qos_classifier': info}

        LOG.debug("request=%s" % req)
        resp = self.neutron().create_qos_classifier(req)
        LOG.debug("resp=%s" % (resp,))
        self.resource_id_set(resp.get('qos_classifier').get('id'))

        LOG.info("QOS-CLASSIFIER successfully created: rID=%s" %
                 (self.resource_id,))

    def handle_delete(self):
        LOG.info("qos-classifier-handle_delete rID=%s" % (self.resource_id,))

        if self.resource_id is not None:
            try:
                self.neutron().delete_qos_classifier(self.resource_id)

            except Exception as e:
                LOG.error("QOS-CLASSIFIER exception: %s" % (e,))
                self.client_plugin('neutron').ignore_not_found(e)


def resource_mapping():
    return {'OS::Neutron::qos': qos,
            'OS::Neutron::qos_param': qos_param,
            'OS::Neutron::qos_classifier': qos_classifier, }
