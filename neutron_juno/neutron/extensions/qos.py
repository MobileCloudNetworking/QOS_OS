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


# qos Exceptions
class qosInternalError(qexception.NeutronException):
    """Qos exception for all the error types."""
    message = _("%(internal)s: Internal error.")


class qosNotFound(qexception.NotFound):
    message = _("qos %(qos_id)s not found")
    
# qos_param Exceptions
class qos_paramInternalError(qexception.NeutronException):
    """Qos_param exception for all the error types."""
    message = _("%(internal)s: Internal error.")

class qos_paramNotFound(qexception.NotFound):
    message = _("qos_param %(qos_param_id)s not found")
    
# qos_classifier Exceptions
class qos_classifierInternalError(qexception.NeutronException):
    """Qos_classifier exception for all the error types."""
    message = _("%(internal)s: Internal error.")

class qos_classifierNotFound(qexception.NotFound):
    message = _("qos_classifier %(qos_classifier_id)s not found")

# define resource attribute map four every type of resource
RESOURCE_ATTRIBUTE_MAP_QOS = {
    'qos': {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True, 'primary_key': True},

        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:uuid': None},
                      'required_by_policy': True, 'is_visible': True},

        'type': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': None},
                 'is_visible': True, 'default': ''},

        'ingress_id': {'allow_post': True, 'allow_put': True,
                       'validate': {'type:uuid': None},
                       'is_visible': True, 'default': ''},

        'egress_id': {'allow_post': True, 'allow_put': True,
                      'validate': {'type:uuid': None},
                      'is_visible': True, 'default': ''},

        'net_id': {'allow_post': True, 'allow_put': False,
                   'validate': {'type:uuid': None},
                   'required_by_policy': True, 'is_visible': True},

        'qos_parameters': {'allow_post': True, 'allow_put': True,
                           'validate': {'type:string': None},
                           'is_visible': True, 'default': ''}
    }
}
    
RESOURCE_ATTRIBUTE_MAP_QOS_PARAM = {
    'qos_param': {
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
                   'is_visible': True, 'default': ''},

        'qos_classifiers': {'allow_post': True, 'allow_put': True,
                   'validate': {'type:string': None},
                   'is_visible': True, 'default': ''}
    }
}

RESOURCE_ATTRIBUTE_MAP_QOS_CLASSIFIER = {
    'qos_classifier': {
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

class qos(extensions.ExtensionDescriptor):

    @classmethod
    def get_name(cls):
        return "qos service"

    @classmethod
    def get_alias(cls):
        return "qos"

    @classmethod
    def get_description(cls):
        return "Extension for Quality Of Service"

    @classmethod
    def get_namespace(cls):
        return "http://wiki.openstack.org/Neutron/qos/API_1.0"

    @classmethod
    def get_updated(cls):
        return "2015-07-17T90:00:00-00:00"

    def get_extended_resources(self, version):
        return RESOURCE_ATTRIBUTE_MAP_QOS if version == "2.0" else {}

    @classmethod
    def get_resources(cls):
        plural_mappings = resource_helper.build_plural_mappings(
            {}, RESOURCE_ATTRIBUTE_MAP_QOS)
        attr.PLURALS.update(plural_mappings)
        return resource_helper.build_resource_info(plural_mappings,
                                                   RESOURCE_ATTRIBUTE_MAP_QOS,
                                                   None)

    def update_attributes_map(self, attributes):
        super(qos, self).update_attributes_map(
            attributes, extension_attrs_map=RESOURCE_ATTRIBUTE_MAP_QOS)

class qos_param(extensions.ExtensionDescriptor):

    @classmethod
    def get_name(cls):
        return "qos_param service"

    @classmethod
    def get_alias(cls):
        return "qos_param"

    @classmethod
    def get_description(cls):
        return "Extension for Quality Of Service Parameters"

    @classmethod
    def get_namespace(cls):
        return "http://wiki.openstack.org/Neutron/qos_param/API_1.0"

    @classmethod
    def get_updated(cls):
        return "2015-07-17T90:00:00-00:00"

    def get_extended_resources(self, version):
        return RESOURCE_ATTRIBUTE_MAP_QOS_PARAM if version == "2.0" else {}

    @classmethod
    def get_resources(cls):
        plural_mappings = resource_helper.build_plural_mappings(
            {}, RESOURCE_ATTRIBUTE_MAP_QOS_PARAM)
        attr.PLURALS.update(plural_mappings)
        return resource_helper.build_resource_info(plural_mappings,
                                                   RESOURCE_ATTRIBUTE_MAP_QOS_PARAM,
                                                   None)

    def update_attributes_map(self, attributes):
        super(qos_param, self).update_attributes_map(
            attributes, extension_attrs_map=RESOURCE_ATTRIBUTE_MAP_QOS_PARAM)

class qos_classifier(extensions.ExtensionDescriptor):

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
        return "http://wiki.openstack.org/Neutron/qos/API_1.0"

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
        super(qos, self).update_attributes_map(
            attributes, extension_attrs_map=RESOURCE_ATTRIBUTE_MAP_QOS_CLASSIFIER)
