# Batch Service
This service helps to set up batch jobs. Provides utilities to help create computer enviornments, job queues, and job definitions necessary to create a job.

The purpose of this service is to be able to configure the AWS Batch enviornment with a single config file and python scripts instead of going into AWS Batch console.

## Program Files
1. ```batch_util.py```: Contains all the necessary methods to create an aws batch environment 
2. ```AWSConfig.ini```: Config file with authentication information regarding the aws account
3. ```BatchConfig.yml```: Config file with the necessary parameters to create aws batch environment (more info in the next section)
4. ```main_batch.py```: sample main file that runs all the methods from *batch_util.py*

## Required Config Files
### File 1: yaml File
Must provide a ```yaml(.yml) file``` with all the necessary parameters to create the appropriate batch enviornment. 
#### Sections of the yaml File
1. ```Computer Enviornment```: Define the resources and type of instances necessary to run the jobs. 
2. ```Job Queue```: Where the jobs are submitted to. A queue is associated to one or more computer resources. The jobs in the queue have access to only the resources defined in the associated computer enviornment(s). 
3. ```Job Definition```: Defines how the job will run. Define the docker image to use (so which model to run) as well as the command to run the model. 
4. ```Job```: Actual unit of work executed as containerized applications by AWS Batch.

***Note:*** Not all sections need to be defined in the yaml file. Just define the sections neccessary to run the methods being used from ```batch_util.py```. 
- Ex: To just set up a computer enviornment and a queue for it, just provide parameters for the *Computer Environment* and *Job Queue* sections in the yaml file. 

***Note:*** For a given section, must provide all the required parameters under that section. 
### File 2: AWS Config (.ini) File
Config file with authentication information, such as aws key, id, secret key, and region associated with the aws account.

## How to Run
The main files needed are ```main_batch.py``` and a batch information config(.yml) file such as ```BatchConfig.yml``` and a AWS authentication information config(.ini) file such as ```AWSConfig.ini```. 

```
python main_batch.py BatchConfig.yml AWSConfig.ini
```

