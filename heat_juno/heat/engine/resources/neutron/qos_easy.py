# implements QoS resource in Heat

__author__ = "Marco Del Seppia"
__version__ = "0.1"
__maintainer__ = "Marco Del Seppia"
__email__ = "m.delseppia@nextworks.it"
__status__ = "Developing"

import random
import string
# log class
import logging

from heat.engine.resources.neutron import neutron
from heat.common import exception
from heat.common.i18n import _
from heat.engine import attributes
from heat.engine import constraints
from heat.engine import properties
from heat.engine import resource
from heat.engine import support
from enum import Enum

class qos(neutron.NeutronResource):
	
    # define the settings the template author can manipulate when including that resource in a template
    # Some examples would be:
    # Which flavor and image to use for a Nova server
    # The port to listen to on Neutron LBaaS nodes	
    # The size of a Cinder volume

    PROPERTIES = (
        NAME, QOS_PARAMETER
    ) = (
        'name','qos_parameter',
    )
    
    properties_schema = {
        NAME: properties.Schema(
            properties.Schema.STRING,
            _('A string specifying a symbolic name for the resource, which is required to be unique.'),
            required=True,
            update_allowed=True,
        ),
        QOS_PARAMETER: properties.Schema(
            # let to pass one or more qos_param resource
            properties.Schema.LIST,
            _('One or more parametric resource to be rated to enhance the qos.'),
            default=[],
            required=True,
            update_allowed=True,
        ),
    }
    
    # describe runtime state data of the physical resource that the plug-in can expose to other resources in a Stack.
    # Generally, these aren t available until the physical resource has been created and is in a usable state.
    # Some examples would be:
    # The host id of a Nova server
    # The status of a Neutron network
    # The creation time of a Cinder volume
    # ---- HELPFUL FOR THE OUTPUTS: ---- 
    
    #ATTRIBUTES = (
        #PORT_ID,
    #) = (
        #"port_id",
    #)
    
    #attributes_schema = {
        #PORT_ID: attributes.Schema(
        #_("Resource to be ")
        #),
    #}
    
    def handle_create(self):
        #logging.basicConfig(filename='qos_da_fuck.log', filemode='w',level=logging.DEBUG)
        logger = logging.getLogger('simple_example')
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        logger.addHandler(ch)
        # empty list
        logger.debug('Checking qos_parameter parameter')
        try:
            if self.properties['qos_parameter'] == []:
                logger.debug('qos parameter list empty, creation failed')
        except Exception as ex:
            raise
        try:
        # check properties resources type
            for x in self.properties['qos_parameter']:
                if isinstance(x, qos_param) == false:
                    print('qos parameter list must have qos-parameter types, creation failed')
        except Exception as ex:
            raise

    def check_create_complete(self, token):
        return;

    def handle_delete(self):
        # delete resource from Neutron
        client = self.neutron()
        try:
            c = 6
            #client.delete_qos(self.resource_id)
        except Exception as ex:
            logging.debug('can\'t delete resource ' + self. properties['name'])
            self.client_plugin().ignore_not_found(ex)
        else:
            return self._delete_task();
    
    def check_delete_complete(self, token):
        return;
    
class qos_param(neutron.NeutronResource): 
    
    PROPERTIES = (
        NAME, TYPE, POLICY, CLASSIFIER,
    ) = (
        'name','type','policy','classifier'
    )
    
    properties_schema = {
        NAME: properties.Schema(
            properties.Schema.STRING,
            _('A string specifying a symbolic name for the resource, which is required to be unique.'),
            required=True,
            update_allowed=True,
        ),
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
        CLASSIFIER: properties.Schema(
            properties.Schema.STRING,
            _('Threshold not to exceeded for the selected type.'),
            required=True,
            update_allowed=True,
        ),
    }
    
    # define a set of types for qos_parameter
    def enum(*sequential, **named):
        enums = dict(zip(sequential, range(len(sequential))), **named)
        return type('Enum', (), enums)
    
    # types constants
    Types = enum('Rate-limit', 'DSCP', 'Minimum-Reserved-Bandwidth', 'Delay', 'Jitter')
    
    def handle_create(self):
        logging.basicConfig(filename='qos.log',level=logging.DEBUG)
        # checkin' type
        if check_type(self) == -1:
            logging.debug('qos_param type unknow, creation failed')
            return;
        # dont't need to check the value for the integer 'Threshold'
        if isinstance(self.properties['classifier'], qos_classifier) == false:
            logging.debug('qos parame classifier type wrong, creation failed')
            return;

    def check_create_complete(self,token):
        return;

    def handle_delete(self):
        return;
    
    def check_delete_complete(self, token):
        # delete resource from Neutron
        client = self.neutron()
        try:
            c = 6
            #client.delete_qos_param(self.resource_id)
        except Exception as ex:
            logging.debug('can\'t delete resource ' + self. properties['name'])
            self.client_plugin().ignore_not_found(ex)
        else:
            return self._delete_task();
        return;
    
    # check if the type of the resources is correct
    def check_type(self):
        for x in Types:
            if self.properties['type'] == x:
                return 0;
        return -1;
      
class qos_classifier(neutron.NeutronResource):	
    
    PROPERTIES = (
        NAME, TYPE, POLICY,
    ) = (
        'name','type','policy',
    )
    
    properties_schema = {
        NAME: properties.Schema(
            properties.Schema.STRING,
            _('A string specifying a symbolic name for the resource, which is required to be unique.'),
            required=True,
            update_allowed=True,
        ),
        TYPE: properties.Schema(
            properties.Schema.STRING,
            _('Type of interface to monitor.'),
            required=True,
            update_allowed=True,
        ),
        POLICY: properties.Schema(
            properties.Schema.INTEGER,
            _('Threshold not to exceeded for the selected type.'),
            required=True,
            update_allowed=True,
        ),
    }    
    
    def handle_create(self):
        return;

    def check_create_complete(self,token):
        return;

    def handle_delete(self):
        # delete resource from Neutron
        client = self.neutron()
        try:
            c = 6
            #client.delete_qos_classifier(self.resource_id)
        except Exception as ex:
            logging.debug('can\'t delete resource ' + self. properties['name'])
            self.client_plugin().ignore_not_found(ex)
        else:
            return self._delete_task();
    
    def check_delete_complete(self, token):
        return;

# map the class to a resource name
def resource_mapping():
    return {
        'OS::Neutron::qos': qos,
        'OS::Neutron::qos_param': qos_param,
        'OS::Neutron::qos_classifier': qos_classifier,
    }
