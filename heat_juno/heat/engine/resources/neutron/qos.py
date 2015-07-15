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

__author__ = "Marco Del Seppia"
__version__ = "0.1"
__maintainer__ = "Marco Del Seppia"
__email__ = "m.delseppia@nextworks.it"
__status__ = "Developing"
__logFilename__ = "qos.log"

import random
import string
# log class
import logging
# debug purpose
import random

from heat.engine.resources.neutron import neutron
# resources where i can attach the qos_*
from heat.engine.resources.neutron import port
from heat.engine.resources.neutron import net
from heat.common import exception
from heat.common.i18n import _
from heat.engine import attributes
from heat.engine import constraints
from heat.engine import properties
from heat.engine import resource
from heat.engine import support
from enum import Enum
# openstack log
from heat.openstack.common import log as logging

LOG = logging.getLogger(__name__)

# communication client 
#default_client_name = 'neutron'

class qos(neutron.NeutronResource):
    """
    A resource for creating Qos for neutron
    """
    PROPERTIES = (
        QOS_PARAMETER
    ) = (
        'qos_parameter',
    )
    
    properties_schema = {
        QOS_PARAMETER: properties.Schema(
            properties.Schema.LIST,
            _('One or more parametric resource to be rated to enhance the qos parameters.'),
            default=[],
            required=True,
            update_allowed=True,
        ),
    }
    
    def validate(self):
        '''
        Validate any of the provided qos_params
        '''
        # check parameter empty list
        if self.properties[self.QOS_PARAMETER] == []:
            LOG.debug('qos has qos_parameter list empty, creation failed')
            raise exception.InvalidTemplateAttribute(resource=self.QOS_PARAMETER, key='qos_parameter, creation failed')
        # check properties resources type
        for x in self.properties[self.QOS_PARAMETER]:
            if isinstance(x, qos_param) == false:
                LOG.debug('qos has qos_parameter list with no qos_parameter types, creation failed')
                raise exception.InvalidTemplateAttribute(resource=self.QOS_PARAMETER, key='qos_parameter, creation failed')
    def handle_create(self):
        '''
        Create a new qos resource
        '''
        # resource infos
        msg = "qos_parameter %s" %\
            (self.properties[self.QOS_PARAMETER])
        LOG.info("qos creating: %s" % (msg,))
        
        # !!! NEUTRON !!! #
        # get port id if type is an interface
        #if classifier_mode == 'destinationIf':
            #port = self.neutron().show_port(self.properties[self.POLICY])
            #LOG.debug("Port=%s" % port)
            
        # prepare message to be sent to neutron
        neutron_msg = {'qos_parameter': self.properties[self.QOS_PARAMETER]}
        
        #resp = self.neutron().create_qos({'qos': neutron_msg})
        LOG.info("Neutron message=%s" % (neutron_msg,))
        #self.resource_id_set(resp.get('qos').get('id'))
        LOG.info("qos_classifier succesfully created: resource ID=%s" %
                    (self.resource_id,))
        self.resource_id_set(random.randint(0,10000000000))


    def handle_delete(self):
        '''
        Delete an existing qos resource
        '''
        # delete resource from Neutron
        #client = self.neutron()
        #try:
            #client.delete_qos(self.resource_id)
        #except Exception as ex:
            #LOG.error("qos exception: %s" % (ex,))
            #self.client_plugin().ignore_not_found(ex)
        #else:
            #return self._delete_task();
        pass;

class qos_param(neutron.NeutronResource): 
    """
    A resource for creating Qos Parameters
    """
    
    # param types constants
    TYPES = (
        RATE_LIMIT, DSCP, MINIMUM_RESERVED_BAND, DELAY, JITTER,
    ) = ( 
        'Rate-limit', 'DSCP', 'Minimum-Reserved-Bandwidth', 'Delay', 'Jitter',
    )
    
    PROPERTIES = (
        TYPE, POLICY, QOS_CLASSIFIER,
    ) = (
        'type','policy','qos_classifier'
    )
    
    properties_schema = {
        TYPE: properties.Schema(
            properties.Schema.STRING,
            _('Type of parameter to monitor.'),
            required=True,
            update_allowed=True,
        ),
        POLICY: properties.Schema(
            properties.Schema.INTEGER,
            _('Threshold not to exceeded for the selected type.'),
            required=True,
            update_allowed=True,
        ),  
        QOS_CLASSIFIER: properties.Schema(
            properties.Schema.STRING,
            _('An qos_classifier if required.'),
            default='',
            required=False,
            update_allowed=True,
        ),
    }
    
    def validate(self):
        '''
        Validate any of the provided params
        '''
        LOG.info("KILL WILL")
        # check if type is an interface and the policy is a port (no otherwise)
        if self.param_check_type() != 0:
            LOG.error('qos param type unknown, creation failed')
            raise exception.InvalidTemplateAttribute(resource=self.TYPE, key='policy, creation failed')
        LOG.info("DJANGO")
        # check if type is an L3 protocol and the policy an avalaible transport protocol (no otherwise)
        if hasattr(self, self.QOS_CLASSIFIER) and isinstance(self.properties[self.QOS_CLASSIFIER], qos_classifier) != 0:
            LOG.error('the classifier passed is of a type unknown, creation failed')
            raise exception.InvalidTemplateAttribute(resource=self.POLICY, key='policy, creation failed')
        LOG.info("CURIOSITY")
    
    def handle_create(self):
        '''
        Create a new qos_param resource
        '''
        # resource infos CHECK IF HAS QOAS_CLASSIFIER!!!!!!!!!!!!!!!!!!!!!!
        LOG.info("MARS")
        msg = "type %s, policy=%s," %\
            (self.properties[self.TYPE], self.properties[self.POLICY])
        LOG.info("qos_param creating: %s" % (msg,))
        
        # !!! NEUTRON !!! #
        # get port id if type is an interface
        #if classifier_mode == 'destinationIf':
            #port = self.neutron().show_port(self.properties[self.POLICY])
            #LOG.debug("Port=%s" % port)
            
        # prepare message to be sent to neutron
        neutron_msg = {'type': self.properties[self.TYPE],
                       'policy': self.properties[self.POLICY]}
        
        #resp = self.neutron().create_qos_param({'qos_param': neutron_msg})
        LOG.info("Neutron message=%s" % (neutron_msg,))
        #self.resource_id_set(resp.get('qos_param').get('id'))
        LOG.info("qos_param succesfully created: resource ID=%s" %
                    (self.resource_id,))
        self.resource_id_set(random.randint(0,10000000000))
        LOG.info("JUPITER")

    def handle_delete(self):
        '''
        Delete an existing qos_parameter resource
        '''
        LOG.info("qos_param deleting: resource ID=%s" % (self.resource_id,))
        #client = self.neutron()
        #try:
            #client.delete_qos_param(self.resource_id)
        #except Exception as ex:
            #LOG.error("qos_param exception: %s" % (ex,))
            #self.client_plugin().ignore_not_found(ex)
        #else:
            #return self._delete_task();

    # --- AUXILIARY FUNCTIONS --- #

    # check if the type of the resources is correct
    def param_check_type(self):
        for x in qos_param.TYPES:
            if self.properties[self.TYPE] == x:
                return 0;
        return -1;

class qos_classifier(neutron.NeutronResource):	
    """
    A resource for creating Qos Classifier
    """
    # classifier types constants
    TYPES = (
        L3_PROTOCOL, DESTINATION_IF, 
    ) = (
        'L3_protocol', 'destinationIf', 
    )
    
    # classifier policies constants
    POLICIES = (
        UDP, TCP,
    ) = (
        "UDP", "TCP",
    )

    PROPERTIES = (
        TYPE, POLICY,
    ) = (
        'type','policy',
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
            _('ID of an existing port to associate with type destinationIf or a'
              ' level 3 protocol if type is L3_protocol.'),
            required=True,
            update_allowed=True,
        ),
    }

    def validate(self):
        '''
        Validate any of the provided params
        '''
        # check if type is an interface and the policy is a port (no otherwise)
        if self.properties[self.TYPE] == qos_classifier.DESTINATION_IF and isinstance(self.properties[self.POLICY], Port) != 0:
            LOG.error('a qos classifier with type destinationIf needs a port for policy, creation failed')
            raise exception.InvalidTemplateAttribute(resource=self.TYPE, key='type, creation failed')
        # check if type is an L3 protocol and the policy an avalaible transport protocol (no otherwise)
        if ((self.properties[self.TYPE] == qos_classifier.L3_PROTOCOL) and (self.classifier_check_policy() != 0)):
            LOG.error('a qos classifier with type L3_protocol needs an avalaible transport protocol for policy, creation failed')
            raise exception.InvalidTemplateAttribute(resource=self.POLICY, key='policy, creation failed')
        else:
            raise exception.InvalidTemplateAttribute(resource=self.TYPE, key='type, creation failed')

    def handle_create(self):
        '''
        Create a new qos_classifier resource
        '''
        #LOG.info("handle_create(self) --- self.properties[self.POLICY] = %s" % (self.properties[self.POLICY],))
        #LOG.info("handle_create(self) --- self.properties[self.Type] = %s" % (self.properties[self.TYPE],))
        # resource infos
        msg = "type %s, policy=%s," %\
            (self.properties[self.TYPE], self.properties[self.POLICY])
        LOG.info("qos_classifier creating: %s" % (msg,))
        
        # !!! NEUTRON !!! #
        # get port id if type is an interface
        #if classifier_mode == 'destinationIf':
            #port = self.neutron().show_port(self.properties[self.POLICY])
            #LOG.debug("Port=%s" % port)
            
        # prepare message to be sent to neutron
        neutron_msg = {'type': self.properties[self.TYPE],
                       'policy': self.properties[self.POLICY]}
        
        #resp = self.neutron().create_qos_classifier({'qos_classifier': neutron_msg})
        LOG.info("Neutron message=%s" % (neutron_msg,))
        #self.resource_id_set(resp.get('qos_classifier').get('id'))
        LOG.info("qos_classifier succesfully created: resource ID=%s" %
                    (self.resource_id,))
        self.resource_id_set(random.randint(0,10000000000))

    def handle_delete(self):
        '''
        Delete an existing qos_classifier resource
        '''
        LOG.info("qos_classifier deleting: resource ID=%s" % (self.resource_id,))
        # !!! NEUTRON !!! #
        #if self.resource_id is not None:
            #try:
                #client.delete_qos_classifier(self.resource_id)
            #except Exception as ex:
                #LOG.error("qos_classifier exception: %s" % (ex,))
                #self.client_plugin('neutron').ignore_not_found(ex)
            #else:
                #return self._delete_task()
        pass;

    # --- AUXILIARY FUNCTIONS --- #

    # check if the type is correct 
    def classifier_check_type(self):
        for x in qos_classifier.TYPES:
            if self.properties[self.TYPE] == x:
				return 0
        return -1
        
    # check if the policy is correct
    def classifier_check_policy(self):
        #LOG.info("classifier_check_policy OUTSIDE --- self.properties[self.POLICY] = %s" % (self.properties[self.POLICY],))
        #LOG.info("ATTRIBUTES.UDP=%s" % (qos_classifier.UDP,))
        for x in qos_classifier.POLICIES:
            if self.properties[self.POLICY] == x:
                return 0;
        return -1;

# map the class to a resource name
def resource_mapping():
    return {
		'OS::Neutron::qos': qos,
        'OS::Neutron::qos_param': qos_param,
        'OS::Neutron::qos_classifier': qos_classifier,
    }
