# implements QoS resource in Heat

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

LOG = logging.getLogger(__logFilename__)

# define a set of types like enumerates do
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

# log file creator
def createLog(filename):
    logger = logging.getLogger(filename)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger;
    
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
            _('A L3 interface if required.'),
            default='',
            required=False,
            update_allowed=True,
        ),
    }
    
    # qos_param types constants
    param_type = enum('Rate-limit', 'DSCP', 'Minimum-Reserved-Bandwidth', 'Delay', 'Jitter')
    
    def handle_create(self):
        logging = createLog('qos_param.log')
        # checkin' type
        try:
            if check_type(self) == -1:
                logging.debug('qos_param type unknow, creation failed')
        except Exception as ex:
            raise
        # dont't need to check the value for the integer 'Threshold'
        try:
            if self.properties['classifier'] != "":
                if isinstance(self.properties['classifier'], qos_classifier) == false:
                    logging.debug('qos param classifier type wrong, creation failed')
        except Exception as ex:
            raise            

    def check_create_complete(self,token):
        pass;

    def handle_delete(self):
        # delete resource from Neutron
        #client = self.neutron()
        #try:
            #client.delete_qos_param(self.resource_id)
        #except Exception as ex:
            #logging.debug('can\'t delete resource ' + self. properties['name'])
            #self.client_plugin().ignore_not_found(ex)
        #else:
            #return self._delete_task();
        #return;
        pass;
    
    def check_delete_complete(self, token):
        pass;
    
    # check if the type of the resources is correct
    def check_type(self):
        for x in param_type:
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
            properties.Schema.STRING,
            _('Threshold not to exceeded for the selected type.'),
            required=True,
            update_allowed=True,
        ),
    }
    
    # qos_classifier types constants
    classifierType = enum('destinationIf', 'L3_protocol')
    
    # qos_classifier policy constants
    classifierPolicy = enum('UDP', 'TCP')
    
    def handle_create(self):
        logging.warning('FUCK')
        sys.stdout.write("FUCK")
        # check correct syntax
        logger = createLog("qos_classifier.log")
        # check if type is an interface and the policy is a port (no otherwise)
        if self.properties['type'] == classifier_type['destinationIf'] and isinstance(self.properties['policy'], Port) != 0:
            LOG.error('a qos classifier with type destinationIf needs a port for policy')
            raise exception.InvalidTemplateAttribute("qos_classifier policy")
        # check if type is an L3 protocol and the policy an avalaible transport protocol (no otherwise)
        if self.properties['type'] == classifier_type['L3_protocol'] and check_type(self) != 0:
            LOG.error('a qos classifier with type L3_protocol needs an avalaible transport protocol for policy')
            raise exception.InvalidTemplateAttribute("qos_classifier policy")
        # !!! TO IMPLEMENTS ON NEUTRON SIDE !!!
        #props = self.prepare_properties(
            #self.properties,
            #self.physical_resource_name())
        #classifier = self.neutron().create_qos_classifier({'qos_classifier': props})[
            #'qos_classifier']
        #self.resource_id_set(classifier['id'])
        pass;
            
    def handle_delete(self):
        # !!! TO IMPLEMENTS ON NEUTRON SIDE !!!
        #client = self.neutron()
        #try:
            #client.delete_qos_classifier(self.resource_id)
        #except Exception as ex:
            #self.client_plugin().ignore_not_found(ex)
        #else:
            #return self._delete_task()
        pass;

    # --- AUXILIARY FUNCTIONS --- #

    # check if the type is correct 
    def check_type(self):
        for x in classifierType:
            if self.properties['type'] == x:
                return 0;
        return -1;
        
    # check if the policy is correct
    def check_policy(self):
        for x in classifierPolicy:
            if self.properties['policy'] == x:
                return 0;
        return -1;

# map the class to a resource name
def resource_mapping():
    return {
        'OS::Neutron::qos_classifier': qos_classifier,
    }
