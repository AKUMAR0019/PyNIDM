import prov.model as pm

from ..core import Constants

from ..experiment.Core import Core
from ..experiment.Core import getUUID

class ProcessSpecification(pm.ProvEntity, Core):
    """Class for NIDM-Workflow Process Objects.

    Default constructor uses empty graph with namespaces added from NIDM/Scripts/Constants.py.
    Additional alternate constructors for user-supplied graphs and default namespaces (i.e. from Constants.py)
    and user-supplied graph and namespaces

    """
    def __init__(self,parentDoc=None, attributes=None):
        """
        Default contructor, creates document and adds Process activity to graph with optional attributes
        
        :param parentDoc: optional ProvDocument
        :param attributes: optional dictionary of attributes to add
    
        """

        #set graph document
        if (parentDoc):
            self.graph = parentDoc
        else:
            self.graph = Constants.p_graph

       # A Process Specification is a Prov Plan
        if not attributes:
            attributes = {}
        attributes.update(**{pm.PROV_TYPE: pm.PROV_ATTR_PLAN})
            
         #execute default parent class constructor
        super(ProcessSpecification,self).__init__(self.graph, pm.QualifiedName(pm.Namespace("prov",Constants.PROV),getUUID()),attributes)
        self.graph._add_record(self)
