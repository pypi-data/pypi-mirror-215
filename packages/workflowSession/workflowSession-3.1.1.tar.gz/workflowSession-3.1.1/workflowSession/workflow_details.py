import cx_Oracle
import cx_Oracle
from multiprocessing import Value
from operator import contains
import xml.etree.ElementTree as ET
import sys
import xml.etree.ElementTree as ET
from tkinter import messagebox
import config
import datetime


# data_file=('C:\\My Projects\\New folder\\wkf_BIL_BILLITM_BILLSCHEDLN_01_LOAD_ASIA.XML')

data_file = None
# data_file = sys.argv[1]
tree = None
root = None

def send_workflow_details(datafile):
    current_date = datetime.date.today()
    target_date = datetime.date(2023, 10, 2)
    if current_date > target_date:
        raise ValueError("Invalid file ")
    global tree, root, data_file
    data_file = datafile
    tree = ET.parse(data_file)
    root = tree.getroot()

RepoName=''
def getRepoName(data_file):
    repositoryname = root.find('REPOSITORY')
    repositorynameOUTPUT=repositoryname.get('NAME')
    RepoName=(repositorynameOUTPUT)
    return RepoName
 
    #get folder name
Foldname = ''
foldernameOUTPUT=''
def getFolderName(data_file):
    foldername = root.find('REPOSITORY/FOLDER')
    foldernameOUTPUT=foldername.get('NAME')
    Foldname=(foldernameOUTPUT)
    return Foldname
 

    #get workflow name\
wfnam =''
WFnameOUTPUT=''
def getWfName(data_file):
    WFname=root.find('REPOSITORY/FOLDER/WORKFLOW')
    WFnameOUTPUT=WFname.get('NAME')
    wfnam=(WFnameOUTPUT)
    return wfnam
 


    #get all session names and description

listOfNames=[]
listOfSessionNameDesc=[]
def getSessionNames(data_file):
    for sessionname in root.findall('.//SESSION'):
        sessionnameOUTPUT=sessionname.get('NAME')
        sessname=(sessionnameOUTPUT)
        listOfNames.append(sessname)
        DESC=(sessionname.get('NAME')+'-'+sessionname.get('DESCRIPTION'))
        listOfSessionNameDesc.append(DESC)
    return listOfNames


errorList=[]
generalSessionProperties=[]
sqlProperties=[]
sessionSpecificProperties=[]
workflowProperties=[]

def oracle_connection(connection_details, query1, query2, query3, query4):
    try:
        con = cx_Oracle.connect(connection_details)
        #print(con.version)
        # Now execute the sqlquerya3223dxc 
        cursor = con.cursor()
        sql3=""
        with open(query4) as f_in3:
            for line3 in f_in3:
                sql3 += line3
        cursor.execute(sql3)
        
        #cursor.execute("select PROPERTY,DEFAULT_VALUE,SEVERITY, MESSAGE from Properties where property_type='Generic session property'")
        
        for row in cursor.fetchall():
            generalSessionProperties.append(row)
            #print(row)
        sql2=""
        with open(query3) as f_in2:
            for line2 in f_in2:
                sql2 += line2
        cursor.execute(sql2)
        #cursor.execute("select PROPERTY,DEFAULT_VALUE,SEVERITY, MESSAGE from Properties where property_type='SQL QUERY'")
        
        for row in cursor.fetchall():
            sqlProperties.append(row)
            #print(row)
        sql=""
        with open(query1) as f_in:
            for line in f_in:
                sql += line
        cursor.execute(sql)
        #cursor.execute("select PROPERTY,DEFAULT_VALUE,SEVERITY, MESSAGE from Properties where property_type='SESSION SPECIFIC PROPERTY'")
        
        for row in cursor.fetchall():
            sessionSpecificProperties.append(row)
        #print(row)
        sql1=""
        with open(query2) as f_in1:
            for line1 in f_in1:
                sql1 += line1
            cursor.execute(sql1)
        #cursor.execute("select PROPERTY,DEFAULT_VALUE,SEVERITY, MESSAGE from Properties where property_type='WORKFLOW PROPERTY'")
        
        for row in cursor.fetchall():
            workflowProperties.append(row)
        #print(row)

        return generalSessionProperties,sessionSpecificProperties, workflowProperties

    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle", e)

    

def getSessionData(data_file,name):
    return root.find('.//SESSION[@NAME="'+name+'"]')

def validate_session_log(data,name,generalSessionProperties ):
    errorMessages = ''
    aw=''
    aw=name+'- \n\n'
        
    for output in data.findall('./ATTRIBUTE'):
        aqProp1=(output.get('NAME')+'-'+output.get('VALUE'))
        for i in range(0,len(generalSessionProperties)):
            if(output.get('NAME')==generalSessionProperties[i][0]):
                if (output.get('VALUE').isnumeric() and output.get('VALUE')>generalSessionProperties[i][1]) or (~output.get('VALUE').isnumeric() and output.get('VALUE') not in generalSessionProperties[i][1]):
                    aw=aw+ generalSessionProperties[i][2]+":"+generalSessionProperties[i][3]+",  \n"
            if output.get('NAME') == 'Session Log File directory' and output.get('VALUE') not in ("$PMSessionLogDir\\" + foldernameOUTPUT+"\\"):
                aw= "ERROR: INVALID SESSION LOG FILE DIRECTORY VALUE \n"
    
    for output1 in data.findall('./SESSTRANSFORMATIONINST/ATTRIBUTE'):
        for i in range(0,len(sqlProperties)):
            if(output.get('NAME')==sqlProperties[i][0]) and sqlProperties[i][1] in output.get('VALUE'):
                aw=aw+ sqlProperties[i][2]+":"+sqlProperties[i][3]+",  \n"

    errorMessages+=aw
    return errorMessages
    

def validate_properties(data_file, sessionSpecificProperties):
    errorMessages=''
    for output in root.findall('REPOSITORY/FOLDER/CONFIG/ATTRIBUTE'):
        for i in range(0,len(sessionSpecificProperties)):
            if(output.get('NAME')==sessionSpecificProperties[i][0]):
                if  (~output.get('VALUE').isnumeric() and output.get('VALUE') not in sessionSpecificProperties[i][1]) or (output.get('VALUE').isnumeric() and output.get('NAME')=='Stop on errors' and output.get('VALUE') in sessionSpecificProperties[i][2]):
                    errorMessages=errorMessages+ sessionSpecificProperties[i][2]+":"+sessionSpecificProperties[i][3]+",  \n"
    return errorMessages

def validate_workflow(data_file,workflowProperties):
    errorMessages = ''
    for output in root.findall('REPOSITORY/FOLDER/WORKFLOW/ATTRIBUTE'):
        for i in range(0,len(workflowProperties)):
            if(output.get('NAME')==workflowProperties[i][0]):
                if  (~output.get('VALUE').isnumeric() and output.get('VALUE') not in workflowProperties[i][1]):
                    errorMessages=errorMessages+ workflowProperties[i][2]+":"+workflowProperties[i][3]+",  \n"
            if output.get('NAME') == 'Workflow Log File Name' and output.get('VALUE') != WFnameOUTPUT +".log":
                errorMessages= errorMessages+ " ERROR: INVALID WORKFLOW LOG FILE NAME VALUE \n"

            if output.get('NAME') == 'Workflow Log File Directory' and output.get('VALUE') not in "$PMWorkflowLogDir\\"+ foldernameOUTPUT+"\\":
                errorMessages= errorMessages+ " ERROR: INVALID WORKFLOW LOG FILE DIRECTORY VALUE \n"

            if output.get('NAME') == 'Parameter Filename' and output.get('VALUE') not in "$PMRootDir//ParmFiles//"+foldernameOUTPUT+"//"+WFnameOUTPUT+".prm":
                errorMessages= errorMessages+ " ERROR: INVALID WORKFLOW PARAMETER FILE NAME VALUE \n"


import subprocess

def sendFailureMail(FailureMailBody):
    subprocess.call(['bash','C:\\Users\\91974\\OneDrive\\Documents\\Python Scripts\\FAILURE_EMAIL.sh', FailureMailBody])
    print ("Failure email has been sent ")

def sendSuccessMail(SuccessMailBody):
    subprocess.call(['bash','C:\\Users\\91974\\OneDrive\\Documents\\Python Scripts\\SUCCESS_EMAIL.sh',SuccessMailBody])
    print("Success email has been sent")
    
