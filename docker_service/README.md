# Docker Service
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
        - ```push_to_ecr```: 'true' or 'false' value to indicate if you want the image to be pushed into AWS ECR
        - ```repository```: (optinal if 'push_to_ecr' = false) name of the repository to upload the image to in aws 
        - ```version```: (optinal if 'push_to_ecr' = false) which version to save the image as on ECR (*this version does not have to match the image version in your local docker registry)
        - ```aws_config_file```: (optinal if 'push_to_ecr' = false) .ini file with aws authetication information such as *region*, *aws_access_key_id*, *aws_secret_access_key*, and *aws_id*
    - Output:
        -Image uploaded onto AWS ECR 

## Files

1. ```create_docker.py```: Creates a Dockerfile and Docker Image for a program.
2. ```ecr_push.py```: Pushes the Docker Image to AWS ECR
3. ```AWSConfig.ini```: Config file with authentication information regarding the aws account
4. ```DockerConfig.ini```: Config file with all the necessary parameters to create and push docker image
5. ```main_docker.py```: main file that runs all the services
6. ```push-to-ecr.sh```: Bash file that performs the same command as ```ecr_push.py``` (uploades docker image to AWS ECR) 
        - **How to run:** ```sh push-to-ecr.sh <arg1> <arg2> <arg3> <arg3>```
            - *arg1*: AWS account ID
            - *arg2*: name (with its version) of the docker image to push (ex: imgname:v1)
            - *arg3*: name of the repository on ECR to push the image to 
            - *arg4*: version the image to be saved as in ECR (version can be different from the version in arg2)

## How to Run

The main files needed are ```main_docker.py``` and a docker information config(.ini) file such as ```DockerConfig.ini``` and a AWS authentication information config(.ini) file such as ```AWSConfig.ini```, which is passed in as a variable through the docker config file.

```
python main_docker.py DockerConfig.ini
```
