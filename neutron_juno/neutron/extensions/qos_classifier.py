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

from neutron.api import extensions
from neutron.common import exceptions as qexception
from neutron.openstack.common import log as logging
from neutron.api.v2 import attributes as attr
from neutron.api.v2 import resource_helper


LOG = logging.getLogger(__name__)


class QosClassifierNotFound(qexception.NotFound):
    message = _("qos_classifier %(id)s not found")


RESOURCE_ATTRIBUTE_MAP_QOS_CLASSIFIER = {
    'qos_classifiers': {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True, 'primary_key': True},

        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:uuid': None},
                      'required_by_policy': True, 'is_visible': True},

        'type': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': None},
                 'is_visible': True, 'default': ''},

        'policy': {'allow_post': True, 'allow_put': True,
                   'validate': {'type:string': None},
                   'is_visible': True, 'default': ''}
    }
}


class Qos_classifier(extensions.ExtensionDescriptor):

    @classmethod
    def get_name(cls):
        return "qos_classifier service"

    @classmethod
    def get_alias(cls):
        return "qos_classifier"

    @classmethod
    def get_description(cls):
        return "Extension for Quality Of Service Classifiers"

    @classmethod
    def get_namespace(cls):
        return "http://wiki.openstack.org/Neutron/QosClassifiers/API_1.0"

    @classmethod
    def get_updated(cls):
        return "2015-07-17T90:00:00-00:00"

    def get_extended_resources(self, version):
        return RESOURCE_ATTRIBUTE_MAP_QOS_CLASSIFIER if version == "2.0" else {}

    @classmethod
    def get_resources(cls):
        plural_mappings = resource_helper.build_plural_mappings(
            {}, RESOURCE_ATTRIBUTE_MAP_QOS_CLASSIFIER)
        attr.PLURALS.update(plural_mappings)
        return resource_helper.build_resource_info(plural_mappings,
                                                   RESOURCE_ATTRIBUTE_MAP_QOS_CLASSIFIER,
                                                   None)

    def update_attributes_map(self, attributes):
        super(QosClassifiers, self).update_attributes_map(
            attributes, extension_attrs_map=RESOURCE_ATTRIBUTE_MAP_QOS_CLASSIFIER)
