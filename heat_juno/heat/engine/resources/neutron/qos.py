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

# define a type like enumerates (non avalaible in Python 2.7)
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
    
# communication client 
default_client_name = 'neutron'

# qos_param types constants
parameterType = enum('Rate-limit', 'DSCP', 'Minimum-Reserved-Bandwidth', 'Delay', 'Jitter')
    
# qos_classifier types constants
classifierType = enum('destinationIf', 'L3_protocol')
    
# qos_classifier policy constants
classifierPolicy = enum('UDP', 'TCP')

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
            # let give one or more qos_param resource
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
        logger = createLog('qos.log')
        logger.debug('Checking qos_parameter parameter')
        # empty list
        try:
            if self.properties['qos_parameter'] == []:
                logger.debug('qos parameter list empty, creation failed')
        except Exception as ex:
            raise
        # check properties resources type
        try:
            for x in self.properties['qos_parameter']:
                if isinstance(x, qos_param) == false:
                    print('qos parameter list must have qos-parameter types, creation failed')
        except Exception as ex:
            raise

    def check_create_complete(self, token):
        pass;

    def handle_delete(self):
        # delete resource from Neutron
        #client = self.neutron()
        #try:
            #client.delete_qos(self.resource_id)
        #except Exception as ex:
            #logging.debug('can\'t delete resource ' + self. properties['name'])
            #self.client_plugin().ignore_not_found(ex)
        #else:
            #return self._delete_task();
        pass;
    
    def check_delete_complete(self, token):
        pass;
    
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
    """
    A resource for creating Qos Classifier
    """

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
            _('ID of an existing port to associate with this classifier if type is an interface or a'
              ' level 3 protocol.'),
            required=True,
            update_allowed=True,
        ),
    }

    def validate(self):
        '''
        Validate any of the provided params
        '''
        # check if type is an interface and the policy is a port (no otherwise)
        if self.properties[self.TYPE] == classifierType.destinationIf and isinstance(self.properties[self.POLICY], Port) != 0:
            LOG.error('a qos classifier with type destinationIf needs a port for policy')
            raise exception.InvalidTemplateAttribute("qos_classifier policy")
        # check if type is an L3 protocol and the policy an avalaible transport protocol (no otherwise)
        if self.properties[self.TYPE] == classifierType.L3_protocol and check_type(self) != 0:
            LOG.error('a qos classifier with type L3_protocol needs an avalaible transport protocol for policy')
            raise exception.InvalidTemplateAttribute("qos_classifier policy")
        # set classifier mode
        classifier_mode = self.properties[self.POLICY]

    def handle_create(self):
        '''
        Create a new qos_classifier resource
        '''
        # resource infos
        msg = "name=%s, type %s, policy=%s," %\
            (self.properties[self.NAME], self.properties[self.TYPE], self.properties[self.POLICY])
        LOG.info("qos_classifier creating: %s" % (msg,))
        
        # !!! NEUTRON !!! #
        # get port id if type is an interface
        #if classifier_mode == 'destinationIf':
            #port = self.neutron().show_port(self.properties[self.POLICY])
            #LOG.debug("Port=%s" % port)
            
        # prepare message to be sent to neutron
        neutron_msg = {'name': self.properties[self.NAME],
                       'type': self.properties[self.TYPE],
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
                #LOG.error("qos_classifier exceprion: %s" % (ex,))
                #self.client_plugin('neutron').ignore_not_found(ex)
            #else:
                #return self._delete_task()
        pass;

    # --- AUXILIARY FUNCTIONS --- #

    # check if the type is correct 
    def check_type(self):
        for x in classifierType:
            if self.properties[self.TYPE] == x:
                return 0;
        return -1;
        
    # check if the policy is correct
    def check_policy(self):
        for x in classifierPolicy:
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
