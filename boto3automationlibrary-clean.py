"""
############################################
##### 2019-09-18 removed SAML code
##### 2020-08-18 added client initilization to start of the script
##### 2020-08-25 added many methods for EC2Operations
##### 2020-09-11 modified ASG resume/suspend processes' function to take ASG suffix
##### 2020-09-15 added method to copy files within same bucket - WIP
##### 2020-09-18 added method to modify desiredCapacity, min, maxSize of ASG
##### 2020-09-21 added method to update CodeDeploy DG with an ASG
##### 2020-10-30 cleaned file for github upload
"""


import boto3 as bt
import sys, rsa, base64, matplotlib, json
import argparse as ar
import subprocess as sb
from tkinter import *
from tkinter import ttk
from tkinter.font import *
import tkinter.font as font
import random as rn
import tkinter as tk
from pprint import pprint as pp
from os import path as pt
from botocore import exceptions as ex
from tkinter import messagebox
import pprint as ppr

## Set default profile to name SAML, you can change ton any other profile saml, based on your AWS profile setup
bt.setup_default_session(profile_name='saml')

## Initilize the client for different AWS services
ec2client = bt.client('ec2')
asgclient = bt.client('autoscaling')
cfclient = bt.client('cloudformation')
lbclient = bt.client('elbv2')
cdclient = bt.client('codedeploy')
s3Resource = bt.resource('s3')
s3client = bt.client('s3')

## for codedeployfile upload
downloadsDir = r'<<DownloadDir>>'
zip_file_name_suffix = '.zip'

## S3 prefix is harcoded here
## TODO: make it dynamic
s3_object_prefix_key = "abc/"

## Color scheme, can be changed to your liking
## Refer https://htmlcolorcodes.com/
submitButtonBGColor = '#302908'
exitButtonBGColor = '#000000'
exitButtonFGColor = '#F1C9C9'
exitButtonFGColor = '#F1C9C9'
radioButtonBGColor = '#FFFFFF'
mainmenuBGColor = '#FFCD98'
mainmenuFGColor = '#010100'

snapshotIDList = []

masterMenuList = ["EC2 instance management",
                  "ASG management",
                  "CloudFormation management",
                  "codeDeploy management",
                  "S3 object management"
                  ]

ec2LabelList = ["Terminate EC2 instance",
                "Stop EC2 instance",
                "Start EC2 instance",
                "Enable termination protection",
                "Disable termination protection",
                "Get Windows password",
                "Add no-backup for CPM",
                "Add extended-ec2 work schedule tag",
                "Add RDS extended-ec2 work schedule tag"]

ec2ManagementMenu = [
    ("Terminate EC2 instance", 1),
    ("Stop EC2 instance", 2),
    ("Start EC2 instance", 3),
    ("Reboot EC2 instance", 4),
    ("Enable termination protection", 5),
    ("Disable termination protection", 6),
    ("Add no-backup tag for CPM", 7),
    ("Add EC2 extended work schedule tag", 8),
    ("Add RDS stop work schedule tag", 9)
]

asgProcessList = ['Launch', 'Terminate', 'AddToLoadBalancer', 'AlarmNotification',
                  'AZRebalance', 'HealthCheck', 'InstanceRefresh', 'ReplaceUnhealthy', 'ScheduledActions']
asgSelectedList = []
autoScalingGroupsMasterList = []

color = {"black": "#32373E", "orange": "#EE8D1F", "green": "#33FF7C"}

envNameList = ['ops', 'dev', 'int', 'uat', 'prd', 'ept']
portList = [80, 8080, 443, 15672, 11223, 8443, 5672, 8444]


def Extract(lst):
    return [item[0] for item in lst]


def getRandomColor():
    colorList = list(matplotlib.colors.cnames.values())
    return(rn.choice(colorList))


def getPrivateIP(InstanceID):
    response = ec2client.describe_instances(
        InstanceIds=[
            InstanceID,
        ],
    )
    return (response['Reservations'][0]['Instances'][0]['PrivateIpAddress'])

# Manage Lanuch, Terminate process on an ASG


def resumeASGProcesses(ASGSuffix, processList):
    descResponse = asgclient.describe_auto_scaling_groups(MaxRecords=100)
    for autoScalingGroups in descResponse['AutoScalingGroups']:
        autoScalingGroupsMasterList.append(
            autoScalingGroups['AutoScalingGroupName'])
    ASGName = [i for i in autoScalingGroupsMasterList if ASGSuffix in i]

    response = asgclient.resume_processes(
        AutoScalingGroupName=str(ASGName[0]),
        ScalingProcesses=processList)
    autoScalingGroupsMasterList.clear()
    return(ppr.pformat(response))


def suspendASGProcesses(ASGSuffix, processList):
    descResponse = asgclient.describe_auto_scaling_groups(MaxRecords=100)
    for autoScalingGroups in descResponse['AutoScalingGroups']:
        autoScalingGroupsMasterList.append(
            autoScalingGroups['AutoScalingGroupName'])
    ASGName = [i for i in autoScalingGroupsMasterList if ASGSuffix in i]

    response = asgclient.suspend_processes(
        AutoScalingGroupName=str(ASGName[0]),
        ScalingProcesses=processList)
    autoScalingGroupsMasterList.clear()
    return(ppr.pformat(response))


# Manage EC2 Instance
def terminateEC2Instance(InstanceID):
    response = ec2client.terminate_instances(
        InstanceIds=[
            InstanceID,
        ]
    )
    return(InstanceID + " is being terminated, please check")


def startEC2Instance(InstanceID):
    response = ec2client.start_instances(
        InstanceIds=[
            InstanceID,
        ]

    )
    return(InstanceID + " is started, please check")


def stopEC2Instance(InstanceID):
    response = ec2client.stop_instances(
        InstanceIds=[
            InstanceID,
        ]

    )
    return(InstanceID + " is stopped, please check")


def rebootEC2Instance(InstanceID):
    response = ec2client.reboot_instances(
        InstanceIds=[
            InstanceID,
        ]

    )
    return(InstanceID + " is rebooted, please check")


def enableTerminationProtection(InstanceID):
    response = ec2client.modify_instance_attribute(
        DisableApiTermination={
            'Value': True
        },
        InstanceId=InstanceID,
    )
    return("Termination Protection is enabled for " + InstanceID + ".please check")


def disableTerminationProtection(InstanceID):
    response = ec2client.modify_instance_attribute(
        DisableApiTermination={
            'Value': False
        },
        InstanceId=InstanceID,
    )
    return("Termination Protection is disabled for " + InstanceID + ".please check")


def deleteStack(stackName):
    response = cfclient.delete_stack(
        StackName=stackName,

    )
    return(stackName + " is being deleted, please check")


def getWindowsPassword(InstanceID, choice, privKeyFile):
    response = ec2client.get_password_data(
        InstanceId=InstanceID,
    )
    passwd = base64.b64decode(response['PasswordData'])
    with open(privKeyFile, 'r') as privkeyfile:
        priv = rsa.PrivateKey.load_pkcs1(privkeyfile.read())
        key = rsa.decrypt(passwd, priv)

    privateIP = getPrivateIP(InstanceID)
    decodedKey = key.decode("utf-8")
    return privateIP, decodedKey


def getStackResources(stackName):
    response = cfclient.list_stack_resources(
        StackName=stackName,
    )
    return(response['StackResourceSummaries'][0])


def describeASG(ASGName):
    response = asgclient.describe_auto_scaling_groups(
        AutoScalingGroupNames=[
            ASGName,
        ],
    )


def addRDSTag(InstanceID):
    response = ec2client.create_tags(
        Resources=[
            InstanceID,
        ],
        Tags=[
            {
                'Key': 'work-schedule',
                'Value': 'melbourne-stop-after-hours-rds'
            },
        ]
    )
    return(ppr.pformat(response))


def addCPMTag(InstanceID):
    response = ec2client.create_tags(
        Resources=[
            InstanceID,
        ],
        Tags=[
            {
                'Key': 'cpm backup',
                'Value': 'no-backup'
            },
        ]
    )
    return(ppr.pformat(response))


def untagWS(InstanceID):
    response = ec2client.create_tags(
        Resources=[
            InstanceID,
        ],
        Tags=[
            {
                'Key': 'work-schedule-donotrun',
                'Value': ''
            },
        ]
    )
    return(ppr.pformat(response))


def enableDeletionProtectionLB(lbARN):
    response = lbclient.modify_load_balancer_attributes(
        LoadBalancerArn=lbARN,
        Attributes=[
            {
                'Key': 'deletion_protection.enabled',
                'Value': 'true'
            },
        ]
    )
    return(response)


def enableDeletionProtectionLB(lbARN):
    response = lbclient.modify_load_balancer_attributes(
        LoadBalancerArn=lbARN,
        Attributes=[
            {
                'Key': 'deletion_protection.enabled',
                'Value': 'false'
            },
        ]
    )
    return(response)


def tagExtendedOfficeHoursEC2(InstanceID):
    response = ec2client.create_tags(
        Resources=[
            InstanceID,
        ],
        Tags=[
            {
                'Key': 'work-schedule',
                'Value': 'melbourne-extended-office-hours-ec2'
            },
        ]
    )
    return(ppr.pformat(response))


def getCodeDeployDGTarget(CDAppName):
    reponse = cdclient.get_deployment_group(
        applicationName=CDAppName,
        deploymentGroupName=(CDAppName + "-deployment-group")
    )
    return(reponse['deploymentGroupInfo']['autoScalingGroups'][0]['name'])


def describeStack(stackName):
    stackOutputList = []
    try:
        response = cfclient.describe_stacks(
            StackName=stackName,
        )
        for Outputs in response['Stacks'][0]['Outputs']:
            stackOutputList.append(Outputs['ExportName'])
            stackOutputList.append(Outputs['OutputValue'])
            stackOutputList.append("------------------")
        stackOutputList = '\n'.join(stackOutputList)
        return(stackOutputList)
    except ex.ClientError as ce:
        return(ce)


def changeEC2InstanceType(InstanceID, instanceType):
    response = ec2client.modify_instance_attribute(
        InstanceType={
            'Value': instanceType
        },
        InstanceId=InstanceID,
    )
    return("InstanceType" + instanceType + " modified, please check\n " + str(response(['ResponseMetadata']['HTTPStatusCode'])))


def uploadToS3Location(absolutePathName, bucketName, keyName):
    keyName1 = (s3_object_prefix_key + keyName + zip_file_name_suffix)
    uploadOperation = s3Resource.meta.client.upload_file(
        pt.join(downloadsDir, absolutePathName + zip_file_name_suffix),
        bucketName,
        (s3_object_prefix_key + keyName + zip_file_name_suffix))
    return(uploadOperation)


def copyBetweenSameS3Buckets(bucketName, fromKey, toKey):
    s3ObjectList = []
    s3ObjectList.clear()
    s3ObjectList.append('S3 object list is as follows -->')
    s3ObjectList.append('\n')

    try:
        copy_source = {
            'Bucket': bucketName,
            'Key': fromKey
        }
        s3Resource.meta.client.copy(copy_source, bucketName, toKey)
        toKeyForS3ls = toKey.split('/')
        response = s3client.list_objects_v2(
            Bucket=bucketName,
            Prefix=toKeyForS3ls[0]
        )
        s3ObjectCount = range(len(response['Contents']))
        for i in s3ObjectCount:
            s3ObjectList.append(response['Contents'][i]['Key'])
        return("S3 copy is successfull, please check bucket")
    except ex.ClientError as ce:
        return(ce)
    except UnboundLocalError as ue:
        return(ue)


def listS3Objects(bucketName, keyName):
    s3ObjectList = []
    s3ObjectList.clear()
    s3ObjectList.append('S3 object list is as follows -->')
    s3ObjectList.append('\n')
    keyName = ""
    try:
        if (keyName.__contains__('/')):
            toKeyForS3ls = keyName.split('/')
        response = s3client.list_objects_v2(
            Bucket=bucketName,
            Prefix=toKeyForS3ls[0]
        )
        s3ObjectCount = range(len(response['Contents']))
        for i in s3ObjectCount:
            s3ObjectList.append(response['Contents'][i]['Key'])
    except ex.ClientError as ce:
        return(ce)
    except UnboundLocalError as ue:
        return(ue)
    return(s3ObjectList)


def deregisterAMIdeleteSnapshots(amiID):
    try:
        snapshotIDList.clear()
        ec2client.deregister_image(
            ImageId=amiID,
            DryRun=False)
        response = ec2client.describe_snapshots(
            Filters=[
                {
                    'Name': 'description',
                    'Values': ['*' + amiID + '*']
                }, ],
            DryRun=False)
        snapshotSummaryLength = len(response['Snapshots'])
        for i in range(snapshotSummaryLength):
            snapshotIDList.append(response['Snapshots'][i]['SnapshotId'])
        for j in snapshotIDList:
            ec2client.delete_snapshot(
                SnapshotId=str(j)
            )
    #    snapshotIDList.clear()
        return('snaphotsDeleted are -->' + str(snapshotIDList))
    except ex.ClientError as ce:
        return(ce)


def getASGNameFromStack(stackName, appName, envName, roleName):
    stackOutputList = []
    response = cfclient.describe_stacks(
        StackName=stackName,
    )
    for Outputs in response['Stacks'][0]['Outputs']:
        stackOutputList.append(Outputs['OutputValue'])
    asgName = [i for i in stackOutputList if roleName in i]
    return(str(asgName[0]))
    cdclient.update_deployment_group(
        applicationName='string')


def copyBetweenDifferentS3Buckets(fromBucketName, toBucketName, fromKey, toKey):
    s3ObjectList = []
    s3ObjectList.clear()
    s3ObjectList.append('S3 object list is as follows -->')
    s3ObjectList.append('\n')

    try:
        copy_source = {
            'Bucket': fromBucketName,
            'Key': fromKey
        }
        s3Resource.meta.client.copy(copy_source, toBucketName, toKey)
        toKeyForS3ls = toKey.split('/')
        response = s3client.list_objects_v2(
            Bucket=toBucketName,
            Prefix=toKeyForS3ls[0]
        )
        s3ObjectCount = range(len(response['Contents']))
        for i in s3ObjectCount:
            s3ObjectList.append(response['Contents'][i]['Key'])
        return(s3ObjectList)
    except ex.ClientError as ce:
        return(ce)
    except UnboundLocalError as ue:
        return(ue)


def detachEC2InstanceFromASG(ASGSuffix, instanceId):
    try:
        descResponse = asgclient.describe_auto_scaling_groups(MaxRecords=100)
        for autoScalingGroups in descResponse['AutoScalingGroups']:
            autoScalingGroupsMasterList.append(
                autoScalingGroups['AutoScalingGroupName'])
        ASGName = [i for i in autoScalingGroupsMasterList if ASGSuffix in i]

        response = asgclient.detach_instances(
            InstanceIds=[
                str(instanceId),
            ],
            AutoScalingGroupName=str(ASGName[0]),
            ShouldDecrementDesiredCapacity=False
        )
        return(ppr.pformat(response))
    except ex.ClientError as ce:
        return(ce)


def modifyASGCapacityFunction(ASGSuffix, desiredCapacity, minSize, maxSize):
    descResponse = asgclient.describe_auto_scaling_groups(MaxRecords=100)
    for autoScalingGroups in descResponse['AutoScalingGroups']:
        autoScalingGroupsMasterList.append(
            autoScalingGroups['AutoScalingGroupName'])
    ASGName = [i for i in autoScalingGroupsMasterList if ASGSuffix in i]

    response = asgclient.update_auto_scaling_group(
        AutoScalingGroupName=str(ASGName[0]),
        MinSize=int(minSize),
        MaxSize=int(maxSize),
        DesiredCapacity=int(desiredCapacity)
    )
    return(ppr.pformat(response))


def updateCodeDeployDGTarget(appName, envName, componentName, ASGSuffix):
    descResponse = asgclient.describe_auto_scaling_groups(MaxRecords=100)
    for autoScalingGroups in descResponse['AutoScalingGroups']:
        autoScalingGroupsMasterList.append(
            autoScalingGroups['AutoScalingGroupName'])
    ASGName = [i for i in autoScalingGroupsMasterList if ASGSuffix in i]

    response = cdclient.update_deployment_group(
        applicationName=(appName + '-' + envName + '-' + componentName),
        currentDeploymentGroupName=(
            appName + '-' + envName + '-' + componentName + '-deployment-group'),
        autoScalingGroups=[
            str(ASGName[0])
        ]
    )
    return(ppr.pformat(response))
