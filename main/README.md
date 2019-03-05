# Main
This service helps data scientist dockerize their models. The purpose of dockerizing the models is so that it is easy to move models from development to production as well as reproduce the models, since they are well encapsulated into a defined enviornment. 

## Services

1. **Creating the Dockerfile:** Given the program script files and requirements.txt file or bash file, a Dockerfile is created and saved into the program folder.
    - Required Input: 
        - ```program_path```: path to the program scripts
    - Optinal Input: 
        - ```requirements_file```: requirements.txt file with all the pip installation necessary to run the program
        - ```init_file```: (.sh file) bash script that contains all of the installation necessary to run the program
    - Output:
        - *Dockerfile*: docker file with the necessary commands is created
            - program scrits are saved into a ```/program/``` folder
            - docker file built on top of the base image ```python:3.6```
            - working directory is the ***program*** folder (```WORKDIR /program```)
2. **Creating a Docker Image:** Using the Dockerfile created, a docker image is created for that program
<br>Equivalent to running ```docker build -t <name:version> <path to Dockerfile>``` on cmd line
    - Required Input: 
        - ```image_name```: name for the image
        - ```image_version```: version of the image (or program)
    - Output:
        - *Docker image* of the program is created and saved to your local docker registry
        - ```NOTE:``` Must have Docker engine installed and running on your computer.
3. **Upload the Image to AWS ECR:** Uploades the docker image into aws Elastic Container Registry (ECR)
    - Required Input:
        - ```push_to_ecr```: *true* or *false* value to indicate if you want the image to be pushed into AWS ECR
        - ```repository```: (optinal if *push_to_ecr* = false) name of the repository to upload the image to in aws 
        - ```version```: (optinal if *push_to_ecr* = false) which version to save the image as on ECR (*this version does not have to match the image version in your local docker registry)
        - ```aws_config_file```: (optinal if *push_to_ecr* = false) .ini file with aws authetication information such as *region*, *aws_access_key_id*, *aws_secret_access_key*, and *aws_id*
    - Output:
        - Image uploaded onto AWS ECR 
4. **Create Job Definition in AWS Batch:** Creates a job definition with the uploaded image so that batch jobs can be set up using this docker image. 
    - Required Input:
        - ```create_job_def```: *true* or *false* value to indicated if you want to create a job definition in aws batch with the uploaded docker image
        - ```batch_config_file```: yaml file with the parameters needed to create a job definition
    - Output:
        - Job definition created for the docker image (if a previous definition existed already the a new version created)

## Folders & Files
1. ```docker_service```: helps dockerize models and push them into aws ECR
    1. ```create_docker.py```: Creates a Dockerfile and Docker Image for a program.
    2. ```ecr_push.py```: Pushes the Docker Image to AWS ECR
    3. ```push-to-ecr.sh```: Bash file that performs the same command as ```ecr_push.py``` (uploades docker image to AWS ECR) 
        - **How to run:** ```sh push-to-ecr.sh <arg1> <arg2> <arg3> <arg3>```
            - *arg1*: AWS account ID
            - *arg2*: name (with its version) of the docker image to push (ex: imgname:v1)
            - *arg3*: name of the repository on ECR to push the image to 
            - *arg4*: version the image to be saved as in ECR (version can be different from the version in arg2)

2. ```batch_service```: helps set up batch jobs
    1. ```batch_util.py```: Contains all the necessary methods to create an aws batch environment


3. ```main```: main program file to dockerize models, upload to aws, and create batch jobs
    - Config Files:
        1. ```AwsConfig.ini```: (Required) Config file with authentication information regarding the aws account
        2. ```Config.ini```: (Required) Config file with all the necessary parameters to create, push docker image, and set-up batch enviornment
        3. ```BatchConfig.yml```: (Optional - only required if working with *batch_util.py*) Config file with the necessary parameters to create aws batch environment (more info in the next section)
    - Main Files:
        1. ```main.py```: main file to run all the services 
            - Dockerfile -> Docker Image -> Upload to AWS ECR -> Job Definition of Image (in AWS Batch)
        2. ```main2.py```: main file that can be used to develop and update AWS Batch enviornment
        <br> **Note:** This main file can be used to set up the computer enviornment and job queue in which the jobs can run through the lambda function. Do not need to set up the computer enviornment and job queue everytime new job definitions are created (same ones can be used)
            - When the computer enviornment and job queues are changed, update the lambda function so that the jobs are created into the appropriate queue. 
    
## How to Run

The main files needed are ```main.py``` or ```main_b.py``` and a parameters config(.ini) file such as ```Config.ini``` and a AWS authentication information config(.ini) file such as ```AwsConfig.ini``` and AWS Batch parameter config(.yml) file such as ```BatchConfig.yml```. 

***Note:*** The ```BatchConfig.yml``` is only necessary if a job definition is being created from the uploaded ECR image or changes are being made in AWS Batch. 

```
python main.py Config.ini
```
OR
```
python main_b.py BatchConfig.yml AwsConfig.ini
```
