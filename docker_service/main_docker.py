import sys
import os 
import configparser
import boto3
import docker

from create_docker import create_dockerfile, create_docker_image
from ecr_push import ecr_push

"""
Creates a Dockerfile for a program and using that file creates a docker image and
uploades it to AWS Elastic Container Registry (ECR).
"""

if __name__ == '__main__':
    
    try:
        config_file_path = sys.argv[1]
        config = configparser.ConfigParser()
        config.read(config_file_path)
    except Exception as e:
        e.args += ("Need to provide a parameters file", )
        raise

    #aws
    aws_config_file = config.get('awsauth', 'aws_config_file')
    aws_config = configparser.ConfigParser()
    aws_config.read(aws_config_file)
    
    region=aws_config.get('aws', 'region')
    aws_access_key_id = aws_config.get('aws', 'aws_access_key_id')
    aws_secret_access_key = aws_config.get('aws', 'aws_secret_access_key')
    aws_id = aws_config.get('aws', 'aws_id')
    

    #dockerfile
    program_path = config.get('dockerfile', 'program_path')
    requirements_file = config.get('dockerfile', 'requirements_file')
    init_file = config.get('dockerfile', 'init_file')

    #dockerimage
    image_name=config.get('dockerimage', 'image_name')
    image_version=config.get('dockerimage', 'image_version')
    
    if not image_version:
        image_version = 'latest'
    image = image_name+":"+image_version

    #ecr
    push_to_ecr=config.get('ecr', 'push_to_ecr') == 'True'
    repository=config.get('ecr', 'repository')
    version=config.get('ecr', 'version')


    #create dockerfile and docker image
    create_dockerfile(program_path=program_path, init_file=init_file, requirements_file=requirements_file)
    create_docker_image(program_path=program_path, image_name=image_name, image_version=image_version)

    #aws session 
    session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    #push image to ecr
    if push_to_ecr:
        docker_client = docker.from_env()
        ecr_client = session.client('ecr', region_name=region)
        ecr_push(ecr_client, aws_id, docker_client, image, repository, version)


