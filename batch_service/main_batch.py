"""
Sample on how to use the batch_util.

To Run: "python main_batch.py BatchConfig.yml AwsConfig.ini
    need to provide two command line arguments.
    Argument 1 = yaml file path with batch parameters defined 
    Argument 2 = aws config(.ini) file path with aws account info (such as aws_key, region, ...)
"""
#_____________________________________________________________________________________________________

import sys
import os 
import configparser
import boto3

from batch_util import Batch


if __name__ == '__main__':
    
    try:
        yaml_file_path = sys.argv[1] #batch yaml file
        config_file_path = sys.argv[2] #aws config file
        aws_config = configparser.ConfigParser()
        aws_config.read(config_file_path)
    except Exception as e:
        e.args += ("Need to provide a parameters file", )
        raise
    
    #aws
    region=aws_config.get('aws', 'region')
    aws_access_key_id = aws_config.get('aws', 'aws_access_key_id')
    aws_secret_access_key = aws_config.get('aws', 'aws_secret_access_key')
    aws_id = aws_config.get('aws', 'aws_id')

    #aws session and batch client
    session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    client = session.client('batch', 'us-west-2')

    #Batch Util Obj
    batch = Batch(client=client, config_file=yaml_file_path) #must provide client to be able to use other Batch methods

    #create computer environement
    batch.create_compute_environment()

    #create job queue
    batch.create_job_queue()

    #create job definition
    batch.create_job_definition()

    #create job
    batch.create_job()

    #get latest job definition version
    latest_version = batch.latest_version_job_definition(job_def_name="test") #if parameter not provide here, then job_Def_name from yaml file will be used
    




