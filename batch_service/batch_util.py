"""
This object creates a client representation of AWS Batch and provides certain methods 
to setup the appropriate eviornemnt to run jobs. A yaml file contining the parameters
necessary to create computer enviornment, job queue, job definition, and jobs can be passed
to utilize the provided methods. 

Yaml File: 
The 4 possible sections are comp_env, job_queue, job_def, and job. Not all sections are needed. 
Just provide information necssary for the methods being used. However, for a given section all 
the parameter information must be provided. 

For certain methods, certain information can be overrriden by providing arguments when call
the methods. 
"""
# ______________________________________________________________________________

import yaml
import boto3
import time


class Batch(object):

    def __init__(self, 
                 client=None,
                 config_file=None, 
                 comp_env_dict=None, 
                 job_queue_dict=None, 
                 job_def_dict=None, 
                 job_dict=None):
        """
        Defines the variable necessary for cerating computer enviornments, job queues,
        job definitions, and jobs. client must be defined. config_file must be defined
        if the rest of the dict parameters are not provided or can provide the other 
        dict parameters and not provide a config_file. If config_file defined, the other 
        dict parameters are ignored. 

        Inputs:
            client = boto batch client (default=None)
            config_file = yaml file path that contains all the necessary parameters to 
                          setup batch enviornments (default=None)
            comp_env_dict = dict of batch computer environment parameters (default=None)
            job_queue_dict = dict of batch job queue parameters (default=None)
            job_def_dict = dict of batch job definition parameters (default=None)
            job_dict = dict of batch job parameters (default=None)
        """

        self.comp_env_dict = comp_env_dict
        self.job_queue_dict = job_queue_dict
        self.job_def_dict = job_def_dict
        self.job_dict = job_dict
        self.client = client
        
        if config_file: 
            with open(config_file) as c:
                config = yaml.load(c)
            self.comp_env_dict = config['comp_env']
            self.job_queue_dict = config['job_queue']
            self.job_def_dict = config['job_def']
            self.job_dict = config['job']

            # print (self.comp_env_dict)
            # print ("\n", self.job_queue_dict)
            # print ("\n", self.job_def_dict)
            # print ("\n", self.job_dict)

    #1) create computer Environment
    def create_compute_environment(self):
        """
        Creates a computer evironment in AWS batch.
        Computer Environment: Defines the resources (i.e. memory, network, vCpus, IAM roles)
                              and type of instances the jobs can run on. 

        Returns:
            - client response 
        """
        try:
            print (self.comp_env_dict)
            comp_env_response = self.client.create_compute_environment(
                computeEnvironmentName=self.comp_env_dict['computer_enviornment_name'],
                type='MANAGED',
                computeResources={
                    'type': 'EC2',
                    #'ec2KeyPair': 'id_rsa',
                    'instanceRole': self.comp_env_dict['instance_role'],
                    'instanceTypes': [
                        'optimal'
                    ],
                    'maxvCpus': self.comp_env_dict['max_vcpus'],
                    'minvCpus': 0,
                    'securityGroupIds': self.comp_env_dict['security_group_ids'],
                    'subnets': self.comp_env_dict['subnets'],
                },
                serviceRole=self.comp_env_dict['service_role'],
                state='ENABLED',
            )
            print("Computer environment '{}' created".format(self.comp_env_dict['computer_enviornment_name']))
            return(comp_env_response)
        except Exception as e:
            print("!Exception:", e)
    
    #2) Create Job Queue
    def create_job_queue(self, comp_env=None, retry=1):
        """
        Creates a job queue in AWS batch.
        Job Queue: This is where jobs are submitted to. Defines they type of resources the jobs can use.  
                   A job queue is associate to one or more compute environments. 

        Parameters:
        1) comp_env (str): (default=None) computer enviornment resources the jobs in the queue will use
        2) retry (int): (default=1) retry attempts if creating job queue fails 

        Returns:
            - client response 
        """
        if comp_env == None:
            comp_env = self.job_queue_dict['computer_enviornment_name']
        try:
            queue_response = self.client.create_job_queue(
                computeEnvironmentOrder=[
                    {
                        'computeEnvironment': comp_env,
                        'order': 1,
                    },
                ],
                jobQueueName=self.job_queue_dict['job_queue_name'],
                priority=self.job_queue_dict['job_queue_priority'],
                state='ENABLED',
            )
            print("Job queue '{}' created with computer environment '{}'".format(self.job_queue_dict['job_queue_name'], comp_env))
            return(queue_response)
        except Exception as e:
            print("!Exception:", e)
            if ("Object already exists" in str(e)): #if queue already exists, returns
                return
            response = self.client.describe_compute_environments(  #getting info on 'comp_env' computer environment
                computeEnvironments=[comp_env],
            )
            if (len(response['computeEnvironments']) == 0):
                print ("!Computer Environment '{}' not found".format(comp_env))
                return
            env = response['computeEnvironments'][0]
            if (env['status'] != 'VALID'):  #if 'comp_env' is not in valid status, program sleeps 15sec to give time for env to be valid
                time.sleep(15)  
            if (retry > 0): #since 'comp_env' exists, retry method applied to create queue
                print("Retrying to create queue with computer environment '{}'".format(comp_env))
                self.create_job_queue(comp_env=comp_env, retry=retry-1)
            else:
                print ("!Computer Environment '{}' status is '{}'".format(comp_env,  env['status']), end = " - ")
                print ("Unable to create queue")
        
    #3) Create Job Definition 
    #Need to upload docker file and call the appropriate file
    def create_job_definition(self, job_def_name = None, image = None):
        """
        Creates a job definition in AWS batch.
        Job Definition: Tells how a job should run. This is where the docker image is defined 
                        to tell jobs which model or program to run. 

        Parameters:
        1) job_def_name (str): (default=None) name for the job defintion
        2) image (str): (default=None) docker image from ECR that the definition is based on

        Returns:
            - client response 
        """
        if job_def_name == None:
            job_def_name = self.job_def_dict['job_definition_name']
        if image == None:
            image = self.job_def_dict['image']
        try:
            job_def_response = self.client.register_job_definition(  #creating job definition with name 'job_def_name'
                jobDefinitionName=job_def_name,
                type='container',
                parameters= self.job_def_dict['job_definition_param'],
                containerProperties={
                    'command': [ self.job_def_dict['command'] ],
                    'image': image,
                    'memory': self.job_def_dict['memory'],
                    'vcpus': self.job_def_dict['vcpus'],
                    'environment': self.job_def_dict['job_definition_enviornment_variables'],
                }
                
            )
            latest_version = self.latest_version_job_definition(job_def_name=job_def_name)
            if latest_version > 0:
                print ("Job definition '{}' exits. Revision '{}' created.".format(job_def_name, latest_version))
            else:
                print("Job Definition '{}' does not exist".format(job_def_name))
            return job_def_response
        except Exception as e:
            print("!Exception:", e)

    #4) Submit a Job
    def create_job(self, job_name = None, job_def_name = None, job_queue=None):
        """
        Creates a job in AWS batch.

        Parameters:
        1) job_name (str): (default=None) name for the job
        2) job_def_name (str): (default=None) name of the job defintion used to create the job
        3) job_queue (str): (default=None) name of the queue the job is created in

        Returns:
            - client response 
        """

        if job_name == None:
            job_name = self.job_dict['job_name']
        if job_def_name == None:
            job_def_name = self.job_dict['job_definition_name']
        if job_queue == None:
            job_queue = self.job_dict['job_queue_name']

        try:
            job_response = self.client.submit_job(
                jobDefinition= job_def_name,
                jobName=job_name,
                jobQueue=job_queue,
                parameters=self.job_dict['job_param'],
                containerOverrides={
                    'vcpus': self.job_dict['job_vcpus'],
                    'memory': self.job_dict['job_memory'], 
                    'command': [self.job_dict['job_command']],
                    'environment': self.job_dict['job_enviornment_variables']
                },
                retryStrategy={
                    'attempts': self.job_dict['retry_attempts']
                }
            )
            print("Job '{}' created".format(job_name))
            return job_response
        except Exception as e:
            print ("!Exception", e)  

    #get the latest version of job definition
    def latest_version_job_definition(self, job_def_name=None):
        """
        Looks for the latest version of a given job definition.

        Parameters:
        1) job_def_name (str): (default=None) name of job definition

        Returns:
            - (int) latest version of the job definition; returns 0 if the job definition does not exist
        """

        if job_def_name == None:
            job_def_name = self.job_def_dict['job_definition_name']

        response = self.client.describe_job_definitions( #checking for all versions of the newly created job defintion ('job_def_name')
                jobDefinitionName=job_def_name,
                status='ACTIVE'
            )
        if (len(response['jobDefinitions']) != 0):
            revisions = []
            for i in response['jobDefinitions']:
                revisions.append(i['revision'])
            version = max(revisions)    #getting the version of the job definition just created (if the definition already existed)
            return version
        else:
            return 0