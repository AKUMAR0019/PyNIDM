import rdflib as rdf
import os, sys

#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from nidm.core import Constants
from nidm.experiment import *
from prov.model import *


class Session(ProvActivity,Core):
    """Class for NIDM-Experimenent Session-Level Objects.

    Default constructor uses empty graph with namespaces added from NIDM/Scripts/Constants.py.
    Additional alternate constructors for user-supplied graphs and default namespaces (i.e. from Constants.py)
    and user-supplied graph and namespaces

    @author: David Keator <dbkeator@uci.edu>
    @copyright: University of California, Irvine 2017

    """
    #constructor
    def __init__(self, project,attributes=None):
        """
        Default contructor, creates a session activity and links to project object

        :param project: a project object
        :return: none

        """
        #execute default parent class constructor
        super(Session,self).__init__(project.graph, QualifiedName(Namespace("nidm",Constants.NIDM),self.getUUID()),attributes)
        project.graph._add_record(self)

        self.add_attributes({PROV_TYPE: Constants.NIDM_SESSION})
        self.graph = project.graph

    def __str__(self):
        return "NIDM-Experiment Session Class"

