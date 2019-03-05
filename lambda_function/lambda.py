import boto3
import datetime
import os

def latest_version_job_definition(client, job_def_name):
    '''
    Looks at the version of a given job definition.
    Parameters:
    1) clinet: boto client connected to batch
    2) job_def_name (str): name of job definition
    Returns:
        - (int) latest version of the job definition; returns 0 if the job definition does not exist
    '''
    response = client.describe_job_definitions( #checking for all versions for a job defintion ('job_def_name')
            jobDefinitionName=job_def_name,
            status='ACTIVE',
        )
    if (len(response['jobDefinitions']) != 0): #get the max version if the job definition exists
        revisions = []
        for i in response['jobDefinitions']:
            revisions.append(i['revision'])
        version = max(revisions)
        return version
    else:
        return 0    #return 0 if the job definition does not exist

def lambda_handler(event, context):
    now = datetime.datetime.now().strftime('%y_%m_%d_%H_%M_%S') #current time

    job_queue = os.environ['JOB_QUEUE_NAME']
    job_def_name = os.environ['JOB_DEFINITION_NAME']

    sourceKey = event['Records'][0]['s3']['object']['key']   #name of the file
    sourceSize = event['Records'][0]['s3']['object']['size'] #size of the file
    print("sourceKey:", sourceKey, "sourceSize:", sourceSize)

    client = boto3.client('batch', 'us-west-2')

    #job definition to use for the job (looking for the latest version of the job definition)
    version = latest_version_job_definition(client, job_def_name)
    if version > 0:
        job_def_name = job_def_name+":"+str(version)

    #job name: gives the same name as the input file name (with out the .json part)
    if("/" in sourceKey) and ("." in sourceKey):
        filename = sourceKey.split("/")[-1]
        job_name = filename.split(".")[0]
    else:
        job_name = "test_{}".format(now)

    #submit job
    print ("Job Name:", job_name)
    print ("Job Definition:", job_def_name)
    print ("Filename:", filename)
    client.submit_job(
        jobName= job_name,
        jobQueue= job_queue, #job queue this job shoud run in
        jobDefinition=job_def_name,
        parameters= {
            "infile" : filename
        }
    )
    print ("job submitted to batch")