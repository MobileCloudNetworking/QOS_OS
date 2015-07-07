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
    classifier_type = enum('destinationIf', 'L3_protocol')
    
    # qos_classifier policy constants
    classifier_policy = enum('udp', 'tcp')
    
    def handle_create(self):
        print "willaccio"
        logging.basicConfig(filename='qos_classifier.log',level=logging.DEBUG)
        try:
            # check if type is an interface and the policy is a port (no otherwise)
            if self.properties['type'] == classifier_type['destinationIf'] and isinstance(self.properties['policy'], Port) == false:
                logger.debug('a qos classifier with type destinationIf needs a port for policy')
        except Exception as ex:
            raise
        try:
            # check if type is an L3 protocol and the policy an avalaible transport protocol (no otherwise)
            print 'willy!'
            if self.properties['type'] == classifier_type['L3_protocol'] and check_type(self) != 0:
                logger.debug('a qos classifier with type L3_protocol needs an avalaible transport protocol for policy')
        except Exception as ex:
            raise
        return;
            
    def check_create_complete(self,token):
        pass;

    def check_delete_complete(self, token):
        pass;
        
    # check if the type is correct
    def check_type(self):
        for x in classifier_type:
            if self.properties['type'] == x:
                return 0;
        return -1;
        
    # check if the policy is correct
    def check_policy(self):
        for x in classifier_policy:
            if self.properties['policy'] == x:
                return 0;
        return -1;

# map the class to a resource name
def resource_mapping():
    return {
        'OS::Neutron::qos_classifier': qos_classifier,
    }
