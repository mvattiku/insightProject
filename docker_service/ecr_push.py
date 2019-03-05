import base64
import docker
import boto3
import sys
import configparser
import os

"""
Uploads images to AWS ECR (Elastic Container Registry)
"""

def ecr_client(region, aws_access_key_id, aws_secret_access_key):
    """
    Connects to ECR (Elastic Container Registry.

    Parameters:
    1) region (str): AWS ECR region
    2) aws_access_key_id (str): AWS account access key
    3) aws_secret_access_key (str): AWS account secret access key

    Returns:
        - ECR service client
    """
    session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    ecr_client = session.client('ecr', region_name=region)
    return ecr_client

def connect_to_ecr(ecr_client, aws_id):
    """
    Step 1: authentication ($(aws ecr get-login --no-include-email --region us-west-2))
    Connects to ECR (Elastic Container Registry).

    Parameters:
    1) ecr_client (str): AWS ECR service client
    2) aws_id (str): AWS account id

    Returns:
        (dict)
        - dictionary of username, password, and registry information used to login to docker to authenticate to a registry
    """
    auth = ecr_client.get_authorization_token(registryIds=[aws_id])
    token = auth["authorizationData"][0]["authorizationToken"]
    username, password = base64.b64decode(token).decode().split(':')
    registry = auth['authorizationData'][0]['proxyEndpoint']
    #expires = auth['authorizationData'][0]['expiresAt']
    #print ("*****", expires)
    print ("Registry:", registry)
    ecr_conn = {'username': username,
                'password': password,
                'registry': registry}
    return ecr_conn

def tag_image(docker_client, image, registry, repository, version):
    """
    Step 2: Tag the local image so that it can be pushed into the repository (docker tag)

    Parameters:
    1) docker_client: docker client to get and tag image
    2) image (str): name of image to be tagged (format- name:version)
    3) registry (str): ECR registry
    4) repository (str): name of repository on ECR to upload image to
    5) version (str): the version to be saved as onto ECR 

    Returns:
        (str)
        - the name the image was tagged as
    """
    img = docker_client.images.get(image)
    registry_name = registry.split("://")[-1]
    tag_name = registry_name+"/"+repository+":"+version
    print("Image tagged as:", tag_name)
    img.tag(tag_name)
    return (tag_name)

def push_image(docker_client, username, password, registry, upload_img, retry=1):
    """
    Step 3: Push this image to the AWS repository (docker push)

    Parameters:
    1) docker_client: docker client to get and tag image
    2) username (str): username for docker login
    3) password (str): password for docker login
    4) registry (str): registry to login to
    5) upload_img (str): name of the image to be uploaded to ECR
    """
    docker_client.login(username, password, registry=registry)
    auth_config = {
        "username": username,
        "password": password
    }
    response = docker_client.images.push(upload_img, auth_config=auth_config)
    response = response.split("\n")
    
    for i in reversed(response):
        if ('errorDetail' in i):
            print ("!Image was not pushed to ECR")

def ecr_push(ecr_client, aws_id, docker_client, image, repository, version):
    """
    Connects to the ECR registry and uploads the image to the appropriate repository.

    Parameters:
    1) ecr_client: ecr_client (str): AWS ECR service client
    2) aws_id (str): AWS account id
    3) docker_client: docker client 
    4) image (str): name of local image to be uploaded (format- name:version)
    5) repository (str): name of repository on ECR to upload image to
    6) version (str): the version to be saved as in the ECR repository
    """
    ecr_conn = connect_to_ecr(ecr_client, aws_id)
    upload_img_name = tag_image(docker_client, image, ecr_conn['registry'], repository, version)
    push_image(docker_client, ecr_conn['username'], ecr_conn['password'], ecr_conn['registry'], upload_img_name)
    return upload_img_name
