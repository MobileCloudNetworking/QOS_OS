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
from heat.common import exception
from heat.common.i18n import _
from heat.engine import properties
from heat.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class qos(neutron.NeutronResource):
    """
    A resource for creating Qos for neutron
    """
    PROPERTIES = (
        QOS_PARAMETERS
    ) = (
        'qos_parameters'
    )

    properties_schema = {
        QOS_PARAMETERS: properties.Schema(
            properties.Schema.LIST,
            _('At least one qos_param..'),
            required=True
        ),
    }

    def handle_create(self):
        LOG.info("qos-handle_create params=%s" %
                 (self.properties[self.QOS_PARAMETERS],))

        msg = {'qos': self.properties[self.QOS_PARAMETERS]}
        resp = self.neutron().create_qos(msg)
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
    TYPES = (
        RATE_LIMIT, DSCP, MINIMUM_RESERVED_BAND, DELAY, JITTER,
    ) = (
        'Rate-limit', 'DSCP', 'Minimum-Reserved-Bandwidth', 'Delay', 'Jitter',
    )

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

    def __param_check_type(self):
        # check if the type of the resources is correct
        for x in qos_param.TYPES:
            if self.properties[self.TYPE] == x:
                return 0
        return -1

    def validate(self):
        '''
        Validate any of the provided params:
        check if type is an interface and the policy is a port (no otherwise)
        '''
        if self.__param_check_type() != 0:
            LOG.error('qos param type unknown, creation failed')
            raise exception.InvalidTemplateAttribute(
                resource=self.TYPE, key='policy, creation failed')

    def handle_create(self):
        params = "(type %s, policy=%s, qos_classifier=%s)" %\
            (self.properties[self.TYPE], self.properties[self.POLICY],
             self.properties[self.QOS_CLASSIFIERS])
        LOG.info("qos-param-handle_create params=%s" % (params,))

        info = {'type': self.properties[self.TYPE],
                'policy': self.properties[self.POLICY],
                'qos_classifiers': self.properties[self.QOS_CLASSIFIERS]}
        msg = {'qos-params': info}
        resp = self.neutron().create_qos_param(msg)
        LOG.debug("resp=%s" % (resp,))
        self.resource_id_set(resp.get('qos-params').get('id'))

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
    TYPES = (
        L3_PROTOCOL, DESTINATION_IF,
    ) = (
        'L3_protocol', 'destinationIf',
    )

    POLICIES = (
        UDP, TCP,
    ) = (
        "UDP", "TCP",
    )

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
        ),
        POLICY: properties.Schema(
            properties.Schema.STRING,
            _('ID of an existing port to associate with type destinationIf or'
              ' a level 3 protocol if type is L3_protocol.'),
            required=True,
            update_allowed=True,
        ),
    }

    # check if the policy is correct
    def __classifier_check_policy(self):
        for x in qos_classifier.POLICIES:
            if self.properties[self.POLICY] == x:
                return 0
        return -1

    def validate(self):
        '''
        Validate any of the provided params
        check if type is an L3 protocol and the policy an avalaible transport
        protocol (no otherwise)
        '''
        cond = (self.properties[self.TYPE] == qos_classifier.L3_PROTOCOL) and\
               (self.__classifier_check_policy() != 0)
        if cond:
            LOG.error('a qos classifier with type L3_protocol needs an\
                      avalaible transport protocol for policy,\
                      creation failed')
            raise exception.InvalidTemplateAttribute(
                resource=self.POLICY, key='policy, creation failed')

    def handle_create(self):
        params = "(type %s, policy=%s)" %\
            (self.properties[self.TYPE], self.properties[self.POLICY],)
        LOG.info("qos-classifier-handle_create params=%s" % (params,))

        info = {'type': self.properties[self.TYPE],
                'policy': self.properties[self.POLICY]}
        msg = {'qos-classifier': info}
        resp = self.neutron().create_qos_classifier(msg)
        LOG.debug("resp=%s" % (resp,))
        self.resource_id_set(resp.get('qos-classifier').get('id'))

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
