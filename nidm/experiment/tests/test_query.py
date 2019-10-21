import pytest
from nidm.experiment import Project, Session, AssessmentAcquisition, AssessmentObject, Acquisition, AcquisitionObject, Query
from nidm.core import Constants
from rdflib import Namespace,URIRef
import prov.model as pm
from os import remove
import os
import pprint

from prov.model import ProvDocument, QualifiedName
from prov.model import Namespace as provNamespace
import json
import urllib.request
from pathlib import Path

# when set to true, this will test example NIDM files downloaded from
# the GitHub dbkeator/simple2_NIDM_examples repo
#
# DBK: this is a bit unsafe as the TTL files in the github repo above can change and the UUID will change since they are randomly
# generated at this point.  It's probably more robust to explicitly create these files for the time being and explicitly set the
# UUID in the test file:
# For example:  kwargs={Constants.NIDM_PROJECT_NAME:"FBIRN_PhaseIII",Constants.NIDM_PROJECT_IDENTIFIER:1200,Constants.NIDM_PROJECT_DESCRIPTION:"Test investigation2"}
#               project = Project(uuid="_654321",attributes=kwargs)
USE_GITHUB_DATA = True

def test_GetProjectMetadata():

    kwargs={Constants.NIDM_PROJECT_NAME:"FBIRN_PhaseII",Constants.NIDM_PROJECT_IDENTIFIER:9610,Constants.NIDM_PROJECT_DESCRIPTION:"Test investigation"}
    project = Project(uuid="_123456",attributes=kwargs)


    #save a turtle file
    with open("test.ttl",'w') as f:
        f.write(project.serializeTurtle())

    kwargs={Constants.NIDM_PROJECT_NAME:"FBIRN_PhaseIII",Constants.NIDM_PROJECT_IDENTIFIER:1200,Constants.NIDM_PROJECT_DESCRIPTION:"Test investigation2"}
    project = Project(uuid="_654321",attributes=kwargs)


    #save a turtle file
    with open("test2.ttl",'w') as f:
        f.write(project.serializeTurtle())


    #WIP test = Query.GetProjectMetadata(["test.ttl", "test2.ttl"])

    #assert URIRef(Constants.NIDM + "_654321") in test
    #assert URIRef(Constants.NIDM + "_123456") in test
    #assert URIRef(Constants.NIDM_PROJECT_IDENTIFIER + "1200") in test
    #assert URIRef(Constants.NIDM_PROJECT_IDENTIFIER + "9610") in test
    #assert URIRef((Constants.NIDM_PROJECT_NAME + "FBIRN_PhaseII")) in test
    #assert URIRef((Constants.NIDM_PROJECT_NAME + "FBIRN_PhaseIII")) in test
    #assert URIRef((Constants.NIDM_PROJECT_DESCRIPTION + "Test investigation")) in test
    #assert URIRef((Constants.NIDM_PROJECT_DESCRIPTION + "Test investigation2")) in test

    remove("test2.ttl")


def test_GetProjects():

    kwargs={Constants.NIDM_PROJECT_NAME:"FBIRN_PhaseII",Constants.NIDM_PROJECT_IDENTIFIER:9610,Constants.NIDM_PROJECT_DESCRIPTION:"Test investigation"}
    project = Project(uuid="_123456",attributes=kwargs)


    #save a turtle file
    with open("test.ttl",'w') as f:
        f.write(project.serializeTurtle())

    project_list = Query.GetProjectsUUID(["test.ttl"])

    remove("test.ttl")
    assert URIRef(Constants.NIIRI + "_123456") in project_list

def test_GetParticipantIDs():

    kwargs={Constants.NIDM_PROJECT_NAME:"FBIRN_PhaseII",Constants.NIDM_PROJECT_IDENTIFIER:9610,Constants.NIDM_PROJECT_DESCRIPTION:"Test investigation"}
    project = Project(uuid="_123456",attributes=kwargs)
    session = Session(uuid="_13579",project=project)
    acq = Acquisition(uuid="_15793",session=session)
    acq2 = Acquisition(uuid="_15795",session=session)

    person=acq.add_person(attributes=({Constants.NIDM_SUBJECTID:"9999"}))
    acq.add_qualified_association(person=person,role=Constants.NIDM_PARTICIPANT)

    person2=acq2.add_person(attributes=({Constants.NIDM_SUBJECTID:"8888"}))
    acq2.add_qualified_association(person=person2,role=Constants.NIDM_PARTICIPANT)

    #save a turtle file
    with open("test.ttl",'w') as f:
        f.write(project.serializeTurtle())

    participant_list = Query.GetParticipantIDs(["test.ttl"])

    remove("test.ttl")
    assert (participant_list['ID'].str.contains('9999').any())
    assert (participant_list['ID'].str.contains('8888').any())

def test_GetProjectInstruments():

    kwargs={Constants.NIDM_PROJECT_NAME:"FBIRN_PhaseII",Constants.NIDM_PROJECT_IDENTIFIER:9610,Constants.NIDM_PROJECT_DESCRIPTION:"Test investigation"}
    project = Project(uuid="_123456",attributes=kwargs)

    session = Session(project)
    acq = AssessmentAcquisition(session)

    kwargs={pm.PROV_TYPE:pm.QualifiedName(pm.Namespace("nidm",Constants.NIDM),"NorthAmericanAdultReadingTest")}
    acq_obj = AssessmentObject(acq,attributes=kwargs)

    acq2 = AssessmentAcquisition(session)

    kwargs={pm.PROV_TYPE:pm.QualifiedName(pm.Namespace("nidm",Constants.NIDM),"PositiveAndNegativeSyndromeScale")}
    acq_obj2 = AssessmentObject(acq2,attributes=kwargs)

    #save a turtle file
    with open("test.ttl",'w') as f:
        f.write(project.serializeTurtle())


    assessment_list = Query.GetProjectInstruments(["test.ttl"],"_123456")

    #remove("test.ttl")

    assert URIRef(Constants.NIDM + "NorthAmericanAdultReadingTest") in assessment_list['assessment_type'].to_list()
    assert URIRef(Constants.NIDM + "PositiveAndNegativeSyndromeScale") in assessment_list['assessment_type'].to_list()


'''
The test data file could/should have the following project meta data. Taken from
https://raw.githubusercontent.com/incf-nidash/nidm/master/nidm/nidm-experiment/terms/nidm-experiment.owl
  
  - descrption
  - fileName
  - license
  - source
  - title
  - hadNumericalValue ???
  - BathSolution ???
  - CellType
  - ChannelNumber
  - ElectrodeImpedance
  - GroupLabel
  - HollowElectrodeSolution
  - hadImageContrastType
  - hadImageUsageType
  - NumberOfChannels
  - AppliedFilter
  - SolutionFlowSpeed
  - RecordingLocation
   
Returns the 
  
'''
def saveTestFile(file_name, data):
    project = Project(uuid="_123_" + file_name, attributes=data)

    return saveProject(file_name, project)

def saveProject(file_name, project):
    # save a turtle file
    with open(file_name, 'w') as f:
        f.write(project.serializeTurtle())
    return "nidm:_123_{}".format(file_name)


def makeProjectTestFile(filename):
    DCTYPES = Namespace("http://purl.org/dc/dcmitype/")

    kwargs = {Constants.NIDM_PROJECT_NAME: "FBIRN_PhaseII", # this is the "title"
              Constants.NIDM_PROJECT_IDENTIFIER: 9610,
              Constants.NIDM_PROJECT_DESCRIPTION: "Test investigation",
              Constants.NIDM_FILENAME: "testfile.ttl",
              Constants.NIDM_PROJECT_LICENSE: "MIT Licence",
              Constants.NIDM_PROJECT_SOURCE: "Educational Source",
              Constants.NIDM_HAD_NUMERICAL_VALUE: "numval???",
              Constants.NIDM_BATH_SOLUTION: "bath",
              Constants.NIDM_CELL_TYPE: "ctype",
              Constants.NIDM_CHANNEL_NUMBER: "5",
              Constants.NIDM_ELECTRODE_IMPEDANCE: ".01",
              Constants.NIDM_GROUP_LABEL: "group 123",
              Constants.NIDM_HOLLOW_ELECTRODE_SOLUTION: "water",
              Constants.NIDM_HAD_IMAGE_CONTRACT_TYPE: "off",
              Constants.NIDM_HAD_IMAGE_USAGE_TYPE: "abcd",
              Constants.NIDM_NUBMER_OF_CHANNELS: "11",
              Constants.NIDM_APPLIED_FILTER: "on",
              Constants.NIDM_SOLUTION_FLOW_SPEED: "2.8",
              Constants.NIDM_RECORDING_LOCATION: "lab"
              }
    return saveTestFile(filename, kwargs)

def makeProjectTestFile2(filename):
    DCTYPES = Namespace("http://purl.org/dc/dcmitype/")

    kwargs = {Constants.NIDM_PROJECT_NAME: "TEST B", # this is the "title"
              Constants.NIDM_PROJECT_IDENTIFIER: 1234,
              Constants.NIDM_PROJECT_DESCRIPTION: "More Scans",
              Constants.NIDM_FILENAME: "testfile2.ttl",
              Constants.NIDM_PROJECT_LICENSE: "Creative Commons",
              Constants.NIDM_PROJECT_SOURCE: "Other",
              Constants.NIDM_HAD_NUMERICAL_VALUE: "numval???",
              Constants.NIDM_BATH_SOLUTION: "bath",
              Constants.NIDM_CELL_TYPE: "ctype",
              Constants.NIDM_CHANNEL_NUMBER: "5",
              Constants.NIDM_ELECTRODE_IMPEDANCE: ".01",
              Constants.NIDM_GROUP_LABEL: "group 123",
              Constants.NIDM_HOLLOW_ELECTRODE_SOLUTION: "water",
              Constants.NIDM_HAD_IMAGE_CONTRACT_TYPE: "off",
              Constants.NIDM_HAD_IMAGE_USAGE_TYPE: "abcd",
              Constants.NIDM_NUBMER_OF_CHANNELS: "11",
              Constants.NIDM_APPLIED_FILTER: "on",
              Constants.NIDM_SOLUTION_FLOW_SPEED: "2.8",
              Constants.NIDM_RECORDING_LOCATION: "lab"
              }
    project = Project(uuid="_123_" + filename, attributes=kwargs)
    s1 = Session(project)

    a1 = AssessmentAcquisition(session=s1)
      # = s1.add_acquisition("a1", attributes={"http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#Age" : 22})

    p1 = a1.add_person("p1", attributes={Constants.NIDM_GIVEN_NAME:"George", Constants.NIDM_AGE: 22})
    a1.add_qualified_association(person=p1, role=Constants.NIDM_PARTICIPANT)


    return saveProject(filename, project)


def test_GetProjectsMetadata():

    p1 = makeProjectTestFile("testfile.ttl")
    p2 = makeProjectTestFile2("testfile2.ttl")
    files = ["testfile.ttl", "testfile2.ttl"]


    if USE_GITHUB_DATA and not Path('./cmu_a.nidm.ttl').is_file():
        urllib.request.urlretrieve (
            "https://raw.githubusercontent.com/dbkeator/simple2_NIDM_examples/master/datasets.datalad.org/abide/RawDataBIDS/CMU_a/nidm.ttl",
            "cmu_a.nidm.ttl"
        )
        files.append("cmu_a.nidm.ttl")

    parsed = Query.GetProjectsMetadata(files)


    # assert parsed['projects'][p1][str(Constants.NIDM_PROJECT_DESCRIPTION)] == "Test investigation"
    # assert parsed['projects'][p2][str(Constants.NIDM_PROJECT_DESCRIPTION)] == "More Scans"

    # we shouldn't have the computed metadata in this result
    # assert parsed['projects'][p1].get (Query.matchPrefix(str(Constants.NIDM_NUMBER_OF_SUBJECTS)), -1) == -1


    if USE_GITHUB_DATA:
        # find the project ID from the CMU file
        for project_id in parsed['projects']:
            if project_id != p1 and project_id != p2:
                p3 = project_id
        assert parsed['projects'][p3][str(Constants.NIDM_PROJECT_NAME)] == "ABIDE CMU_a Site"




def test_GetProjectsComputedMetadata():

    p1 = makeProjectTestFile("testfile.ttl")
    p2 = makeProjectTestFile2("testfile2.ttl")
    files = ["testfile.ttl", "testfile2.ttl"]

    if USE_GITHUB_DATA:
        if not Path('./cmu_a.nidm.ttl').is_file():
            urllib.request.urlretrieve (
                "https://raw.githubusercontent.com/dbkeator/simple2_NIDM_examples/master/datasets.datalad.org/abide/RawDataBIDS/CMU_a/nidm.ttl",
                "cmu_a.nidm.ttl"
            )
        files.append("cmu_a.nidm.ttl")

    print ("num files: {}".format(len(files)) )
    print (files)

    parsed = Query.GetProjectsComputedMetadata(files)

    # assert parsed['projects'][p1][str(Constants.NIDM_PROJECT_DESCRIPTION)] == "Test investigation"
    # assert parsed['projects'][p2][str(Constants.NIDM_PROJECT_DESCRIPTION)] == "More Scans"
    # assert parsed['projects'][p2][Query.matchPrefix(str(Constants.NIDM_NUMBER_OF_SUBJECTS))] == 0
    # assert parsed['projects'][p1][Query.matchPrefix(str(Constants.NIDM_NUMBER_OF_SUBJECTS))] == 0


    print ("p1 {}".format(p1))
    print ("p2 {}".format(p2))
    print ("len is {}".format(len(parsed['projects'])))
    if USE_GITHUB_DATA:
        for project_id in parsed['projects']:
            print ("looking at {}".format(project_id))
            if project_id != p1 and project_id != p2:
                p3 = project_id
        print ("got p3 of {}".format(p3))
        assert parsed['projects'][p3][str(Constants.NIDM_PROJECT_NAME)] == "ABIDE CMU_a Site"
        assert parsed['projects'][p3][Query.matchPrefix(str(Constants.NIDM_NUMBER_OF_SUBJECTS))] == 14
        assert parsed['projects'][p3]["age_min"] == 21
        assert parsed['projects'][p3]["age_max"] == 33
        assert parsed['projects'][p3][str(Constants.NIDM_GENDER)] == ['1', '2']


