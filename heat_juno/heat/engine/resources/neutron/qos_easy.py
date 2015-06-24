# implements QoS resource for Heat

__author__ = "Marco Del Seppia"
__version__ = "0.1"
__maintainer__ = "Marco Del Seppia"
__email__ = "m.delseppia@nextworks.it"
__status__ = "Developing"

import random
import string

from heat.engine.resources.neutron import neutron
from heat.common import exception
from heat.common.i18n import _
from heat.engine import attributes
from heat.engine import constraints
from heat.engine import properties
from heat.engine import resource
from heat.engine import support


class qos(resource.Resource):
	
	# define the settings the template author can manipulate when including that resource in a template
	# Some examples would be:
	# Which flavor and image to use for a Nova server
	# The port to listen to on Neutron LBaaS nodes	
	# The size of a Cinder volume
	
	PROPERTIES = (
        NAME,
    ) = (
        'name',
    )
    
	properties_schema = {
        NAME: properties.Schema(
            properties.Schema.STRING,
            _('A string specifying a symbolic name for the network, which is '
              'not required to be unique.'),
            required=True,
            update_allowed=True,
        )
	}
	
	# describe runtime state data of the physical resource that the plug-in can expose to other resources in a Stack.
	# Generally, these aren t available until the physical resource has been created and is in a usable state.
	# Some examples would be:
	# The host id of a Nova server
	# The status of a Neutron network
	# The creation time of a Cinder volume
	# ---- HELPFUL FOR THE OUTPUTS: ---- 
		
	#ATTRIBUTES = (
        #NAME_ATTR,
    #) = (
        #"name",
    #)
    
	#attributes_schema = {
        #NAME_ATTR: attributes.Schema(
            #_("Friendly name of the QoS (for multiple instance)")
        #),
    #}  
    
	@classmethod
	def handle_create(self):
			
	def check_create_complete(self, token):
		
	def handle_delete(self):
	
	def check_delete_complete(self, token):
		
		
#class qos_param(resource.NeutronResource): 
		
#class qos_classifier(resource.NeutronResource):	
		
# map the class to a resource name
def resource_mapping():
    return {
        'OS::Neutron::qos': qos,
        #'OS::Neutron::qos_param': qos_param,
        #'OS::Neutron::qos_classifier': qos_classifier,
    }
